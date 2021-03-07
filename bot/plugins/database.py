import motor.motor_asyncio
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
        self.db = self._client["Auto_Filter"]
        self.col = self.db["Chats"]

        self.cache = {}


    def new_connection(self, group_id, channel1, channel2, channel3):
        return dict(
          _id = group_id,
          channel_ids = dict(
            channel1=channel1, 
            channel2=channel2, 
            channel3=channel3
          )
        )
        
    async def find_connections(self, group_id):
        
        connections = self.cache.get(group_id)
        
        if connections is not None:
            return connections

        connections = await self.col.find_one({'_id':int(group_id)})
        
        if connections:
            self.cache[group_id] = connections
            return connections
        return False

        
    async def add_connections(self, group_id, channel1, channel2, channel3):
        
        group = self.new_connection(group_id, channel1, channel2, channel3)
        
        prev = await self.col.find_one({'_id':int(group_id)})
        
        if prev:
          await self.col.delete_one(prev)
          
        await self.col.insert_one(group)
        return True
        
    async def delete_connections(self, group_id):
        
        group_id = int(group_id)
        
        if self.cache.get(group_id):
            self.cache.pop(group_id)
        
        prev = self.col.find_one({"_id": int(group_id)})
        
        if prev:
           await self.col.delete_one({"_id": int(group_id)})
           return True
        return False
