import redis
import json

redis_client = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

val = json.dumps({"q": "lalala", "d": {"n": "vuvo", "p": "koko.xml", "s": "234"}})
redis_client.set("bu", val)

ra = redis_client.get("bu")
print(ra)
print(type(ra)) # str

print('***')
ra = json.loads(ra)
print(ra)
print(type(ra))

po = redis_client.get('jiasjdoi')
print(po)
print(type(po))