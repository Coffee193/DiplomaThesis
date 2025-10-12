import time
import datetime
import requests
import json
import secrets
import string
from cryptography.hazmat.primitives.asymmetric import rsa, ec

print(time.time())
print(time.time_ns())
print(time.perf_counter())
print(time.process_time())
print('***')
print(time.time() * 1000)
#aa = '{0:042b}'.format()
#print() 
#print(aa)
#print(len(aa))
print('-------')
dt = datetime.datetime(2025, 10, 10, 0, 0, 0, tzinfo = datetime.timezone.utc)
print(dt)
print(dt.timestamp())

#res = requests.post('http://127.0.0.1:8000/loginregister/register/', json = {"val": "T#1}f=toP-"})
#print(res)
#print(res.json())

dateval = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
print(dateval)
print(type(dateval))
ts = dateval.timestamp()
print(ts)
print(type(ts))

print('^^^')
print(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20)))

print(secrets.token_hex(32)) # 32 hex characters = 128 bits
print(secrets.token_hex(64)) # 256 bits
print(secrets.token_bytes(256)) # 256 bytes
print('******')
print(len("MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBd8WKIJYpRbTuUlaSTYVXnsg4xOujbcaKW8ZTmA/bpf1hDhq+MzXImn/BAyGARIiDV7tQeK6Iuvla9FDMN3tu11nfr0VeizDE6xRVUg3RQe2lovU/ZBXy9z/becqiJJqZmZ7pjxrY89Cu9bF28at4rXS1Gh9yuAtc2sRo5ctvSlITmUkyEx7EROheX48L6ty+BEx58C9qY/GuPPgN5sCHholrcZcTfntZJAvMcvCCOxSMZz58jMQx+Swq7j+TQMJpwpiKuOqIu9Fy7jU6HbKDTia4/+HFOfIkF3SpkTY6QbXk7vCMI2dYEHXK4t92oHy83//3Ghgw+lZdE4yEU146PAgMBAAE="))