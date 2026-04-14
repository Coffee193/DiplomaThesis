import json

json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)
query = json_data["taskprecedenceconstraints"]["taskprecedenceconstraint"]

def IntToStrWithSlabInfornt(val):
    if(type(val) != str):
        val = '_' + str(val)
    return val

user_question = 'Does task 584 need to be executed before 585?'
retrieve_info = {  "attribute": True,  "before": 584,  "after": 585,  "think": "The question is asking about the execution order of tasks, specifically whether task 584 must be executed before task 585."}

user_question = 'Does task 584 need to be executed after 585?'
retrieve_info = {  "attribute": True,  "before": 585,  "after": 584,  "think": "The question is asking about the execution order of tasks, specifically whether task 584 must be executed before task 585."}

user_question = "Is there a task to be executed before task with id 483?"
retrieve_info = {  "attribute": True,  "before": "*",  "after": 483,  "think": "The user is asking about the relationship between tasks based on their IDs. The question mentions 'task with id 483', which implies a specific task ID. However, there's no explicit mention of an ID that must be executed before task 483, so I assume it's any task."}

user_question = "Is there a task to be executed before task with id 584?"
retrieve_info = {  "attribute": True,  "before": "*",  "after": 584,  "think": "The user is asking about the relationship between tasks based on their IDs. The question mentions 'task with id 483', which implies a specific task ID. However, there's no explicit mention of an ID that must be executed before task 483, so I assume it's any task."}

user_question = 'What task can i execute after completing task 585?'
retrieve_info = {  "attribute": True,  "before": 585,  "after": "*",  "think": "Identified a query about execution order and specific task IDs. Extracted the ID of the task that needs to be executed before another task, which is '57'. Since the user asked for a task to execute after completing task 57, used '*' as the task ID for the after relationship."}

user_question = 'Does task 578 require another task to be executed beforehand?'
retrieve_info = {"attribute": True, "before": "*", "after": 578, "think": "The user is asking about the relationship between task IDs, specifically whether task 92 requires another task to be executed before it. The question wording indicates a 'before' relationship, so I've prioritized extracting this information."}

user_question = 'Return the names of all tasks that have to be executed after task 579'
retrieve_info = {  "attribute": True,  "before": 579,  "after": "*",  "think": "Identified a specific task ID (85) and inferred a relationship with other tasks. The user is asking for tasks that must be executed after task 85, implying a 'before' condition on task 85 itself."}

#########################

user_question = 'Is task 579 independent of other tasks?'
retrieve_info = {"attribute": True, "reference": 579, "target": "*", "think": "The user is asking about task dependencies using one or more task IDs, specifically the task with ID 13, and refers to any other task."}

user_question = "Is task 535 independent of task 901" # 535/901, 3/3 times #
retrieve_info =  {  "attribute": True,  "reference": 579,  "target": 901,  "think": "The user is asking about the dependencies between two specific tasks, so I'm assuming they're looking for a dependency relationship between these tasks."}

user_question = "Is task 535 independent of task 578" # 535/901, 3/3 times #
retrieve_info =  {  "attribute": True,  "reference": 579,  "target": 578,  "think": "The user is asking about the dependencies between two specific tasks, so I'm assuming they're looking for a dependency relationship between these tasks."}

user_question = 'Does task 578 has to be executed before or after task 579'
retrieve_info = {    "attribute": True,    "reference": 578,    "target": 579,    "think": "The user is asking about the dependency between two specific tasks, so I extracted their IDs."}

user_question = 'Does task 71 depend on other tasks?'
retrieve_info = {  "attribute": True,  "reference": 71,  "target": "*",  "think": "The user is asking about the dependencies of a specific task (task 71) in relation to other tasks, indicated by 'other tasks'."}

user_question = 'Does task 578 depend on other tasks?'
retrieve_info = {  "attribute": True,  "reference": 578,  "target": "*",  "think": "The user is asking about the dependencies of a specific task (task 71) in relation to other tasks, indicated by 'other tasks'."}

user_question = 'Does task 578 need to be executed before or after task 90?'
retrieve_info = {  "attribute": True,  "reference": 578,  "target": 90,  "think": "The user is asking about the dependencies of task 72 in relation to another specific task, which is task 90."}


if("before" in retrieve_info):
    if(retrieve_info["before"] != "*"):
        query = [q for q in query if q['preconditiontaskreference']['refid'] == IntToStrWithSlabInfornt(retrieve_info["before"])]
    if(retrieve_info["after"] != "*"):
        query = [q for q in query if q['postconditiontaskreference']['refid'] == IntToStrWithSlabInfornt(retrieve_info["after"])]

else:
    if(retrieve_info['target'] == "*"):
        query = [q for q in query if IntToStrWithSlabInfornt(retrieve_info['reference']) in (q['preconditiontaskreference']['refid'], q['postconditiontaskreference']['refid'])]
    else:
        query = [q for q in query if {q['preconditiontaskreference']['refid'], q['postconditiontaskreference']['refid']} == {IntToStrWithSlabInfornt(retrieve_info['reference']), IntToStrWithSlabInfornt(retrieve_info['target'])}]

### Final Form ###
query = [{'before': q['preconditiontaskreference']['refid'], 'next': q['postconditiontaskreference']['refid']} for q in query]
### ###

print(query)