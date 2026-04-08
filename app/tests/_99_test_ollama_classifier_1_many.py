from ollama import chat
import time
from transformers import AutoTokenizer
import datetime
import pandas as pd

### RESOURCES ###

user_question = "Return all resources" # {  "pick": 2,  "think": "The user asks about resources, which is specified in rule 2: 'Pick \"2\" if the user asks about resources.'"}
user_question = "Return all resource ids" # {  "pick": 2,  "think": "The user is asking for 'resource ids', which indicates they are looking for information about resources."}
user_question = "Return resouce 2" # {  "pick": 2,  "think": "The user asked about a resource (specifically 'resouce 2') so I picked number 2."}
user_question = "Return resouce 1" # {  "pick": 2,  "think": "The user is asking about a resource (resource 1), which includes availability when it can be used."}
user_question = "What is the name of the resource with id 3" # {  "pick": 2,  "think": "The user asks about resources (specifically by 'resource' and mentioning 'id'), so I picked number 2 according to classification rule 2."}
user_question = "Return resource with id 7" # {"pick": 2,"think": "The user asks about a resource (with id), so rule #2 applies."}
user_question = "Return resource ROLLING MILL" # {  "pick": 2,  "think": "The user is asking about a specific resource (ROLLING MILL), which falls under rule 2: Pick '2' if the user asks about resources."}
user_question = "Return resource rolling mill" # {  "pick": 2,  "think": "The user question asks about resources, specifically 'resource' and mentions a location, 'rolling mill'. According to rule 2, if the question includes availability or when a resource can be used, I should pick '2'."}
user_question = "How many resources are there" # {  "pick": 2,  "think": "The user asks about resources, so I picked '2' as it matches rule 2."}
user_question = "Return the first resource" # {  "pick": 2,  "think": "The user question asks about a resource (the first one), which matches rule #2."}
user_question = "Return 1 resource" # {"pick": 2,"think": "The user asks about resources (returning one resource) which matches rule #2."}
user_question = "Return 1 resources" # {  "pick": 2,  "think": "The user asks about resources and implies availability when they say 'return'. This suggests a question about when a resource can be used."}

### JOBS ###

