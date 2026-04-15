from ollama import chat
import json

import _x0_test_ollama_error_chain_1_prompt
import _6_0_test_ollama_fin_answer_noresults_asfunc
import _6_1_test_ollama_fin_answer_jobs_tasks_resources_matchesfound_asfunc
import _6_2_x_NEW_classify_boolean_asfunc
import _6_2_test_ollama_tasksuitableresources_asfunc
import _6_4_test_ollama_taskprepost_dependence_asfunc
import _6_3_test_ollma_tasksuitres_answer_what_task_asfunc
import _6_0_0_task_not_exist_in_json_file_asfunc

### JOBS ###

user_question = "List all jobs" '''I've found 10 matches for your query.

(DATA)

Would you like me to help with anything else, or would you like more information about these jobs?'''
search = 'jobs'
query = [1,1,1,1,1,1,1,1,1,1]
retrieve_info = []


user_question = "Return the job with arrival date 31/3" '''I've searched the JSON file you provided, but unfortunately, I couldn't find any matches for "job" with an arrival date of 31/3. It's possible that such information is not present in the uploaded file or does not match your chosen filtering criteria.

Would you like me to help you review the available data or assist you with a different query?'''
search = 'jobs'
query = []
retrieve_info = []


user_question = "Give me the jobs" '''Based on your search, I found 10 matching results. 

(DATA)

Would you like me to help with anything else? Do you need more information about these jobs or would you like to narrow down the search by specifying a particular attribute?'''
search = 'jobs'
query = [1,1,1,1,1,1,1,1,1,1]
retrieve_info = []

user_question = "Return the job with id 8" '''I couldn't find any matches for the job ID 8 in the JSON file you provided.

However, I can tell you that there are no jobs found with this specific ID. If you'd like to try searching again or need help with something else, how about trying a different search criteria? Do you need assistance finding information on tasks or resources instead?'''
search = 'jobs'
query = []
retrieve_info = []


user_question = "Return the job with id 300" '''Based on your search, I found only one match.

(DATA)

Is there anything else you'd like to know or any other task you need help with?'''
search = 'jobs'
query = [1]
retrieve_info = []
'''There's a single result that matches your query. I'll list the retrieved data below:

(DATA)


Would you like me to assist you in filtering this result based on specific criteria, such as job title or department?'''

user_question = "Are there any jobs with arrival date 31 2" '''I've searched the JSON file you uploaded and couldn't find any matches for "jobs" with an arrival date of 31st February. It's possible that this specific filter criteria didn't exist in the data or was not available.

Would you like to try filtering by a different date range or perhaps look at another aspect of the JSON file?'''
search = 'jobs'
query = []
retrieve_info = []

user_question = "List jobs with id 295" '''There's only one job matching your search criteria. I'll list the retrieved data.

(DATA)

Would you like me to explain what each field in the output means, or is there anything else I can help you with?'''
search = 'jobs'
query = [1]
retrieve_info = []

user_question = "Find jobs that require task 581" '''There's only one job that matches your search criteria. I can provide you with the details of this job.

(DATA)

Would you like me to help with anything else, or would you like more information about a specific aspect of this job?'''
search = 'jobs'
query = [1]
retrieve_info = []

#user_question = "Find the last job that requires task with id 581" # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'task', 'value': 581}
#user_question = "Return the first job" # [...] (len: 1), {'pick': 3}, {'attribute': False, 'think': 'The user did not specify a particular attribute or value. It seems they are asking for the first job, but without specifying how to identify it (e.g., by id, name), I cannot determine which key and value to extract.'}
#user_question = "Return the job at index 5" # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': "The user is asking for a job by its index, but there's no information about the job itself. This could be referring to any job or none, so I'm assuming it's not a specific job."}
#user_question = "Return the first job that requires the task with id 580" # [...] (len: 1), {'pick': 3}, [{'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_580'}, {'refid': '_581'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_297'}]
#user_question = "Return job 5" #<---implies id here # [...] (len: 1), {'pick': 3}, {'attribute': True, 'key': 'id', 'value': 5, 'think': 'The user is asking for a specific job by its id, which matches one of the allowed attributes (id).'}
#user_question = "Return 4 jobs" # [...] (len: 9), {'pick': 3}, {'attribute': False, 'think': 'The question does not specify a particular attribute or job. It is asking for all jobs without any specific criteria.'}

