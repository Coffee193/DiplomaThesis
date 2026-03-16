import pymongo

replica_conn = ['localhost:27017']

mongo_client = pymongo.MongoClient(replica_conn[0], serverSelectionTimeoutMS = 15000, waitQueueTimeoutMS = 5000)
mongo_db = mongo_client['Sapling']

chats = mongo_db['Chats']

chat_ret = chats.find_one({"_id": 295662116193193984, "user_id": 1}, {"_id": 0, "chat.q": 1, "chat.a": 1, "chat.d": 1})
print(chat_ret)