user_question = "Return the job with arrival date 31/3" # {  "pick": 3,  "think": "The user is asking about jobs and specifically mentions 'arrival date' which implies a job-related concept."}
user_question = "List all jobs" # {  "pick": 3,  "think": "The user input asks about jobs, so I picked '3' according to rule 3."}
user_question = "Give me the jobs" # {  "pick": 3,  "think": "The user input asks about jobs."}
user_question = "Return the job with id 8" # {  "pick": 3,  "think": "The user asks about jobs, specifically asking to return a job with an ID."}
user_question = "Are there any jobs with arrival date 31 2" # {"pick": 3,"think": "The user input asks about jobs because it includes information related to 'jobs' and a specific attribute ('arrival date') but no tasks."}
user_question = "List jobs with id 51" # {  "pick": 3,  "think": "The user input asks about jobs, specifically requesting a list of jobs with id 51, which indicates a job-related query."}
user_question = "Find jobs that require task 581" # {"pick": 3,"think": "The question asks about 'jobs' and specifically mentions 'task 581', indicating a job-task relationship."}
user_question = "Find jobs that require task with id 581" # {"pick": 3,"think": "The user input asks about jobs and includes a specific task ID (id 581) which is part of a job. This matches rule 3, so I picked number 3."}
user_question = "Find the last job that requires task with id 581" # {  "pick": 3,  "think": "The user asks about jobs (specifically, finding a job based on its relationship to a task), so according to rule 3, I pick '3'."}
user_question = "Return the first job" # {  "pick": 3,  "think": "The user input asks about jobs."}
user_question = "Return the job at index 5" # {  "pick": 3,  "think": "The user is asking for a job by its index, which indicates a question about jobs."}
user_question = "Return the first job that requires the task with id 580" # {"pick": "3","think": "The user is asking about jobs, specifically requesting to return the first job that requires a specific task, which indicates a relationship between tasks and jobs. According to rule 3, when the question includes both jobs and tasks, return '3' as it asks about jobs."}
user_question = "Return job 5" # {"pick": 3,"think": "The user input asks about jobs. The question 'Return job 5' specifically mentions a job ID (5), which implies that it's referring to a job."}
user_question = "Return 4 jobs" # {  "pick": 3,  "think": "The user input asks about jobs, specifically asking to return 4 jobs, which indicates they are looking for information related to jobs."}
user_question = "Return me the FROM BILLET job" # {  "pick": 3,  "think": "The user input asks about a specific 'job', namely 'FROM BILLET'. According to rule 3, if the question includes jobs, return 'Job'."}
user_question = 'Return the names of every job' # {  "pick": 3,  "think": "The user asks about jobs, so I picked number 3 according to rule 3."}
user_question = 'Return the task of job 509' # {  "pick": 3,  "think": "The question asks about a job (job 509), which falls under category 3, where we ask about jobs."}
user_question = 'Return the id of all jobs with name ROLLING' # {  "pick": 3,  "think": "The user asks about jobs and specifically mentions a job by its name, which indicates they are asking for information related to jobs."}
user_question = 'Return the first task of every job' # {  "pick": 3,  "think": "The user input asks about jobs, specifically requesting the first task of each job."}
user_question = 'Return the tasks of all jobs with name ROLLING' # {  "pick": 3,  "think": "The user input asks about jobs, specifically requesting the tasks of jobs with a certain name (ROLLING), which indicates the focus is on job-related information."}
user_question = 'Return all FROM BILLET jobs' # {  "pick": 3,  "think": "The user asks about jobs, specifically returning all jobs from a certain category ('BILLET'). This matches rule 3."}
user_question = 'Return all jobs with name FROM BILLET' # {  "pick": 3,  "think": "The user asks about jobs and specifically mentions 'name FROM BILLET', which is related to job information, so I picked 3 as it concerns jobs."}
user_question = 'Return all ROLLING jobs' # {  "pick": 3,  "think": "The user input asks about jobs, so I picked number 3 according to rule 3."}
user_question = 'Return all job ids' # {  "pick": 3,  "think": "The user asks about jobs, which matches rule #3."}

### TASKS ###

user_question = "Return task with id 584" # {"pick": 4,"think": "The user input asks about a specific task by its id, which falls under the category of tasks only."}
user_question = "task with name Rolling" # {  "pick": 4,  "think": "The user input asks about tasks only, as it specifically mentions a task by its name 'Rolling'."}
user_question = "Return first task with name Rolling" # {  "pick": 4,  "think": "The user asks about a specific task by name ('Rolling'), which suggests it's asking about tasks only."}
user_question = "Return first task" # {  "pick": 4,  "think": "The question specifically asks about tasks ('task') and does not mention resources, jobs, or other categories that would require a different classification."}
user_question = "tasks" # {  "pick": 4,  "think": "The user input asks about tasks only, so according to rule 4, I pick number 4."}
user_question = "return task 7" # {  "pick": 4,  "think": "The user is asking about a specific task (task 7) which suggests that the question concerns tasks only, so I picked number 4"}
# Problematic --> ## user_question = "return 7 task" # {"pick": 4,"think": "The user input asks about tasks only, specifically mentioning the 'task' keyword."}
user_question = "return 7 tasks" # {  "pick": 4,  "think": "The user asks about tasks only, specifically requesting to return a certain number of them (7 in this case). This matches rule 4, which states that if the question concerns tasks only or any of their attributes, I should pick '4'."}
user_question = "return the last task" # {  "pick": 4,  "think": "The user question asks about tasks only, as it is asking to return a specific task, which implies attributes related to that task."}
user_question = 'Return all ROLLING tasks' # {  "pick": 4,  "think": "The user question is asking about tasks only, specifically ROLLING tasks, which indicates a query related to task attributes."}
user_question = 'Return the id of all tasks with name ROLLING' # {  "pick": 4,  "think": "I picked 4 because the user question asks about tasks only, specifically those with a certain name 'ROLLING'. This falls under category 4, which concerns tasks and their attributes."}
user_question = 'What is the name of the task with id 77' # {  "pick": 4,  "think": "I picked number 4 because the user question asks about tasks only, specifically asking for the name of a task with an ID."}
# user_question = 'What are the ids of MELTING' # {"attribute": true,"key": "name","value": "MELTING", "think": "The user is searching for a specific task using its name, which is provided as 'MELTING'."}
user_question = 'Return all tasks' # {  "pick": 4,  "think": "The user input asks about tasks only."}
user_question = 'Return the name of every task' # {  "pick": 4,  "think": "The user input asks about tasks only."}

