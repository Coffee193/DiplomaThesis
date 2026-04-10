#from _1_test_ollamaclassifier import ClassifyRootSearch
import _1_0_test_ollamaclassifier_new_gibberish_asfunc
import _1_test_ollamaclassifier_new_list_rewrite_moreshots_asfunc
import _1_2_test_ollamaclassifier_tasks_asfunc
import _3_5_test_ollamaclassifier_attr_resource
import _3_1_test_ollamaclassifier_attr_job
import _3_2_test_ollamaclassifier_attr_task
import _3_3_test_ollamaclassifier_attr_tasksuitableresource
import _3_4_test_ollamaclassifier_attr_taskprepost
import _x0_test_ollama_error_chain_1_prompt
import _a0_test_ollama_str_to_date
import _5_test_answer_question_job

from ollama import chat
import ollama
import json
import re
from datetime import datetime

from transformers import AutoTokenizer

# user_question = '22'
# user_question = 'Return the ids of all tasks' <--- Problem!!!
user_question = 'Return all tasks'
user_question = 'Return the names of every job' # <--- he correctly finds this though
# user_question = 'Return all resources' # tokens: 9557
# user_question = 'Return all jobs' # tokens: 1217
# user_question = 'Return all tasks' # tokens: 416
# user_question = 'Return all tasks and resources' # tokens: 1315
# user_question = 'Return all task time dependencies' # tokens: 397

## Jobs ##
user_question = "List all jobs"
#user_question = "Return the job with arrival date 31/3" # [] (len: 0), {'pick': 3}, {'attribute': True, 'key': 'arrivaldate', 'value': {'day': 31, 'month': 3}, 'think': "The user is searching for a specific job by its arrival date, which matches one of the allowed attributes. The value '31/3' could be interpreted as either a date or a string. I will assume it's a string to match the format specified in the job dictionary."}
#user_question = "List all jobs" # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': "The user did not specify any particular attribute or value, so it's likely they want to retrieve all jobs."}
#user_question = "Give me the jobs" # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': 'The user is asking for a general list of jobs without specifying any attribute or value, so no specific job is being referenced.'}
#user_question = "Return the job with id 8" # [] (len: 0), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 8, 'think': "The user is searching for a specific job using its id. The keyword 'id' was mentioned, and it matches one of the allowed attributes."}
#user_question = "Return the job with id 300" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 300, 'think': "The user is asking for a specific job by its id. I found the word 'id' and the value associated to it."}
#user_question = "Return the job with id _300" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': '_300', 'think': "The user is searching for a specific job by its id, which was mentioned as '_300'."}
#user_question = "Are there any jobs with arrival date 31 2" # [] (len: 0), {'pick': 3}, {'attribute': True, 'key': 'arrivaldate', 'value': {'day': 31, 'month': 2}, 'think': "The user is searching for a specific job based on its arrival date, which is mentioned as '31 2'"}
#user_question = "List jobs with id 295" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 295, 'think': 'The user is asking for a specific job by its id, which matches one of the allowed attributes.'}
#user_question = "Find jobs that require task 581" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'task', 'value': 581, 'think': 'The user is searching for jobs based on a specific task ID.'}
#user_question = "Find jobs that require task with id 581" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'task', 'value': 581, 'think': "The user is searching for jobs based on a specific attribute 'task' and value '581', which indicates they are looking for jobs related to a particular task."}
#user_question = "Find the last job that requires task with id 581" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'task', 'value': 581}
#user_question = "Return the first job" # [...] (len: 1), {'pick': 3}, {'attribute': False, 'think': 'The user did not specify a particular attribute or value. It seems they are asking for the first job, but without specifying how to identify it (e.g., by id, name), I cannot determine which key and value to extract.'}
#user_question = "Return the job at index 5" # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': "The user is asking for a job by its index, but there's no information about the job itself. This could be referring to any job or none, so I'm assuming it's not a specific job."}
#user_question = "Return the first job that requires the task with id 580" # [...] (len: 1), {'pick': 3}, [{'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_580'}, {'refid': '_581'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_297'}]
#user_question = "Return job 5" #<---implies id here # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 5, 'think': 'The user is asking for a specific job by its id, which matches one of the allowed attributes (id).'}
#user_question = "Return 4 jobs" # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': 'The question does not specify a particular attribute or job. It is asking for all jobs without any specific criteria.'}
#user_question = "Return me the FROM BILLET job" #<---understand theres name here # [...] (len: 9), {'pick': 3}, {'attribute': True, 'key': 'name', 'value': 'FROM BILLET', 'think': "The user is searching for a specific job by its name, so I extracted the key 'name' and its corresponding value 'FROM BILLET'. The mention of 'job' in the question confirms that it's looking for a specific job."}
#user_question = 'Return the job with id 509' # [] (len: 0), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 509, 'think': 'The user is searching for a specific job using its id attribute'}
#user_question = 'Return all jobs with name: from billet' # [...] (len: 9), {'pick': 3}, {'attribute': True, 'key': 'name', 'value': 'from billet', 'think': "The user is searching for a specific job by its name. The keyword 'name' was found in the question, along with the value 'from billet', which matches one of the attributes."}
#user_question = 'Return all jobs with arrivaldate 31 3' # [] (len: 0), {'pick': 3}, {'attribute': True, 'key': 'arrivaldate', 'value': {'day': 31, 'month': 3}, 'think': 'The user is searching for jobs based on a specific attribute (arrivaldate) and value (31 3)'}
#user_question = 'Return all jobs with due date 31 march' # [...] (len: 9), {'pick': 3}, {'attribute': True, 'key': 'duedate', 'value': {'day': 31, 'month': 3}}
#user_question = 'Return all jobs that require task 574' # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'task', 'value': 574, 'think': 'The user is searching for a specific job by its task attribute. The value mentioned is 574, which is likely the id of a task.'}
#user_question = 'Return job 299' # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 299, 'think': "The user is asking for a specific job by its id, which is mentioned as 'job 299'"}
#user_question = 'Return 299 job' # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 299, 'think': "The user is asking for a specific job by its id. The word 'job' at the end suggests it's an id rather than any other attribute."}
#user_question = 'Return 299 jobs'  # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': 'The user is requesting a quantity of jobs without specifying any attribute.'}

