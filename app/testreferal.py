import requests
import json

#{"id": 237346999496364032}
# T#1}f=toP-
#res = requests.post('http://127.0.0.1:8000/referal/test/', json = {"id": 237346999496364032})
res = requests.post('http://127.0.0.1:8000/referal/test/', json = {"val": "T#1}f=toP-"})
print(res)