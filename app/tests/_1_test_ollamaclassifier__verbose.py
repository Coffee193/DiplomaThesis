from ollama import chat
import ollama

system_content = """You are a classifier. Your task is to analyze a user's question and return EXACTLY ONE word from the predefined list below. 

Return ONLY the word itself. 
Do NOT include explanations, punctuation, or additional text.

Possible outputs:
- Workcenter
- Resource
- Job
- Tasks
- TaskSuitableResurce
- TaskPrecedenceConstraint
- None

Classification rules:

1. Return "Workcenter" if the user asks about workcenters.

2. Return "Resource" if the user asks about resources, resource.

3. Return "Job" if the user input asks about jobs, job.  
   IMPORTANT: If the question includes both jobs and tasks (e.g., tasks belonging to a job, job-task relationships, nested task structures within jobs), return "Job".

4. Return "Tasks" if the user asks about tasks only (e.g., task details, task status, task attributes).

5. Return "TaskSuitableResurce" if the question concerns:
   - both tasks AND resources
   - which resource can execute a task
   - where a task can be executed
   - how long a task takes
   - execution time or duration of a task

6. Return "TaskPrecedenceConstraint" if the question concerns:
   - the order of tasks
   - dependencies between tasks
   - which task must happen before/after another task

7. Return "None" if the question does not clearly belong to any category above.

Output format:
Return exactly one of the allowed words and nothing else.
"""

system_content_verbose = """You are a classifier. Your task is to analyze a user's question and return EXACTLY ONE word from the predefined list below as well as your thinking process. 

Your output should be of the form: {pick: the word itself, think: your thinking process of why picking that word}

Possible outputs:
- Workcenter
- Resource
- Job
- Tasks
- TaskSuitableResurce
- TaskPrecedenceConstraint
- None

Classification rules:

1. Return "Workcenter" if the user asks about workcenters.

2. Return "Resource" if the user asks about resources, resource.

3. Return "Job" if the user input asks about jobs, job or information regarding them.  
   IMPORTANT: If the question includes both jobs and tasks (e.g., tasks belonging to a job, job-task relationships, nested task structures within jobs), return "Job".

4. Return "Tasks" if the user asks about tasks only (e.g., task details, task status, task attributes).

5. Return "TaskSuitableResurce" if the question concerns:
   - both tasks AND resources
   - which resource can execute a task
   - where a task can be executed
   - how long a task takes
   - execution time or duration of a task

6. Return "TaskPrecedenceConstraint" if the question concerns:
   - the order of tasks
   - dependencies between tasks
   - which task must happen before/after another task

7. Return "None" if the question does not clearly belong to any category above.

Output format:
Return exactly one of the allowed words and nothing else.
"""
user_content = 'what tasks can i do in the meltshop?'
system_content_asuserprompt = f"""You are a classifier. Your task is to analyze a user's question and return EXACTLY ONE word from the predefined list below as well as your thinking process. 

Your output should be of the form: <pick: the word itself, think: your thinking process of why picking that word>. The word you pick should always match the one you ended up choosing based on your thinking process. Think before you pick. Never make assumptions.

Possible outputs:
- 1
- 2
- 3
- 4
- 5
- 6
- 7

Classification rules:

1. Return "1" if the user specifically lists the word 'workcenter' in the question.

2. Return "2" if the user asks about resources. If the question includes availability, when a resource can be used return "2". a resource might also be refered to as a location like a meltshop.

3. Return "3" if the user input asks about jobs.  
   IMPORTANT: If the question includes both jobs and tasks (e.g., tasks belonging to a job, job-task relationships, nested task structures within jobs), return "Job".

4. Return "4" if the user asks about tasks only.

5. Return "5" if the question concerns one or more of the following:
   - both tasks AND resources
   - which resource can execute a task
   - the location in which (where) a task can be executed
   - how long a task takes
   - execution time or duration of a task

6. Return "6" if the question concerns:
   - the order of tasks
   - dependencies between tasks
   - which task must happen before/after another task

7. Return "7" if the question does not clearly belong to any category above. If the question is gibberish or random, single characters or numbers return "7". If the question is a single number always return "7"

User Question:
{user_content}
"""

# The final prompt is the prompt: system_content_asuserprompt
# Questions tested the prompt on: results seem to be consistent #
'''
### QUESTIONS POSSIBLE ###

# RESOURCE #
vars possible: name, id, resourceavailability

# user_content = 'List all resources'
# user_content = 'What is the name of each resource'
# user_content = 'when is resource 1 available?'
# user_content = 'when can i use resource 1?'
# user_content = 'when can i use the meltshop?'

# JOBS #
vars possible: name, arrivaldate, duedate, jobtaskreference, jobworkcenterreference, id

# user_content = 'How many jobs are there?' ## Job
# user_content = 'Return all job ids?' ## Job
# user_content = 'Return all Job names' ## Job
# user_content = 'Return all job ids' ## Job
# user_content = 'List the arrival dates of each job' ## Job
# user_content = 'Which job starts first?' ## Job
# user_content = 'List all job due dates?' ## Job
# user_content = 'Which job needs to finish first?' ## Job
# user_content = 'Return the 1st job in the json file' ## Job
# user_content = 'List the tasks of each Job' ## Job
# user_content = 'List the id of each job and its tasks' ## Job
# user_content = 'Return the name and id of each job and the task corresponding to each job' ## Job

# TASKS #
vars possible: name, id

# user_content = 'Return all task ids?' ## Tasks
# user_content = 'How many tasks are there?' ## Tasks
# user_content = 'List all task names' ## Tasks
# user_content = 'Ouput the first task in the json file' ## Tasks
# user_content = 'In which resource can task 1 be executed in?' ## Tasks

# TASKSUITABLERESOURCES #
vars possible: resourcereference, taskreference, operationtimeperbatchinseconds, setupcode

# user_content = 'Which tasks can be done in resource 1?' ##
# user_content = 'Where can task 1 be executed'
# user_content = 'Which resource can execute task 1?'
# user_content = 'Can Task 1 be executed in the MELTSHOP?'
# user_content = 'How long does task 1 take?'

# TASKSPRECEDENCECONSTRAINTS #
vars possible: preconditiontaskreference, postconditiontaskreference

# user_content = 'Which task should i execute before task 1?'
# user_content = 'Is there a task to be executed before task 3?'

## NONE ##

# user_content = 'Hi, how are you?'
# user_content = 'What is this file about?'
# user_content = 'How are you'
# user_content = 'asijhduasjh'
# user_content = 'a'
# user_content = 'aaa'
# user_content = '90809809'
# user_content = '1'
# user_content = 'Who is Pikachu?'
# user_content = 'Where can i buy Gucci'
# user_content = '111111'
# user_content = '11'
# user_content = 'vuvuvuvuvu'

# user_content = 'What is the name of each resource?' ## Resource
# user_content = 'Which task can I execute in resource 2?' ## TaskSuitableResurce
'''

# llm_answer = chat('llama3.1', messages = [{'role': 'system', 'content': system_content_verbose}, {'role': 'user', 'content': user_content}])
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': system_content_asuserprompt}])
#except ollama._types.ResponseError:
#    print('agugu')

#print(llm_answer)
print('==============')
print(user_content)
print(llm_answer.message.content)