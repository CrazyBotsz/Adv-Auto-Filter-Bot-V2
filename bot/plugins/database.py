import pymongo
from bot import DB_URI # pylint: disable=import-error

myclient = pymongo.MongoClient(DB_URI) # TODO: Rewrite To Motor🙁
mydb = myclient["Auto_Filter"]
CHATS = mydb["Chats"]

a = {}

def add_connections(group: int, channel1: int, channel2: int, channel3: int):
    a["_id"] = group
    
    prev = CHATS.find_one(a)
    a["channel_ids"] = {
        "channel1": channel1,
        "channel2": channel2,
        "channel3": channel3
    }
    
    print(a)
    if prev:
        CHATS.delete_one(prev) # pylint: disable=no-value-for-parameter
        
    CHATS.insert_one(a)
    return True

def find_connections(group: int):
    a["_id"] = group
    
    connections = CHATS.find_one(a)
    
    if connections:
        return connections
    return False

def delete_connections(group: int):
    a["_id"] = group
    
    prev = CHATS.find_one(a)
    
    if prev:
        CHATS.delete_one(a)
        return True
    return False