### Tasks ###
#user_question = "Return task with id 584" # [...] (len: 1), {'pick': 4}, {'attribute': True, 'key': 'id', 'value': 584, 'think': "The user is searching for a specific task using its id as an attribute. The keyword 'id' was mentioned in the question along with the value '584', so I extracted the key and value accordingly."}
#user_question = "task with name Rolling" # [...] (len: 8), {'pick': 4}, {'attribute': True, 'key': 'name', 'value': 'Rolling'}
#user_question = "Return first task with name Rolling" # [...] (len: 8), {'pick': 4}, {'attribute': True, 'key': 'name', 'value': 'Rolling', 'think': "The question mentions 'name' and a specific value 'Rolling', which indicates that the user is searching for a task identified by its name."}
#user_question = "Return first task" # [...] (len: 18), {'pick': 4}, {'attribute': False, 'think': 'The user is asking to return all tasks or a specific task, but no attribute (id, name) is specified'}
#user_question = "tasks" # [...] (len: 18), {'pick': 4}, {'attribute': False, 'think': "The user's question is asking for tasks without specifying any attribute or value, so I assume it's a request to return all tasks."}
#user_question = "return task 7" # <--- recognises it as id # [] (len: 0), {'pick': 4}, {'attribute': True, 'key': 'id', 'value': 7, 'think': "The user is searching for a specific task using an attribute and value (id). The key extracted is 'id' and the value is 7."}
#user_question = "return 7 task" # <--- PROBLEMATIC
#user_question = "return 7 tasks" # [...] (len: 18), {'pick': 4}, {'attribute': False, 'think': "The question does not specify a particular task by attribute, so I assume it's asking for all tasks without filtering."}
#user_question = "return the last task" # [...] (len: 18), {'pick': 4}, {'attribute': False, 'think': "The question does not specify a particular attribute or value. It is likely asking for all tasks or the most recent task, but it's ambiguous and no specific key (id or name) was mentioned."}
#user_question = 'Return all ROLLING tasks' # [...] (len: 8), {'pick': 4}, {'attribute': True, 'key': 'name', 'value': 'ROLLING', 'think': "The question refers to a specific task by attribute, specifically looking for tasks with name 'ROLLING'"}
#user_question = 'Return the id of all tasks with name ROLLING' # [...] (len: 8), {'pick': 4}, {'attribute': True, 'key': 'name', 'value': 'ROLLING'}
#user_question = 'What is the name of the task with id 77' # [] (len: 0), {'pick': 4}, {"attribute": true,"key": "id","value": 77,"think": "The user is searching for a specific task by 'id' attribute, which matches one of the allowed keys. The value provided (77) will be used to identify the task."
## user_question = 'What are the ids of MELTING' # {"attribute": true,"key": "name","value": "MELTING", "think": "The user is searching for a specific task using its name, which is provided as 'MELTING'."}
#user_question = 'Return all tasks' # [...] (len: 18), {'pick': 4}, {'attribute': False, 'think': 'The user question does not specify a particular attribute or task to search for. It is asking to return all tasks without specifying any conditions.'}
#user_question = 'Return the name of every task' # [...] (len: 18), {'pick': 4}, {'attribute': False, 'think': 'The user is requesting information about all tasks without specifying a particular attribute or value.'}

