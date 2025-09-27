import secrets
import string
import datetime
import pytz

length = 35
rand_str = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
rand_str = rand_str.replace('$', '=') + str(int(datetime.datetime.now(pytz.utc).timestamp() * 1000000))
print(rand_str)
print(str(int(datetime.datetime.now(pytz.utc).timestamp() * 1000000)))
'''
This script is used to generate the ADMIN_KEYS that are then copied pasted in the .env file
'''