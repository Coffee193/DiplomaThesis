import json

json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)
query = json_data["tasksuitableresources"]["tasksuitableresource"]

def IntToStrWithSlabInfornt(val):
    if(type(val) != str):
        val = '_' + str(val)
    return val

search = 'resource'

user_question = 'Which tasks can be done in resource 2?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "id", "value": 2}, "search": {"info": "task"}, "think": "The user is asking for tasks that can be executed by a specific resource with id 2. This requires extracting the resource's id and matching it to task resources."}

user_question = 'Can the MELTSHOP execute Task 584?'
retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "name", "value": "MELTSHOP"}

#user_question = 'Return all resource ids that can execute Task 584?'
#retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
#search_info = {"attribute": True, "key": "id"}

#user_question = 'Can the ROLLING MILL execute Task 584?'
#retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
#search_info = {"attribute": True, "key": "name", "value": "ROLLING MILL"}

#user_question = 'Return all resource names that can execute Task 584?'
#retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
#search_info = {"attribute": True, "key": "name"}

user_question = 'Can resource 1 execute Task 584?'
retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "id", "value": 1}

user_question = 'Can resource 2 execute Task 584?'
retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "id", "value": 2}

user_question = 'Return the working period of the resource that can execute Task 584?'
retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "period"}

user_question = 'Return all resource that can execute Task 584?'
retrieve_info = {"attribute": True, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = None

search = 'task'

user_question = 'Return all taks that can be executed in resource 2?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "id", "value": 2}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = None

user_question = 'Which tasks be executed in the MELTSHOP?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = None

user_question = 'Return all task ids that can be executed in resource _1'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "id", "value": "_1"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "id"}

user_question = 'Return all task names that can be executed in resource _2'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "id", "value": "_2"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "name"}

user_question = 'Return the operation times of all tasks that can be executed in the ROLLING MILL'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "name", "value": "ROLLING MILL"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "time"}

###

user_question = 'Can Task 585 be executed in the MELTSHOP?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "id", "value": 585}

user_question = 'Can Task 584 be executed in the MELTSHOP?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "id", "value": 584}

user_question = 'Can ROLLING Tasks be executed in the MELTSHOP?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "name", "value": "ROLLING"}

user_question = 'Can Melting Tasks be executed in the MELTSHOP?'
retrieve_info = {"attribute": True, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
search_info = {"attribute": True, "key": "name", "value": "Melting"}

# {"attribute": <bool>, "know": {"info": <str>, "key": <str>, "value": <str, int>}, "search": {"info": <str>}, "think": <str>}
# know -> info: resource, task #<---NOTE: ALTHOUGH NOT INSTRUCTED TO IT MIGHT PUT: time IF QUESTION SHOULD BE TIME!!!
# key: id, name
# search -> info: resource, task, time
val_get = None
if(retrieve_info['know']['key'] == 'name'):
    val_get = [d['id'] for d in json_data[retrieve_info['know']['info'] + 's'][retrieve_info['know']['info']] if d['name'].upper() == retrieve_info['know']['value'].upper()]
### Above gets the ids, now use these to get the value.
### NOTE: above retrieves a list. value might be list or str
if(val_get != None):
    query = [q for q in query if q[retrieve_info['know']['info'] + 'reference']['refid'] in val_get] # Fix this <---
else:
    query = [q for q in query if q[retrieve_info['know']['info'] + 'reference']['refid'] == IntToStrWithSlabInfornt(retrieve_info['know']['value'])]


### Info Final Form ###
fin_list = []
for i in range(0, len(query)):
    if(len(fin_list) == 0 or (not any(fl['resource']['id'] == query[i]['resourcereference']['refid'] for fl in fin_list)) ):
        fin_list.append({'resource': {'id': query[i]['resourcereference']['refid'], 'name': [r['name'] for r in json_data['resources']['resource'] if r['id'] == query[i]['resourcereference']['refid']][0]}, 'tasks': [{'id': query[i]['taskreference']['refid'], 'operation_time': query[i]['operationtimeperbatchinseconds'], 'name': [t['name'] for t in json_data['tasks']['task'] if t['id'] == query[i]['taskreference']['refid']][0]}]})
    else:
        next(item for item in fin_list if item['resource']['id'] == query[i]['resourcereference']['refid'])['tasks'].append({'id': query[i]['taskreference']['refid'], 'operation_time': query[i]['operationtimeperbatchinseconds'], 'name': [t['name'] for t in json_data['tasks']['task'] if t['id'] == query[i]['taskreference']['refid']][0]})
### ###

if search_info != None:
    if search == 'resource':
        if 'value' not in search_info:
            if search_info['key'] == 'id':
                for item in fin_list: item['resource'] = {'id': item['resource']['id']}
            elif search_info['key'] == 'period':
                for item in fin_list: item['resource']['no_work_period'] = [rp['resourceavailability']['nonworkingperiods']['period'] for rp in json_data['resources']['resource'] if rp['id'] == item['resource']['id']][0]
        
        else:
            search_info['value'] = IntToStrWithSlabInfornt(search_info['value'])
            fin_list = [item for item in fin_list if item['resource'][search_info['key']].upper() == search_info['value'].upper()]
    
    elif search == 'task':
        if 'value' not in search_info:
            if search_info['key'] == 'id':
                for item in fin_list: item['tasks'] = [{'id': t['id']} for t in item['tasks']]
            elif search_info['key'] == 'name':
                for item in fin_list: item['tasks'] = [{'id': t['id'], 'name': t['name']} for t in item['tasks']]
            elif search_info['key'] == 'time':
                for item in fin_list: item['tasks'] = [{'id': t['id'], 'operation_time': t['operation_time']} for t in item['tasks']]
        else:
            search_info['value'] = IntToStrWithSlabInfornt(search_info['value'])
            fin_list = [{'resource': item['resource'], 'tasks': [t for t in item['tasks'] if t[search_info['key']].upper() == search_info['value'].upper()]}  for item in fin_list if any(t[search_info['key']].upper() == search_info['value'].upper() for t in item['tasks'])]

print(query)
print('****')
print(fin_list)