### TASKSUITABLERESOURCES ###

user_question = 'Which tasks can be done in resource 901?' # {  "pick": 5,  "think": "The question concerns which task can be executed on a specific resource (resource 901), so I picked number 5 according to rule 5."}
user_question = 'Where can task 57 be executed' # {  "pick": 5,  "think": "The question concerns the location in which (where) a task can be executed, which matches rule 5."}
user_question = 'Which resource can execute task with id 39?' # {"pick": 5,"think": "The question includes both tasks (task) and resources (resource), so I picked number 5 according to rule 5."}
user_question = 'Which resource can execute task 39?' # {"pick": 5,"think": "The question mentions both tasks and resources, specifically asking which resource can execute a task."}
user_question = 'Can Task 11 be executed in the MELTSHOP?' # {"pick": 5,"think": "The question concerns a task and its execution resource (the location where it can be done). The user is asking about the ability to execute a specific task (Task 11) at a certain location (MELTSHOP), which meets rule 5."}
user_question = 'How long does task 52 take?' # {  "pick": 5,  "think": "The user question asks about how long a specific task (task 52) takes, which falls under category 5: concerns the execution time or duration of a task."}
user_question = 'What resource can execute each task?' # {  "pick": 5,  "think": "The user question asks about which resource can execute a task, so I picked number 5 according to rule 5."}
user_question = 'Return all resources and tasks' # {  "pick": 5,  "think": "The question concerns both tasks and resources, as both words are explicitly mentioned in the user's input. Therefore, I picked number 5 according to rule 5."}
user_question = 'Return all resources and their tasks' # {  "pick": 5,  "think": "The user question asks for both resources and tasks, indicating that it falls under category 5, which concerns relationships between tasks and resources."}
user_question = 'Return the id of the resource that can execute task 91' # {  "pick": 5,  "think": "The user question asks about a specific task (91) and references a resource, so it falls under category 5 which concerns relationships between tasks and resources."}
#user_question = 'What task can be executed in the ROLLING MILL' # {  "pick": 5,  "think": "The user question concerns the location where a task can be executed, which matches rule 5."}
#user_question = 'Return the ids of all resources and tasks' # {  "pick": 5,  "think": "The user question includes both resources and tasks, so I picked number 5 according to rule 5."}
#user_question = 'Return all resources where task 77 can be executed' # {"pick": 5,"think": "The user asks about the location in which (where) a task can be executed, and also mentions the specific task id '77'. This matches rule 5."}
#user_question = 'Return the id of every resource where task 77 can be executed' # {  "pick": 5,  "think": "The user is asking about a task (task 77) and its execution on one or more resources, which matches rule 5. Additionally, the question includes the words 'resource' and 'task', reinforcing this choice."}
#user_question = 'What is the operation time for task 73' # {  "pick": 5,  "think": "The question concerns execution time of a task, so I picked number 5 according to rule 5"}
#user_question = 'What tasks need to operate for more than 30minutes?' # {  "pick": 5,  "think": "The user question asks about tasks and their execution time, which is longer than 30 minutes, so it falls under category 5."}

### TASKPREPOST ###

