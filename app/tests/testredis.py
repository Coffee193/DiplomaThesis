import redis

redis_client = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

print(redis_client.lrange('i', 0, -1))
print(redis_client.lrem('i', 1, 'ss'))
print(redis_client.lrange('i', 0, -1))
print('***')