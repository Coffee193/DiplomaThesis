import json

json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)


def IntToStrWithSlabInfornt(val):
    if(type(val) != str):
        val = '_' + str(val)
    return val

search = 'tasks'

user_question = "Return task with id 584"
retrieve_info = {"attribute": True,"key": "id","value": 584}
search_info = None

user_question = 'What are the ids of MELTING task'
retrieve_info = {"attribute": True,"key": "name","value": "MELTING", "think": "The user is searching for a specific job using an attribute and value. The keyword 'id' was found which matches one of the allowed keys."}
search_info = {"attribute": True, "return": "id"}

search = 'resources'

user_question = "Return resouce 1"
retrieve_info = {"attribute": True,"key": "id","value": 1}
search_info = {"attribute": False, "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

user_question = 'Return the name of resource 1'
retrieve_info = {"attribute": True,"key": "id","value": 1}
search_info = {"attribute": True, "return": "name", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

user_question = 'Return the id of MELTSHOP'
retrieve_info = {"attribute": True,"key": "name","value": "MELTSHOP"}
search_info = {"attribute": True, "return": "id", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

user_question = 'Return the availability of MELTSHOP'
retrieve_info = {"attribute": True,"key": "name","value": "MELTSHOP"}
search_info = {"attribute": True, "return": "period", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

#user_question = 'Return the arrivaldate of job _294'
#retrieve_info = {"attribute": True,"key": "id","value": "_294"}
#search_info = {"attribute": True, "return": "arrivaldate", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}
if(search == 'tasks'):
    query = json_data["tasks"]["task"]
elif(search == 'resources'):
    query = json_data["resources"]["resource"]

if(search == 'resources' or search == 'tasks'):
    if(retrieve_info['key'] == 'id'):
        query = [q for q in query if q[retrieve_info['key']] == IntToStrWithSlabInfornt(retrieve_info['value'])]
    elif(retrieve_info['key'] == 'name'):
        query = [q for q in query if q[retrieve_info['key']].upper() == retrieve_info['value'].upper()]


### Final Form ###
if(search == 'tasks'):
    query = [{'name': q['name'], 'id': q['id']} for q in query]
elif(search == 'resources'):
    query = [{'name': q['name'], 'nonworkingperiods': [{'fromdate': r['fromdate'], 'todate': r['todate']} for r in q['resourceavailability']['nonworkingperiods']['period']], 'id': q['id']} for q in query]
### ###

#####---
if search_info['attribute'] != False:
    if(search_info['return'] == 'name'):
        query = [{'id': q['id'], 'name': q['name']} for q in query]
    elif(search_info['return'] == 'id'):
        query = [{'id': q['id']} for q in query]
    elif(search_info['return'] == 'period'):
        query = [{'id': q['id'], 'nonworkingperiods': q['nonworkingperiods']} for q in query]

print('***')
print(query)
