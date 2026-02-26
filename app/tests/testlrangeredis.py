import redis

rc = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

print(rc.lrange('ut_', 0, -1))
if('isad' not in rc.lrange('ut_', 0, -1)):
    print('BUBUBU')
if(rc.lrange('ut_', 0, -1) == []):
    print('GIGIGI')