user_question = "Return me the FROM BILLET job" #<---understand theres name here
'''It looks like there's only one match for your search. I'd be happy to provide you with more information about that specific result.

I'll list the retrieved data:

(DATA)

Is there anything else I can help you with regarding this particular item or would you like me to assist you with something else?'''
search = 'jobs'
query = [1]
retrieve_info = []

user_question = "Return me the FROM BILLET job" #<---understand theres name here
'''I found 9 relevant matches for your search. It appears that there are numerous jobs available with the title "FROM BILLET". I'll list the retrieved information for you.

(DATA)

Is there anything else I can help you with? Would you like to filter or sort these results in any way, perhaps by a specific attribute such as job ID or location?'''
search = 'jobs'
query = [1,1 ,1 ,1 ,1 , 1,1 ,1 , 1]
retrieve_info = []

user_question = 'Return the job with id 509'
'''I couldn't find any matches for "job" with id 509 in the uploaded JSON file.

If you'd like to try again or need help with something else, what would you like to search for next? Would you like me to assist you with finding a specific task or resource instead?'''
search = 'jobs'
query = []
retrieve_info = []

user_question = 'Return all jobs with arrivaldate 31 3'
'''I've searched the JSON file you uploaded, and unfortunately, I couldn't find any matches for your request. It appears that there are no jobs with an arrival date of 31 3.

Would you like me to help you filter by a different criteria or need assistance with anything else?'''
search = 'jobs'
query = []
retrieve_info = []

user_question = 'Return all jobs with due date 31 march'
'''It looks like there's only one job that matches your search criteria. I've found the relevant information, and I'll list it out for you below.

(DATA)

Is there anything else I can help you with regarding this specific job or would you like to know more about something else?'''
search = 'jobs'
query = [1]
retrieve_info = []


user_question = 'Return job 299'
'''So there's only one item matching your search for job 299. I'll list the information related to it.

(DATA)

Is there anything else I can help you with? Do you need assistance with something specific regarding this result, or would you like more details about the next steps?'''
search = 'jobs'
query = [1]
retrieve_info = []

user_question = 'Return the ids of all jobs'
'''It looks like I was able to find 11 matching records for your query. Before I provide you with the details, I just want to make sure you're aware that I'll be listing out the information related to the "jobs" you requested.

Here is the list of data:

(DATA)

Now that you've seen the list of job IDs, do you need help with anything else or would you like me to explain what each ID represents?'''
'''It seems I found 11 relevant records for your query. Based on this, I can give you a list of the retrieved information.

(DATA)

Would you like me to help with anything else? Perhaps you'd like to know more about any specific record or have further questions regarding the results?'''
search = 'jobs'
query = [1,1 ,1 ,1 ,1, 1, 1, 1, 1, 1, 1]
retrieve_info = []

user_question = 'What is the name of job 277'
'''It looks like there's only one piece of information that matches your query. I've found it, but I'll need to list the details for you first.

(DATA)

Now that you have all the relevant information, would you like me to help with anything else? Perhaps you'd like to know more about a specific attribute or need assistance with something related to job 277?'''
search = 'jobs'
query = [1]
retrieve_info = []

### TASKS ###

user_question = "Return task with id 584"
'''So, it looks like there's only one result matching your query. I've found a single task with an ID of 584. Would you like me to list the details about this specific task?

(DATA)

How would you like to proceed? Would you like more information or is there something else I can help you with?'''
search = 'tasks'
query = [1]
retrieve_info = []

user_question = "task with name Rolling"
'''There's just one task that matches your search. I can list the details for you.

(DATA)

Is there anything else I can help you with regarding this task, or would you like to explore other aspects of it?'''
search = 'tasks'
query = [1]
retrieve_info = []

user_question = 'Return the id of all tasks with name ROLLING'
'''It looks like I've found 8 matching results for your search. Based on my findings, it seems that there are indeed some tasks that match the name "ROLLING". To give you a clear overview, here is the information:

(DATA)

Would you like me to help with anything else or would you like more details about these matches?'''
search = 'tasks'
query = [1,1 ,1, 1, 1, 1, 1,1]
retrieve_info = []

user_question = "return task 7"
'''I'm sorry, but no match was found for "task 7" in the JSON file you provided. It appears that there is no entry with this key.

Would you like to try searching again or need help with anything else?'''
search = 'tasks'
query = []
retrieve_info = []

### RESOURCES ###

