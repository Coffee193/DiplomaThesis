import json

json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)
query = json_data["jobs"]["job"]

def IntToStrWithSlabInfornt(val):
    if(type(val) != str):
        val = '_' + str(val)
    return val

search = 'jobs'

user_question = 'Return all jobs that require task 574'
retrieve_info = {"attribute": True,"key": "task","value": 574}
search_info = None

user_question = "List jobs with id _294" 
retrieve_info = {"attribute": True,"key": "id","value": "_294", "think": "The user is searching for a specific job using an attribute and value. The keyword 'id' was found which matches one of the allowed keys."}
search_info = None

user_question = 'Return the name of job _294'
retrieve_info = {"attribute": True,"key": "id","value": "_294"}
search_info = {"attribute": True, "return": "name", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

user_question = 'Return the duedate of job _294'
retrieve_info = {"attribute": True,"key": "id","value": "_294"}
search_info = {"attribute": True, "return": "duedate", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

user_question = 'Return the arrivaldate of job _294'
retrieve_info = {"attribute": True,"key": "id","value": "_294"}
search_info = {"attribute": True, "return": "arrivaldate", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}

if(search == 'jobs'):
    if(retrieve_info['key'] == 'id'):
        query = [q for q in query if q[retrieve_info['key']] == IntToStrWithSlabInfornt(retrieve_info['value'])]
    elif(retrieve_info['key'] == 'name'):
        query = [q for q in query if q[retrieve_info['key']].upper() == retrieve_info['value'].upper()]
    elif(retrieve_info['key'] == 'task'):
        query = [q for q in query if any(t.get('refid') == IntToStrWithSlabInfornt(retrieve_info['value']) for t in q.get('jobtaskreference', []))]
    elif(retrieve_info['key'] == 'arrivaldate' or retrieve_info['key'] == 'duedate'):
        retrieve_info['value'] = json.loads(chat('llama3.1', messages = [{'role': 'user', 'content': _a0_test_ollama_str_to_date.getPrompt(retrieve_info['value'])}]).message.content)
        query = [q for q in query if ( q[retrieve_info['key']]['day'] == retrieve_info['value']['day'] and q[retrieve_info['key']]['month'] == retrieve_info['value']['month'])]

print(query)

### Final Form ###
query = [{'name': q['name'], 'arrivaldate': q['arrivaldate'], 'duedate': q['duedate'], 'tasks': [r['refid'] for r in q['jobtaskreference']], 'workcenter': q['jobworkcenterreference']['refid'], 'id': q['id']} for q in query]
### ###

#####---
if search_info['attribute'] != False:
    if(search_info['return'] == 'name'):
        query = [{'id': q['id'], 'name': q['name']} for q in query]
    elif(search_info['return'] == 'id'):
        query = [{'id': q['id']} for q in query]
    elif(search_info['return'] == 'task'):
        query = [{'id': q['id'], 'tasks': q['tasks']} for q in query]
    elif(search_info['return'] == 'arrivaldate'):
        query = [{'id': q['id'], 'arrivaldate': q['arrivaldate']} for q in query]
    elif(search_info['return'] == 'duedate'):
        query = [{'id': q['id'], 'duedate': q['duedate']} for q in query]

print('***')
print(query)