### Resources ###
#user_question = "Return all resources" # [...] (len: 2), {'pick': 2}, {'attribute': False, 'think': "The question 'Return all resources' does not specify any particular attribute or value to search for a specific resource."}
#user_question = "Return all resource ids" # [...] (len: 2), {'pick': 2}, {'attribute': False, 'think': "The question does not specify a particular attribute or value, so it's likely asking for all resources and their ids. However, since the user is asking specifically for 'resource ids' without any other information, I'm assuming they don't want to filter by a specific id or name."}
#user_question = "Return resouce 2" #<-- classified as id=2 # [...] (len: 1), {'pick': 2}, {'attribute': True, 'key': 'id', 'value': 2, 'think': 'The question asks for a specific resource with id 2, assuming the user wants to return this resource by its numerical identifier.'}
#user_question = "What is the name of the resource with id 3" # [] (len: 0), {'pick': 2}, {'attribute': True, 'key': 'id', 'value': 3, 'think': "The user is asking for a specific resource identified by its 'name' attribute. However, instead of mentioning 'name', the user asks 'the name of the resource'. The key phrase that gives away the intent is 'with id 3', indicating that the user is referring to an attribute of the resource. Therefore, I extracted the key as 'id'."}
#user_question = "Return resource with id 7" # [] (len: 0), {'pick': 2}, {'attribute': True, 'key': 'id', 'value': 7, 'think': 'The user is searching for a specific resource using its id, which is mentioned as 7.'}
#user_question = "Return resource ROLLING MILL" # [...] (len: 1), {'pick': 2}, {'attribute': True, 'key': 'name', 'value': 'ROLLING MILL', 'think': "The user is searching for a specific resource by name. The keyword 'ROLLING MILL' suggests that it's the value of the 'name' attribute."}
#user_question = "Return resource rolling mill" # [...] (len: 1), {'pick': 2}, {'attribute': True, 'key': 'name', 'value': 'rolling mill'}
#user_question = "How many resources are there" # [...] (len: 2), {'pick': 2}, {'attribute': False, 'think': 'The user question does not specify a particular attribute of a resource, so I assume they want to know the total count of resources.'}
#user_question = "Return the first resource" # [...] (len: 2), {'pick': 2}, {'attribute': False, 'think': 'The user is requesting to return all resources or a general list without specifying any attribute or value. It does not seem like they are searching for a specific resource by id or name.'}
#user_question = "Return 1 resource" # [...] (len: 2), {'pick': 2}, {'attribute': False, 'think': "The question asks to return one resource without specifying any attribute or value, so it's a general request and not a specific search by attribute."}
#user_question = "Return 1 resources" # [...] (len: 2), {'pick': 2}, {'attribute': True, 'key': 'id', 'value': 1, 'think': "The user asked for a resource with id '1'"}