user_question = "Return all resources"
'''There are 2 resources matching your query. I'll list them for you.

(DATA)

Is there anything else I can help you with regarding these resources? Do you need me to help with anything else or would you like more details about any of the items listed?'''
search = 'resources'
query = [1, 1]
retrieve_info = []

user_question = "Return all resource ids"
'''Based on your query, I've found that there are 2 matching resources. To provide you with the information you're looking for, I'll list the retrieved data below:

(DATA)

Is there anything else I can help you with regarding these resources? Perhaps you'd like me to explain how they relate to one another or assist with further analysis?'''
search = 'resources'
query = [1, 1]
retrieve_info = []

user_question = "What is the name of the resource with id 3"
'''I couldn't find any information about a resource with the ID 3. It seems that this ID doesn't exist in the JSON file you provided, or there's no match for it based on your filtering criteria.

Would you like to check another resource by its ID or explore other keys in the JSON file?'''
search = 'resources'
query = []
retrieve_info = []

user_question = "Return resource ROLLING MILL"
'''There's a single resource that matches your search for "ROLLING MILL". I'll list the retrieved information:

(DATA)

Would you like me to explain anything about this resource or help with something else?'''
search = 'resources'
query = [1]
retrieve_info = []

### TASKSUITABLERESOURCES ###
user_question = 'Which tasks can be done in resource 901?'
'''I've searched the JSON file you uploaded, but unfortunately, no matches were found for tasks associated with resource 901. It's possible that there may not be any tasks assigned to this specific resource based on your filtering criteria.

Would you like me to help with anything else, or would you like to clarify the filtering criteria you used?'''
search = 'tasksuitableresources'
query = []
retrieve_info = []

user_question = 'Which tasks can be done in resource 2?'
'''I've found some relevant information about your uploaded JSON file. Based on the details I have, there are multiple resources available, and one of them is specifically labeled as "resource 2". For this particular resource, I was able to find multiple tasks associated with it.

Here's a summary of what I found:

9

(DATA)

Would you like me to help with anything else regarding your uploaded JSON file? Do you need assistance filtering the results or understanding any specific details?'''
'''According to my search, there are 9 results that match your query. I've located the information you're looking for.

Here is the list of tasks that can be done in resource 2:

(DATA)

How would you like me to further assist you with this information or do you need help with anything else?'''
search = 'tasksuitableresources'
query = [1, 1, 1, 1, 1, 1, 1, 1, 1]
retrieve_info = []

user_question = 'Can Task 11 be executed in the MELTSHOP?'
'''I've searched through the JSON file you provided, but unfortunately, I couldn't find any information that matches your request. It seems that there is no Task 11 found with the specified filtering criteria.

If you'd like to proceed, would you like me to help you check for any other tasks or assist you in finding a specific task by its unique identifier?'''
search = 'tasksuitableresources'
query = []
retrieve_info = []

user_question = 'Return the id of the resource that can execute task 585'
'''I've found one matching result. Since there's only one relevant entry, I'll list it out for you.

(DATA)

Would you like me to clarify anything or would you like to proceed with another query?'''
search = 'tasksuitableresources'
query = [1]
retrieve_info = []

user_question = 'Return all resources and tasks'
'''Based on the information you provided, I found 9 relevant matches.

To give you a clear overview of what's available, I'll list the retrieved resources.
(DATA)

Is there anything else I can help you with? Would you like to narrow down your search or view specific details about these resources and tasks?'''
search = 'tasksuitableresources'
query = [1,1 ,1 ,1, 1, 1, 1, 1, 1]
retrieve_info = []

user_question = 'How long does task 584 take?'
'''There's only one piece of information available regarding the duration of task 584. I'll list the retrieved data:

(DATA)

Would you like me to explain how to use this information or is there anything else I can help with?'''
search = 'tasksuitableresources'
query = [1]
retrieve_info = []

