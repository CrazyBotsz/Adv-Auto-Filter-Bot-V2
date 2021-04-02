import motor.motor_asyncio # pylint: disable=import-error
from bot import DB_URI

class Singleton(type):
    __instances__ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances__:
            cls.__instances__[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instances__[cls]


class Database(metaclass=Singleton):

    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.db = self._client["Adv_Auto_Filter"]
        self.col = self.db["Main"]
        self.acol = self.db["Active_Chats"]
        self.fcol = self.db["Filter_Collection"]
        
        self.cache = {}
        self.acache = {}

    async def create_index(self):
        await self.fcol.create_index([("file_name", "text")])


    def new_chat(self, g_id, c_id, c_name):
        try:
            g_id, c_id = int(g_id), int(c_id)
        except:
            pass
        
        return dict(
            _id = g_id,
            chat_ids = [{
                "chat_id": c_id,
                "chat_name": c_name
                }],
            types = dict(
                video=True,
                audio=False,
                document=True
            ),
            configs = dict(
                max_pages=5,
                max_results=50,
                max_per_page=10,
                show_invite_link=True              
            )
        )


    async def status(self, group_id: int):
        
        group_id = int(group_id)
        
        total_filter = await self.tf_count(group_id)
        
        chats = await self.find_chat(group_id)
        chats = chats.get("chat_ids")
        total_chats = len(chats) if chats is not None else 0
        
        achats = await self.find_active(group_id)
        if achats not in (None, False):
            achats = achats.get("chats")
            if achats == None:
                achats = []
        else:
            achats = []
        total_achats = len(achats)
        
        return total_filter, total_chats, total_achats


    async def find_group_id(self, channel_id: int):
        
        data = self.col.find({})
        group_list = []

        for group_id in await data.to_list(length=50): # No Need Of Even 50
            for y in group_id["chat_ids"]:
                if int(y["chat_id"]) == int(channel_id):
                    group_list.append(group_id["_id"])
                else:
                    continue
        return group_list

    # Related TO Finding Channel(s)
    async def find_chat(self, group_id: int):
        
        connections = self.cache.get(str(group_id))
        
        if connections is not None:
            return connections

        connections = await self.col.find_one({'_id': group_id})
        
        if connections:
            self.cache[str(group_id)] = connections

            return connections
        else: 
            return self.new_chat(None, None, None)

        
    async def add_chat(self, g_id: int, c_id: int, c_name):
        
        new = self.new_chat(g_id, c_id, c_name)
        update_d = {"$push" : {"chat_ids" : {"chat_id": c_id, "chat_name" : c_name}}}
        prev = await self.col.find_one({'_id':g_id})
        
        if prev:
            await self.col.update_one({'_id':g_id}, update_d)
            await self.update_active(g_id, c_id, c_name)
            await self.refresh_cache(g_id)
            
            return True
        
        self.cache[str(g_id)] = new
        
        await self.col.insert_one(new)
        await self.add_active(g_id, c_id, c_name)
        await self.refresh_cache(g_id)
        
        return True


    async def del_chat(self, g_id: int, c_id: int):
        
        g_id, c_id = int(g_id), int(c_id) # g_id and c_id Didnt type casted to int for some reason
        
        prev = self.col.find_one({"_id": g_id})
        
        if prev:
            
            await self.col.update_one(
                {"_id": g_id}, 
                    {"$pull" : 
                        {"chat_ids" : 
                            {"chat_id":
                                c_id
                            }
                        }
                    },
                False,
                True
            )

            await self.del_active(g_id, c_id)
            await self.refresh_cache(g_id)

            return True

        return False


    async def in_db(self, g_id: int, c_id: int):
        
        connections = self.cache.get(g_id)
        
        if connections is None:
            connections = await self.col.find_one({'_id': g_id})
        
        check_list = []
        
        if connections:
            for x in connections["chat_ids"]:
                check_list.append(int(x.get("chat_id")))

            if int(c_id) in check_list:
                return True
        
        return False


    async def update_settings(self, g_id: int, settings):
        
        g_id = int(g_id)
        prev = await self.col.find_one({"_id": g_id})
        
        if prev:
            try:
                await self.col.update_one({"_id": g_id}, {"$set": {"types": settings}})
                await self.refresh_cache(g_id)
                return True
            
            except Exception as e:
                print (e)
                return False
        print("You Should First Connect To A Chat To Use This")
        return False


    async def update_configs(self, g_id: int, configs):
        
        prev = await self.col.find_one({"_id": g_id})

        if prev:
            try:
                await self.col.update_one(prev, {"$set":{"configs": configs}})
                await self.refresh_cache(g_id)
                return True
            
            except Exception as e:
                print (e)
                return False
        print("You Should First Connect To A Chat To Use This")
        return False


    async def delete_all(self, g_id: int):
        
        prev = await self.col.find_one({"_id": g_id})
        if prev:
            await self.delall_active(g_id)
            await self.delall_filters(g_id)
            await self.del_main(g_id)
            await self.refresh_cache(g_id)
            
        return


    async def del_main(self, g_id: int):
        
        await self.col.delete_one({"_id": g_id})
        await self.refresh_cache(g_id)
        
        return True


    async def refresh_cache(self, g_id: int):
        if self.cache.get(str(g_id)):
            self.cache.pop(str(g_id))
        
        prev = await self.col.find_one({"_id": g_id})
        
        if prev:
            self.cache[str(g_id)] = prev
        return True

    # Related To Finding Active Channel(s)
    async def add_active(self, g_id: int, c_id: int, c_name):
        
        templ = {"_id": g_id, "chats":[{"chat_id": c_id, "chat_name": c_name}]}
        
        try:
            await self.acol.insert_one(templ)
            await self.refresh_acache(g_id)
        except Exception as e:
            print(e)
            return False
        
        return True


    async def del_active(self, g_id: int, c_id: int):
        
        templ = {"$pull": {"chats": dict(chat_id = c_id)}}
        
        try:
            await self.acol.update_one({"_id": g_id}, templ, False, True)
        except Exception as e:
            print(e)
            pass
        
        await self.refresh_acache(g_id)
        return True


    async def update_active(self, g_id: int, c_id: int, c_name):
        
        g_id, c_id = int(g_id), int(c_id)
        
        prev = await self.acol.find_one({"_id": g_id})
        templ = {"$push" : {"chats" : dict(chat_id = c_id, chat_name = c_name)}}
        in_c = await self.in_active(g_id, c_id)
        
        if prev:
            if not in_c:
                await self.acol.update_one({"_id": g_id}, templ)
            else:
                return False
        else:
            await self.add_active(g_id, c_id, c_name)
        return True


    async def find_active(self, g_id: int):
        
        if self.acache.get(str(g_id)):
            self.acache.get(str(g_id))
        
        connection = await self.acol.find_one({"_id": g_id})

        if connection:
            return connection
        return False


    async def in_active(self, g_id: int, c_id: int):
        
        prev = await self.acol.find_one({"_id": g_id})
        
        if prev:
            for x in prev["chats"]:
                if x["chat_id"] == c_id:
                    return True
            
            return False
        
        return False


    async def delall_active(self, g_id: int):
        
        await self.acol.delete_one({"_id":int(g_id)})
        await self.refresh_acache(g_id)
        return


    async def refresh_acache(self, g_id: int):
        if self.acache.get(str(g_id)):
            self.acache.pop(str(g_id))
        
        prev = await self.acol.find_one({"_id": g_id})
        
        if prev:
            self.acache[str(g_id)] = prev
        return True

    # Related To Finding Filter(s)
    async def add_filters(self, data):
        
        try:
            await self.fcol.insert_many(data)
        except Exception as e:
            print(e)
        
        return True


    async def del_filters(self, g_id: int, c_id: int):
        
        g_id, c_id = int(g_id), int(c_id)
        
        try:
            await self.fcol.delete_many({"chat_id": c_id, "group_id": g_id})
            print(await self.cf_count(g_id, c_id))
            return True
        except Exception as e:
            print(e) 
            return False


    async def delall_filters(self, g_id: int):
        
        await self.fcol.delete_many({"group_id": int(g_id)})
        return True


    async def get_filters(self, g_id: int, keyword: str):

        await self.create_index()

        achats = await self.find_active(g_id)
        
        achat_ids=[]
        if not achats:
            return False
        
        for chats in achats["chats"]:
            achat_ids.append(chats.get("chat_id"))
        
        filters = []

        pipeline= {
            "group_id": g_id, "$text":{"$search": keyword}
        }
        
        db_list = self.fcol.find(pipeline)

        for document in await db_list.to_list(length=600):
            
            if document["chat_id"] in achat_ids:
                filters.append(document)
            
            else:
                continue

        return filters


    async def cf_count(self, g_id: int, c_id: int):
        return await self.fcol.count_documents({"chat_id": c_id, "group_id": g_id})
    
    
    async def tf_count(self, group_id: int):
        return await self.fcol.count_documents({"group_id": group_id})