### TASKSUITABLERESOURCES ###
#user_question = 'Which tasks can be done in resource 901?' # [] (len: 0), {'pick': 5}, {'attribute': True, 'know': {'info': 'resource', 'key': 'id', 'value': 901}, 'search': {'info': 'task'}, 'think': "The question is about a specific task completion time, the user has provided a resource id which is a numeric value, therefore the attribute is set to true and 'resource' info is extracted with key 'id' and value 901. The search info is for tasks."}
user_question = 'Which tasks can be done in resource 2?' # [...] (len: 9), {'pick': 5}, {'attribute': True, 'know': {'info': 'resource', 'key': 'id', 'value': 2}, 'search': {'info': 'task'}, 'think': "Identified specific attribute 'resource id' and extracted reference point 'resource 2'. Now searching for tasks related to this resource."}
#user_question = 'Which tasks can be done in resource 1?' # [...] (len: 9), {'pick': 5}, {'attribute': True, 'know': {'info': 'resource', 'key': 'id', 'value': 1}, 'search': {'info': 'task'}, 'think': "The user is asking for tasks that can be done in a specific resource with id 1, which implies they already know the resource's id and are searching for related tasks."}
#user_question = 'Where can task 57 be executed' # [] (len: 0), {'pick': 5}, {"attribute": true, "know": {"info": "task", "key": "id", "value": 57}, "search": {"info": "resource"}, "think": "The user is looking for the resource where a specific task (task id 57) can be executed."}
#user_question = 'Where can task 584 be executed' # [...] (len: 1), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 584}, 'search': {'info': 'resource'}, 'think': 'Identified specific attribute (task id) and extracted reference point (task 584), now need to search for resources where this task can be executed'}
#user_question = 'Which resource can execute task with id 39?' # [] (len: 0), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 39}, 'search': {'info': 'resource'}, 'think': 'Identified a specific task ID, now looking for resources that match this condition'}
#user_question = 'Which resource can execute task 584?' # [...] (len: 1), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 584}, 'search': {'info': 'resource'}, 'think': 'The user is asking for a specific resource that can execute a task with id 584.'}
#user_question = 'Can Task 11 be executed in the MELTSHOP?' # [] (len: 0), {'pick': 5}, {"attribute": true, "know": {"info": "task", "key": "id", "value": 11}, "search": {"info": "resource"}, "think": "The user is asking for information about a specific resource that can execute a task with id 11. The user knows the task id and is searching for the corresponding resource."}
#user_question = 'How long does task 584 take?' # [...] (len: 1), {'pick': 5}, {"attribute": true, "know": {"info": "task", "key": "id", "value": 584}, "search": {"info": "time"}, "think": "The user is asking for the time it takes to complete a specific task. The task id is known and used as reference point."}
#user_question = 'What resource can execute each task?' # <-- No thinking # [...] (len: 18), {'pick': 5}, {"attribute": false}
#user_question = 'Return all resources and tasks' # <-- No thinking # [...] (len: 18), {'pick': 5}, {'attribute': False}
#user_question = 'Return all resources and their tasks' # [...] (len: 18), {'pick': 5}, {'attribute': False}
#user_question = 'Return the id of the resource that can execute task 585' # [...] (len: 1), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 585}, 'search': {'info': 'resource'}, 'think': "The user is asking for the id of a resource that can execute a specific task. The task id (585) is known, but not the resource's id or any other attribute."}
#user_question = 'What task can be executed in the ROLLING MILL' # [...] (len: 9), {'pick': 5}, {'attribute': True, 'know': {'info': 'resource', 'key': 'name', 'value': 'ROLLING MILL'}, 'search': {'info': 'task'}, 'think': 'Identified a specific resource name (ROLLING MILL) and searched for related tasks'}     
#user_question = 'Return the ids of all resources and tasks' # [...] (len: 18), {'pick': 5}, {'attribute': False, 'think': 'The user wants a general information without specifying any specific attribute or reference point'}
#user_question = 'Return all resources where task 587 can be executed' # [...] (len: 1), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 587}, 'search': {'info': 'resource'}, 'think': 'The user is asking for a specific task (587) and wants to find resources where this task can be executed'}
#user_question = 'Return the id of every resource where task 587 can be executed' # [...] (len: 1), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 587}, 'search': {'info': 'resource'}, 'think': "The user is asking for resources that support a specific task, and they already know the task's ID. This will likely involve querying resources associated with the given task."}
#user_question = 'What is the operation time for task 587' # [...] (len: 1), {'pick': 5}, {'attribute': True, 'know': {'info': 'task', 'key': 'id', 'value': 587}, 'search': {'info': 'time'}, 'think': 'The user asked about a specific attribute (task id) and wants to find the operation time for it'}
## user_question = 'What tasks need to operate for more than 30minutes?' # {"attribute": true, "know": {"info": "time", "key": "value", "value": 30}, "search": {"info": "task"}, "think": ["Identified specific attribute: time", "Extracted known attribute value: 30 minutes", "Determined user wants to find tasks"] }