### TASKPRECEDENCECONSTRAINTS ###
user_question = "Is there a task to be executed before task with id 483?"
'''Yes, I found that information. The relevant data will be listed below.

(DATA)

Would you like me to explain the context of this result or help you find more details about it?'''
'''Yes, based on the information I have, it appears that there is indeed a task that needs to be executed before the task with id 483.

I will list all the relevant tasks as follows:

(DATA)

Would you like me to explain more about these tasks or help with anything else?'''
'''Yes, there is a task that needs to be executed before the task with ID 483.

I will list all the relevant data for your reference:

(DATA)

Would you like me to explain any of these details or help you further with this information?'''
'''Yes, that's correct. There is a task scheduled before the task with ID 483.

I'll list all the relevant tasks for you:

(DATA)

Would you like me to help you understand any specific details about these tasks or assist with anything else?'''
search = 'tasksprecedenceconstraints'
query = [{'before': 227, 'after': 483}]
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Which task should i execute before task 1?'
'''I couldn't find any match for a task that needs to be executed before "task 1" in your uploaded JSON file. It seems there's no dependency or prerequisite task specified for task 1.

If you'd like, I can help you review the tasks listed in your JSON file and identify any dependencies or sequences that might be relevant to your workflow. Would you like me to assist with anything else?'''
search = 'tasksprecedenceconstraints'
query = []
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Which task should i execute before task 581?'
'''Task 553.

I will list the relevant data:
(DATA)

Would you like me to help you find any other tasks or provide more details on these specific tasks?'''
'''Task 553 should be executed before task 581.

I'll list all relevant tasks in order.
(DATA)'''
search = 'tasksprecedenceconstraints'
query = [{'before': 553, 'after': 581}]
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'What task can i execute after completing task 591?' 
'''You should execute task 597 after completing task 591.

(DATA)

Is there anything else I can help you with regarding your tasks or would you like to review the details of these tasks?'''
'''Task 597.

(DATA)'''
'''You should execute task 597.

I'll list all the relevant tasks: (DATA)

Would you like me to explain how to navigate between tasks or do you need help with anything else?'''
query = [{'before': 591, 'after': 597}]
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Does task 590 require another task to be executed beforehand?'
'''Yes, the task you're referring to does indeed require another task to be executed beforehand.

(DATA)

Would you like me to explain any of the details in (DATA) or do you need help with anything else?'''
query = [{'before': 575, 'after': 590}]
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Does task 2 require another task to be executed beforehand?'
'''I've searched through the JSON file you provided, but unfortunately, I couldn't find any information on task dependencies for task 2. It seems that there are no prerequisites specified for task 2.

If you need help with anything else or want more details about your uploaded data, feel free to ask! Would you like me to assist you with something specific now?'''
query = []
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Return the ids of all tasks that have to be executed before task 581'
'''I can confirm that there is exactly one ID for the tasks that need to be executed before task 581.

(DATA)

Is there anything else I can help you with? Would you like me to provide more information about the specific task or its dependencies?'''
query = [{'before': 775, 'after': 581}]
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Does task 584 need to be executed before 585?'
'''Based on the filtering criteria you chose, I did not find any information about the dependency of task 584 needing to be executed before task 585.

However, if you'd like to check the order or dependencies between specific tasks, you can ask me to filter the JSON file by those tasks, and I'll do my best to provide more detailed information. Would you like to proceed with that?'''
query = []
taskprecedenceconstraints_pick = 'order'
retrieve_info = []

user_question = 'Is task 590 independent of other tasks?'
'''Task 590 must be executed before task 991, so it has dependencies and is not entirely independent.

I'll list all relevant data as follows:

(DATA)

Would you like to know more about the tasks' execution order or their individual details?'''
query = [{'before': 590, 'after': 991}]
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = []

user_question = 'Does task 590 need to be executed before or after another task?'
'''Task 590 needs to be executed before task 991.

I'll list all the relevant information regarding these tasks:
(DATA)

Would you like me to explain how these two tasks are related in more detail, or is there anything else I can help you with?'''
query = [{'before': 590, 'after': 991}]
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = []

user_question = "Return all task dependencies"
'''Task 590 must be executed before task 991, task 592 must be executed before task 599, and task 322 must be executed before task 752.

I will list all the task dependencies as follows:
(DATA)

Would you like me to help with anything else or provide more details about these task dependencies?'''
query = [{'before': 590, 'after': 991}, {'before': 592, 'after': 599}, {'before': 322, 'after': 752}]
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = []

### PROBLEM -> says its independent of other tasks not that it does not exist
user_question = 'Does task 2 depend on other tasks?'
'''According to the information in the JSON file you provided, task 2 is independent. Its execution does not depend on any other tasks.

Would you like me to help with anything else or would you like more details about how this was determined from the uploaded data?'''
query = []
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = {'reference': 2, 'target': '*'}

user_question = 'Does task 590 depend on other tasks?'
'''No, task 590 does not rely on any other tasks for its execution. The dependencies in this project are independent.

Would you like to review the status of task 590 or view its associated information from the uploaded JSON file?'''
'''No, task 590 is independent and does not rely on any other tasks. 

Would you like me to check its configuration or help with anything else?'''
query = []
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = {'reference': 590, 'target': '*'}