#user_question = "Is there a task to be executed before task with id 483?" #   "pick": 6,  "think": "The user question concerns dependencies between tasks and which task must happen before another task, so I picked number 6."}
#user_question = "Is there a task to be executed before task 11?" # {"pick": 6,"think": "The question concerns dependencies between tasks and the order in which they must happen, specifically asking which task must occur before another task (task 11)."}
#user_question = "Is there a task to be executed before 183?" # {    "pick": 6,    "think": "The user question mentions 'before' and 'task to be executed', indicating a relationship between tasks, which falls under category 6 (the order of tasks or dependencies between tasks)."}  
#user_question = 'Which task should i execute before task 1?' # {  "pick": 6,  "think": "The question concerns the order of tasks and dependencies between tasks, specifically which task must happen before another task (task 1). This matches rule 6."}
#user_question = 'What task can i execute after completing task 13?' # {  "pick": 6,  "think": "The question concerns dependencies between tasks (which task must happen before/after another task), specifically asking about the order of tasks, so I picked number 6."}
#user_question = 'Which task can i do after task 55?' # {"pick": 6,"think": "The question asks about dependencies between tasks (specifically, which task must happen before another task), so I picked number 6."}
#user_question = 'Does task 53 require another task to be executed beforehand?' # {"pick": 6,"think": "The user question asks about dependencies between tasks (which task must happen before another task), so I picked number 6."}
#user_question = 'Is task 301 independent of other tasks?' # {  "pick": 6,  "think": "The user question concerns dependencies between tasks, specifically which task must happen before/after another task is not mentioned but the independence of a task from others is asked. Hence it's about task order and I picked number 6"}
#user_question = "Return all task dependencies" # {  "pick": 6,  "think": "The user question concerns the order of tasks and dependencies between tasks, specifically asking for task dependencies to be returned."}
#user_question = 'Return the ids of all tasks that have to be executed before task 79' # {  "pick": 6,  "think": "The user is asking about dependencies between tasks, specifically which tasks must happen before another task (task 79). This matches rule 6."}
#user_question = 'Return the names of all tasks that have to be executed before task 85' # {  "pick": 6,  "think": "The question concerns dependencies between tasks, specifically which task must happen before another task (task 85)."}

### NONE ###

#user_question = 'Hi, how are you?' # {  "pick": 7,  "think": "The question does not belong to any category above and appears to be a greeting."}
#user_question = 'What is this file about?' # {  "pick": 7,  "think": "The question does not clearly belong to any category above, it's a general inquiry about a file and doesn't contain any specific keywords related to workcenters, resources, jobs, tasks, or their attributes."}
#user_question = 'How are you' # {  "pick": 7,  "think": "The question does not clearly belong to any category above and is gibberish."}
#user_question = 'asijhduasjh' # {  "pick": 7,  "think": "The user question appears to be gibberish or random characters without any coherent text, so I picked number 7 as it falls under the category of 'the question does not clearly belong to any category above'."}
#user_question = 'a' # {"pick": 7,"think": "The question contains only a single number without any context, so it does not clearly belong to any category above."}
#user_question = 'aaa' # {  "pick": 7,  "think": "The question contains only single characters without anything else in the input, so it does not clearly belong to any category above."}
#user_question = '90809809' # {  "pick": 7,  "think": "The input is a single number without anything else, so it does not clearly belong to any category above."}
#user_question = '1' # {  "pick": 7,  "think": "The user question contains only a single number without any additional text, so it does not fit into any of the other categories and is classified as gibberish."}
#user_question = 'Who is Pikachu?' # {  "pick": 7,  "think": "The question does not contain any relevant keywords related to workcenters, resources, jobs, tasks, etc., and therefore it cannot be classified into any of the predefined categories."}
#user_question = 'Where can i buy Gucci' # {  "pick": 7,  "think": "The user question does not seem to be related to workcenters, resources, jobs, tasks, or their attributes. It is also not asking about any specific details that would lead to one of the other classifications."}
#user_question = '111111' #   "pick": 7,  "think": "The question is a single number without anything else in the input, so it does not clearly belong to any category above and should be classified as a random or gibberish input."}
#user_question = '11' # {  "pick": 7,  "think": "The user question contains only a number (11) without any context or meaningful words, so it does not clearly belong to any category above and is considered gibberish."}
#user_question = 'vuvuvuvuvu' # {  "pick": 7,  "think": "The user question contains only random characters and does not contain any relevant information about workcenters, resources, jobs, tasks, or their attributes."}