### Taskprecedenceconstraints ###
#user_question = "Is there a task to be executed before task with id 483?" # [] (len: 0), {'pick': 6}, {"attribute": true, "id": 483, "order": "before", "think": "Identified specific task by its id. Analyzed question for intent and determined it's asking about tasks that must be executed before the given task."}
#user_question = "Is there a task to be executed before task with id 584?" # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 584, 'order': 'before', 'think': "Identified specific task by its id. Analyzing question wording, detected intent as 'before'"}
#user_question = "Is there a task to be executed before task 580?" # [] (len: 0), {'pick': 6}, {'attribute': True, 'id': 580, 'order': 'before', 'think': "The user is asking about tasks that must be executed before the given task, specifically task 580. The intent of the question can be detected from the wording 'before'."}
#user_question = "Is there a task to be executed before task 581?" # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 581, 'order': 'before', 'think': "Identified specific task by id. Determined intent as 'before' based on wording 'before task'."}
#user_question = "Is there a task to be executed before 581?" # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 581, 'order': 'before', 'think': ['Identified specific task id in the question', "Detected 'before' intent from the wording of the question"]}
#user_question = 'Which task should i execute before task 581?' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 581, 'order': 'before', 'think': ['Identified specific task id in the question', "Detected 'before' intent from the wording of the question"]}
#user_question = 'What task can i execute after completing task 591?' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 591, 'order': 'after', 'think': 'The user is asking about a specific task id and the intent is to find tasks that can be executed after the given task.'}
#user_question = 'Which task can i do after task 591?' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 591, 'order': 'after', 'think': "The user is asking about a specific task id (591) and wants to know which task can be executed after it. I identified the intent as 'after' based on the wording 'do after'. I will now retrieve information about tasks that are dependent on task 591 or have dependencies after task 591."}
#user_question = 'Does task 590 require another task to be executed beforehand?' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 590, 'order': 'before', 'think': 'The user is asking about a specific task by its id and whether it requires something before being executed.'}
#user_question = 'Is task 590 independent of other tasks?' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 590, 'order': 'both', 'think': "Identified specific task id in question. Determined intent as 'independent' or 'standalone', indicating no dependencies before or after the task."}
#user_question = "Return all task dependencies" # [...] (len: 9), {'pick': 6}, {'attribute': False, 'think': ['No specific task id identified', 'returning general query response']}
#user_question = 'Return the ids of all tasks that have to be executed before task 581' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 581, 'order': 'before', 'think': 'Identified specific task by id. The user is asking about tasks that must be executed before the given task.'}
#user_question = 'Return the names of all tasks that have to be executed before task 581' # [...] (len: 1), {'pick': 6}, {'attribute': True, 'id': 581, 'order': 'before', 'think': "Identified specific task id in question. Determined intent based on wording 'before'. Assuming user wants tasks preceding task 581"}


def IntToStrWithSlabInfornt(val):
    if(type(val) != str):
        val = '_' + str(val)
    return val

def LLMOutClean(answer):
    answer = answer.replace('\n', '')
    if('`' in answer):
        answer = answer.replace('`', '')
        if(answer[:4] == 'json'):
            answer = answer[4:]
    return answer


