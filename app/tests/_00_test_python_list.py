import json

json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)

query = json_data["resources"]["resource"]
print([q for q in query if q['id'] == '_1'])

print('aaa===')
print(json.dumps({"attribute": True,"key": "id","value": 509,"think": "The user is searching for a specific job using its id"}))
aa = json.loads('{"attribute": true,"key": "id","value": 509,"think": "The user is searching for a specific job using its id"}')