#user_question = "return 7 task"

system_content_asuserprompt = """You are a classifier. Your task is to analyze a user's question and pick EXACTLY ONE number from the predefined list below.

You must ALWAYS pick a number from the list below

Possible numbers:
- 1
- 2
- 3
- 4
- 5
- 6
- 7

Classification rules:

1. Pick "1" if the user specifically lists the word 'workcenter' in the question.

2. Pick "2" if:
   - the user asks about resources only or their attributes (name, id etc).
   - the question includes availability, when a resource can be used (words like available or can be used have to be present).
   NOTE: a resource might also be refered to as a location like a MELTSHOP. Unless either the keyword 'resource' is mentioned or a location you CANNOT assume the user asks about resources

3. Pick "3" if the user input asks about jobs.  
   IMPORTANT: If the question includes both jobs and tasks (e.g., tasks belonging to a job, job-task relationships, nested task structures within jobs), return "Job".
   Both the keywords 'task' and 'job' need to be present in the question. If they are NOT, do NOT imply any relationships

4. Pick "4" if ALL of the following are satisfied:
   - the user asks about tasks
   - keyword 'task' is present, but NO other keywords are present ('job', 'resource')
   - If an attribute is mentioned it should NOT be about operating time, duration or how long a task takes
   - If the attribute refers to duration, how long a task takes or operating time pick the number "5" instead

5. Pick "5" if the question concerns one or more of the following:
   - references both tasks AND resources (both the words 'resource' and 'task' need to be stated in the user question)
   - which resource can execute a task (both the words 'resource' and 'task' need to be stated in the user question)
   - the location in which (where) a task can be executed
   - how long a task takes, the duration, operating time of a task
   - execution time or duration of a task

6. Pick "6" if the question concerns:
   - the order of tasks
   - dependencies between tasks
   - independencies between tasks
   - which task must happen before/after another task

7. Pick "7" if:
   - the question does not clearly belong to any category above.
   - the question is gibberish or random, single characters or numbers without anything else in the input.
   - If the question is a single number without anything else in the input
   DO NOT RETURN "7" if keywords 'task', 'job' or 'resource' are present in the question

Inportant Rules:
-> Never confuse keywords (job, task, resource etc). These keywords work like identifiers and should never be conceptually interpreted.
   The keyword 'task' refers to tasks only and no other keyword. The keyword 'job' refers to jobs only and no other keyword. The keyword 'resource' refers to resources only and no other keyword. 
-> NEVER correlate a number in the question with a Pick option. These are completely irrelevant. If the number 5 is present in the question NEVER ASSUME that you should pick 5.
   
Output Format:

{'pick': <int>, 'think': <Your thinking process>}

- pick: the number that you picked from the predefined list
- think: Your thinking process as to why you picked that number

Remember:
- Always return ONLY valid JSON and nothing else. Do not explain Youserlf.
- There should be nothing outside the valid JSON: punctuation, semicolons, backticks '`' or '```', the word 'json', any info etc.. Your Output should start with '{' and finish with '}'
   Examples:
   Output: {'pick': 3, 'think': <Your thinking process>}
   Output: {'pick': 1, 'think': <Your thinking process>}
"""

system_content_asuserprompt += f"""

___________________
User Question:
{user_question}
"""