numbertokeyword = {1: 'workcenter', 2: 'resource', 3: 'jobs', 4: 'tasks', 5: 'tasksuitableresources', 6: 'tasksprecedenceconstraints', 7: 'none'}


### Gibberish Classifier ###
answer = chat('llama3.1', messages = [{'role': 'user', 'content': _1_0_test_ollamaclassifier_new_gibberish_asfunc.getPrompt(user_question)}]).message.content
answer = LLMOutClean(answer)

try:
    answer = json.loads(answer)
    if(answer['gibberish'] == True):
        print(chat('llama3.1', messages = [{'role': 'user', 'content': _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)}]).message.content)
except:
    print(chat('llama3.1', messages = [{'role': 'user', 'content': _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)}]).message.content)

### End ###

print('----- Chain 0: Gibberish Classifier -----')
print(answer)

### Classifier 1: User Asks about Task? Jobs?, TaskSuitableRes? etc.. ###
answer = chat('llama3.1', messages = [{'role': 'user', 'content': _1_test_ollamaclassifier_new_list_rewrite_moreshots_asfunc.getPrompt(user_question)}]).message.content
answer = LLMOutClean(answer)

print('----- Chain 1: High Level (Task, Job, etc..) Classifier -----')
print(answer)


try:
    answer = json.loads(answer)
    words = answer['words']
    if(len(words) == 0):
        answer = chat('llama3.1', messages = [{'role': 'user', 'content': user_question}]).message.content # Word-based search
    else:
        if('job' in words):
            search = 'jobs'
        elif('resource' in words and 'task' in words):
            search = 'tasksuitableresources'
        elif(len(words) == 1):
            if('resource' in words):
                search = 'resources'
            elif('task' in words):
                answer = chat('llama3.1', messages = [{'role': 'user', 'content': _1_2_test_ollamaclassifier_tasks_asfunc.getPrompt(user_question)}]).message.content # Meaning-search
                answer = json.loads(LLMOutClean(answer))
                print('----- Chain 1-2: Task Specific Classifier -----')
                print(answer)
                if(answer['pick'] == 1):
                    search = 'tasksuitableresources'
                elif(answer['pick'] == 2):
                    search = 'tasksprecedenceconstraints'
                elif(answer['pick'] == 3):
                    search = 'tasks'
                else:
                    print(chat('llama3.1', messages = [{'role': 'user', 'content': _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)}]).message.content)
except:
    print(chat('llama3.1', messages = [{'role': 'user', 'content': _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)}]).message.content)
### End ###
print('----- Search Value -----')
print(search)

### GET JSON DATA ###
json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)
### End ###


### Classifier 2: Retrieve appropriate data parts ###
if(search == 'resources'):
    query = json_data["resources"]["resource"]
    prompt = _3_5_test_ollamaclassifier_attr_resource.getPrompt(user_question)
    # {"attribute": <bool>, "key": <str>, "value": <str, int>, "think": <str>}
    # key: id, name
elif(search == 'jobs'):
    query = json_data["jobs"]["job"]
    prompt = _3_1_test_ollamaclassifier_attr_job.getPrompt(user_question)
    # {"attribute": <bool>,"key": <str>,"value": <str, int>, "think": <str>}
    # key: name, arrivaldate, duedate, task, workcenter, id
elif(search == 'tasks'):
    query = json_data["tasks"]["task"]
    prompt = _3_2_test_ollamaclassifier_attr_task.getPrompt(user_question)
    # {"attribute": <bool>,"key": <str>,"value": <str, int>, "think": <str>}
    # key: id, name
elif(search == 'tasksuitableresources'):
    query = json_data["tasksuitableresources"]["tasksuitableresource"]
    prompt = _3_3_test_ollamaclassifier_attr_tasksuitableresource.getPrompt(user_question)
    # {"attribute": <bool>, "know": {"info": <str>, "key": <str>, "value": <str, int>}, "search": {"info": <str>}, "think": <str>}
    # know -> info: resource, task #<---NOTE: ALTHOUGH NOT INSTRUCTED TO IT MIGHT PUT: time IF QUESTION SHOULD BE TIME!!!
    # key: id, name
    # search -> info: resource, task, time
