import redis

redis_client = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

redis_client.hset("bu", mapping={"vuvu": 32, "lalo": 'pop'})

aa = redis_client.hgetall("bu")
print(aa)
print(type(aa))

redis_client.delete("bu")
print(redis_client.hgetall("bu"))