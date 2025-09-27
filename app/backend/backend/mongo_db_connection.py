import pymongo

replica_conn = ['localhost:27017']

mongo_clinet = pymongo.MongoClient(replica_conn[0], serverSelectionTimeoutMS = 15000, waitQueueTimeoutMS = 5000)
mongo_db = mongo_clinet['Sapling']

chats = mongo_db['Chats']