elif(search == 'tasksprecedenceconstraints'):
    query = json_data["taskprecedenceconstraints"]["taskprecedenceconstraint"]
    prompt = _3_4_test_ollamaclassifier_attr_taskprepost.getPrompt(user_question)
    # {"attribute": <bool>, "id": <int>, "order": <str>, "think": <str>}
    # order: 'before', 'after', 'both'
else:
    print(chat('llama3.1', messages = [{'role': 'user', 'content': _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)}]).message.content)

answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
asnwer = LLMOutClean(answer)
### End ###

print('----- Chain 2: Info Retrieve Classifier -----')
print(answer)

### EXTRACTION PART ###
try:
    retrieve_info = json.loads(answer)
except:
    retrieve_info = None

if retrieve_info == None:
    prompt = _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)
    print(chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content)
else:
    if(retrieve_info['attribute'] == True):
        
        if(search == 'resources' or search == 'tasks'):
            if(retrieve_info['key'] == 'id'):
                query = [q for q in query if q[retrieve_info['key']] == IntToStrWithSlabInfornt(retrieve_info['value'])]
            elif(retrieve_info['key'] == 'name'):
                query = [q for q in query if q[retrieve_info['key']].upper() == retrieve_info['value'].upper()]

        elif(search == 'jobs'):
            if(retrieve_info['key'] == 'id'):
                query = [q for q in query if q[retrieve_info['key']] == IntToStrWithSlabInfornt(retrieve_info['value'])]
            elif(retrieve_info['key'] == 'name'):
                query = [q for q in query if q[retrieve_info['key']].upper() == retrieve_info['value'].upper()]
            elif(retrieve_info['key'] == 'task'):
                query = [q for q in query if any(t.get('refid') == IntToStrWithSlabInfornt(retrieve_info['value']) for t in q.get('jobtaskreference', []))]
            elif(retrieve_info['key'] == 'arrivaldate' or retrieve_info['key'] == 'duedate'):
                retrieve_info['value'] = json.loads(chat('llama3.1', messages = [{'role': 'user', 'content': _a0_test_ollama_str_to_date.getPrompt(retrieve_info['value'])}]).message.content)
                query = [q for q in query if ( q[retrieve_info['key']]['day'] == retrieve_info['value']['day'] and q[retrieve_info['key']]['month'] == retrieve_info['value']['month'])]
        
        elif(search == 'tasksuitableresources'):
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

        elif(search == 'tasksprecedenceconstraints'):
            # {"attribute": <bool>,"id": <int>,"order": <str>,"think": <str>}
            # order: before, after, both
            if(retrieve_info['order'] != 'both'):
                retrieve_info['order'] = 'preconditiontaskreference' if retrieve_info['order'] == 'after' else 'postconditiontaskreference'
                query = [q for q in query if q[retrieve_info['order']]['refid'] == IntToStrWithSlabInfornt(retrieve_info['id'])]
            else:
                query = [q for q in query if q['preconditiontaskreference']['refid'] == IntToStrWithSlabInfornt(retrieve_info['id']) or q['postconditiontaskreference']['refid'] == IntToStrWithSlabInfornt(retrieve_info['id'])]

### End ###
print('----- Query Retrieved -----')
print(query)
print('----- Len Query Retrieved -----')
print(len(query))
print('----- Len Query Retrieved Tokenized -----')
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
print(len(tokenizer.tokenize(str(query))))

### Classifier 3? - Final Generation ###
fin_prompt = _5_test_answer_question_job.getPrompt(query, user_question)
fin_prompt_len = len(tokenizer.tokenize(fin_prompt))
if(search == 'jobs'):
    fin_answer = chat('llama3.1', messages = [{'role': 'user', 'content': fin_prompt}])
print('----- Chain 3: Final Answer -----')
print(fin_answer.message.content)
print('----- Original User Question -----')
print(user_question)
print('----- Len of Chain 3 Prompt Tokenized -----')
print(fin_prompt_len)