list_questions = [
### RESOURCES ###

'*****',
"Return all resources",
"Return all resource ids",
"Return resouce 2",
"Return resouce 1",
"What is the name of the resource with id 3",
"Return resource with id 7",
"Return resource ROLLING MILL",
"Return resource rolling mill",
"How many resources are there",
"Return the first resource",
"Return 1 resource",
"Return 1 resources",

### JOBS ###

'*****',
"Return the job with arrival date 31/3",
"List all jobs",
"Give me the jobs",
"Return the job with id 8",
"Are there any jobs with arrival date 31 2",
"List jobs with id 51",
"Find jobs that require task 581",
"Find jobs that require task with id 581",
"Find the last job that requires task with id 581",
"Return the first job",
"Return the job at index 5",
"Return the first job that requires the task with id 580",
"Return job 5",
"Return 4 jobs",
"Return me the FROM BILLET job",
'Return the names of every job',
'Return the task of job 509',
'Return the id of all jobs with name ROLLING',
'Return the first task of every job',
'Return the tasks of all jobs with name ROLLING',
'Return all FROM BILLET jobs',
'Return all jobs with name FROM BILLET',
'Return all ROLLING jobs',
'Return all job ids',

### TASKS ###

'*****',
"Return task with id 584",
"task with name Rolling",
"Return first task with name Rolling",
"Return first task",
"tasks",
"return task 7",
"return 7 task",
"return 7 tasks",
"return the last task",
'Return all ROLLING tasks',
'Return the id of all tasks with name ROLLING',
'What is the name of the task with id 77',
'What are the ids of MELTING',
'Return all tasks',
'Return the name of every task',

### TASKSUITABLERESOURCES ###

'*****',
'Which tasks can be done in resource 901?',
'Where can task 57 be executed',
'Which resource can execute task with id 39?',
'Which resource can execute task 39?',
'Can Task 11 be executed in the MELTSHOP?',
'How long does task 52 take?',
'What resource can execute each task?',
'Return all resources and tasks',
'Return all resources and their tasks',
'Return the id of the resource that can execute task 91',
'What task can be executed in the ROLLING MILL',
'Return the ids of all resources and tasks',
'Return all resources where task 77 can be executed',
'Return the id of every resource where task 77 can be executed',
'What is the operation time for task 73',
'What tasks need to operate for more than 30minutes?',

### TASKPREPOST ###

'*****',
"Is there a task to be executed before task with id 483?",
"Is there a task to be executed before task 11?",
"Is there a task to be executed before 183?",
'Which task should i execute before task 1?',
'What task can i execute after completing task 13?',
'Which task can i do after task 55?',
'Does task 53 require another task to be executed beforehand?',
'Is task 301 independent of other tasks?',
"Return all task dependencies",
'Return the ids of all tasks that have to be executed before task 79',
'Return the names of all tasks that have to be executed before task 85',

### NONE ###

'*****',
'Hi, how are you?',
'What is this file about?',
'How are you',
'asijhduasjh',
'a',
'aaa',
'90809809',
'1',
'Who is Pikachu?',
'Where can i buy Gucci',
'111111',
'11',
'vuvuvuvuvu',
]


file_name = 'C:/Users/Chris/Downloads/diplomat/app/tests/_5_output_ollama_test/_1_classifier_outputs/' + 'out_' + str(datetime.date.today()) + '_' + str(int(time.time())) + '.csv'

