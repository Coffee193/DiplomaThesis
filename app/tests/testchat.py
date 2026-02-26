import requests
import json

#{"id": 237346999496364032}
# T#1}f=toP-
#res = requests.post('http://127.0.0.1:8000/referal/test/', json = {"id": 237346999496364032})
#res = requests.post('http://127.0.0.1:8000/referal/test/', json = {"val": "T#1}f=toP-"})
res = requests.get('http://127.0.0.1:8000/chats/test/', json={"id": 1})
print(res) # 0 NOT FOUND |||||| OR 1 WHEN FOUND
print(type(res)) # int