user_question = 'Does task 590 depend on task 735?'
'''Based on the information in the JSON file you've shared with me, I can confirm that task 590 and task 735 are independent of each other. The execution of one does not depend on the completion or status of the other.

Would you like to know if there's any specific dependency between these tasks or would you like help reviewing the overall task flow?'''
query = []
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = {'reference': 590, 'target': 735}

user_question = 'Does task 2 depend on other tasks?'
'''No matches were found for your request regarding dependencies between tasks.

To confirm, I've reviewed the JSON file you provided and couldn't find any information about task 2 depending on other tasks. If you'd like to clarify or provide more context, please let me know!

Would you like me to check for dependencies of a different task, or is there anything else I can help with?'''
'''After reviewing the uploaded JSON file, I couldn't find any information indicating that task 2 depends on other tasks. With the filtering criteria you provided, there were no dependencies found for task 2.

Would you like to review the task hierarchy or explore other features in the JSON file? Do you need help with anything else?'''
query = []
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = {'reference': 2, 'target': '*'}

user_question = 'Does task 590 depend on other tasks?'
'''No, task 590's execution does not depend on other tasks.

Would you like to check if there are any conditions that need to be met before executing task 590? Or would you like me to help with something else?'''
query = []
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = {'reference': 590, 'target': '*'}

user_question = 'Does task 2 depend on other tasks?'
'''Unfortunately, I couldn't find any information about a task with ID "2" in the JSON file you provided. It seems that there is no record of a task with that specific identifier.

If you'd like to check again or need help understanding how the data in the JSON file is structured, please let me know! Would you like some assistance reviewing the contents of the JSON file?'''
query = []
taskprecedenceconstraints_pick = 'dependence'
retrieve_info = {'reference': 2, 'target': '*'}

json_path = "C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json"
with open(json_path, encoding = 'utf-8') as file:
    json_data = file.read()
    json_data = json.loads(json_data)

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

def QueryToInfoNaturalLanguage(query):
    text = ''
    for i in range (0, len(query)):
        text += f'Execute task {query[i]['before']} before task {query[i]['after']}'
        if( i + 1 != len(query)):
            text += '\n'
    return text

if(search != 'tasksprecedenceconstraints'):
    if(len(query) == 0):
        prompt = _6_0_test_ollama_fin_answer_noresults_asfunc.getPrompt(user_question)
    else:
        prompt = _6_1_test_ollama_fin_answer_jobs_tasks_resources_matchesfound_asfunc.getPrompt(user_question, len(query))
else:
    if(taskprecedenceconstraints_pick == "dependence"):
        if(len(query) == 0):
            print([q['id'] for q in json_data["tasks"]["task"]])
            if(IntToStrWithSlabInfornt(retrieve_info['reference']) not in [q['id'] for q in json_data["tasks"]["task"]]):
                print('Not in')
                prompt = _6_0_0_task_not_exist_in_json_file_asfunc.getPrompt(user_question)
            else:
                print('In')
                prompt = _6_4_test_ollama_taskprepost_dependence_asfunc.getPrompt(user_question, retrieve_info['target'])
        else:
            prompt = _6_3_test_ollma_tasksuitres_answer_what_task_asfunc.getPrompt(user_question, QueryToInfoNaturalLanguage(query))
    elif(taskprecedenceconstraints_pick == "order"):
        if(len(query) == 0):
            prompt = _6_0_test_ollama_fin_answer_noresults_asfunc.getPrompt(user_question)
        else:
            bool_classify = chat('llama3.1', messages = [{'role': 'user', 'content': _6_2_x_NEW_classify_boolean_asfunc.getPrompt(user_question)}]).message.content
            bool_classify = LLMOutClean(bool_classify)
            try:
                bool_classify = json.loads(bool_classify)
                print('&&&')
                print(bool_classify)
                print(QueryToInfoNaturalLanguage(query))
                print('&&&')
                if(bool_classify['attribute'] == True):
                    prompt = _6_2_test_ollama_tasksuitableresources_asfunc.getPrompt(user_question, len(query))
                else:
                    prompt = _6_3_test_ollma_tasksuitres_answer_what_task_asfunc.getPrompt(user_question, QueryToInfoNaturalLanguage(query))
            except:
                prompt = _x0_test_ollama_error_chain_1_prompt.getPrompt(user_question)

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print('**********************')
print(llm_answer)