u_q = []
llm_o = []
md = []

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
for i in range(0, len(list_questions)):
    for y in range(0, 5):
        user_question = list_questions[i]
        if(user_question == '*****'):
            continue
        else:
            start_time = time.time()
            prompt = """You are a classifier. Your task is to analyze a user's question and pick EXACTLY ONE number from the predefined list below.

    You must ALWAYS pick a number from the list below

    Possible numbers:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6
    - 7

    Classification rules:

    1. Pick "1" if the user specifically lists the word 'workcenter' in the question.

    2. Pick "2" if:
    - the user asks about resources only or their attributes (name, id etc).
    - the question includes availability, when a resource can be used (words like available or can be used have to be present).
    NOTE: a resource might also be refered to as a location like a MELTSHOP. Unless either the keyword 'resource' is mentioned or a location you CANNOT assume the user asks about resources

    3. Pick "3" if the user input asks about jobs.  
    IMPORTANT: If the question includes both jobs and tasks (e.g., tasks belonging to a job, job-task relationships, nested task structures within jobs), return "Job".
    Both the keywords 'task' and 'job' need to be present in the question. If they are NOT, do NOT imply any relationships

    4. Pick "4" if ALL of the following are satisfied:
    - the user asks about tasks
    - keyword 'task' is present, but NO other keywords are present ('job', 'resource')
    - If an attribute is mentioned it should NOT be about operating time, duration or how long a task takes
    - If the attribute refers to duration, how long a task takes or operating time pick the number "5" instead

    5. Pick "5" if the question concerns one or more of the following:
    - references both tasks AND resources (both the words 'resource' and 'task' need to be stated in the user question)
    - which resource can execute a task (both the words 'resource' and 'task' need to be stated in the user question)
    - the location in which (where) a task can be executed
    - how long a task takes, the duration, operating time of a task
    - execution time or duration of a task

    6. Pick "6" if the question concerns:
    - the order of tasks
    - dependencies between tasks
    - independencies between tasks
    - which task must happen before/after another task

    7. Pick "7" if:
    - the question does not clearly belong to any category above.
    - the question is gibberish or random, single characters or numbers without anything else in the input.
    - If the question is a single number without anything else in the input
    DO NOT RETURN "7" if keywords 'task', 'job' or 'resource' are present in the question

    Inportant Rules:
    -> Never confuse keywords (job, task, resource etc). These keywords work like identifiers and should never be conceptually interpreted.
    The keyword 'task' refers to tasks only and no other keyword. The keyword 'job' refers to jobs only and no other keyword. The keyword 'resource' refers to resources only and no other keyword. 
    -> NEVER correlate a number in the question with a Pick option. These are completely irrelevant. If the number 5 is present in the question NEVER ASSUME that you should pick 5.
    
    Output Format:

    {'pick': <int>, 'think': <Your thinking process>}

    - pick: the number that you picked from the predefined list
    - think: Your thinking process as to why you picked that number

    Remember:
    - Always return ONLY valid JSON and nothing else. Do not explain Youserlf.
    - There should be nothing outside the valid JSON: punctuation, semicolons, backticks '`' or '```', the word 'json', any info etc.. Your Output should start with '{' and finish with '}'
    Examples:
    Output: {'pick': 3, 'think': <Your thinking process>}
    Output: {'pick': 1, 'think': <Your thinking process>}
    """

            prompt += f"""

    ___________________
    User Question:
    {user_question}
    """
            
            prompt_tokens = len(tokenizer.tokenize(prompt))
            
            llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
            llm_answer = llm_answer.replace('\n', '')

            answer_correct = True
            original_answer = llm_answer
            if('`' in llm_answer):
                answer_correct = False
                llm_answer = llm_answer.replace('`', '')
                if(llm_answer[:4] == 'json'):
                    llm_answer = llm_answer[4:]
            compute_time = time.time() - start_time
            metadata = {'Prompt_tokens': prompt_tokens, 'compute_time': compute_time, 'answer_correct': answer_correct, 'original_answer': None if answer_correct else original_answer, 'answer': llm_answer, 'user_question': user_question}
            u_q.append(user_question)
            llm_o.append(llm_answer)
            md.append(metadata)

        print('finsihed: ' + str(i))

all_data = {'User Question': u_q, 'LLM Output': llm_o, 'Metadata': md}
df = pd.DataFrame(all_data)
df.to_csv(file_name, index=False)

asdasdasdasd

print('***')
print(user_question)
start_time = time.time()
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': system_content_asuserprompt}])

print('==============')
aa = llm_answer.message.content
aa = aa.replace('\n', '')
print(aa)
if('`' in aa):
   aa = aa.replace('`', '')
   if(aa[:4] == 'json'):
      aa = aa[4:]
   print('!!!!!!!!!!')
   print(aa)
print('--- time ---')
print(time.time() - start_time)