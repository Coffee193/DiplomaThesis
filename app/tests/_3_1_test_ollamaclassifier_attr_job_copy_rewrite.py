from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = "Return the job with arrival date 31/3" # {"attribute": true,"key": "arrivaldate","value": "31/3","think": "The question is asking for a specific job based on its arrival date, which is mentioned as '31/3'. This matches one of the allowed attributes."}
# user_question = "List all jobs" # {"attribute": false, "think": "The question does not specify a particular attribute or job to search for. It is asking for a general list of jobs."}
# user_question = "Give me the jobs" # {"attribute": false, "think": "The user is requesting a list of all jobs without specifying any specific attribute or value. The question does not contain any keywords referring to job attributes."}
# user_question = "Return the job with id 8" # {"attribute": true,"key": "id","value": 8,"think": "The user is asking for a specific job by its id, which is mentioned as '8'"}
# user_question = "Are there any jobs with arrival date 31 2" # {"attribute": true,"key": "arrivaldate","value": "31 2", "think": "The user is looking for a specific job based on the arrival date attribute."}
# user_question = "List jobs with id 51" # {"attribute": true,"key": "id","value": 51, "think": "The user is searching for a specific job using an attribute and value. The keyword 'id' was found which matches one of the allowed keys."}
# user_question = "Find jobs that require task 581" # {"attribute": true,"key": "task","value": "581","think": "The user is searching for jobs based on a specific task ID, so I'm assuming they want to find all jobs with the task ID equal to 581."}
# user_question = "Find jobs that require task with id 581" # {"attribute": true,"key": "task","value": 581,"think": "The user is searching for jobs based on a specific task ID. This implies they are looking for jobs where this task is required."}
# user_question = "Find the last job that requires task with id 581" # {"attribute": true,"key": "task","value": 581,"think": "The question mentions a specific task (id 581), which implies it's looking for a job related to this task. The key 'task' is identified as the attribute being searched, and the value is the id of the task."}
# user_question = "Return the first job" # {"attribute": false,"think": "The user is requesting to return all jobs, but there is no specification of a particular attribute or value. The keyword 'first' does not correspond to any of the specified keys (id, name, arrivaldate, duedate, task, workcenter)." }
# user_question = "Return the job at index 5" # {"attribute": false,"think": "The user did not specify an attribute that can uniquely identify a job. The keyword 'index' was used instead of 'id', which are two different concepts."}
# user_question = "Return the first job that requires the task with id 580" # {"attribute": true,"key": "task","value": 580,"think": "The user is searching for a specific job based on its task, so I extracted the 'task' key and value."}
# user_question = "Return job 5" #<---implies id here # {"attribute": true,"key": "id","value": 5, "think": "The user is asking for a specific job by its id."}
# user_question = "Return 4 jobs" # {"attribute": false,"think": "The question asks for a number of jobs, but does not specify any attribute. Therefore, it is a request to return all jobs without specifying a particular job."}
# user_question = "Return me the FROM BILLET job" #<---understand theres name here # {"attribute": true,"key": "name","value": "FROM BILLET", "think": "The user is asking for a specific job by name, 'FROM BILLET'."}
# user_question = 'Return the names of every job' # {"attribute": false,"think": "The user is asking for all jobs without specifying a particular attribute or value. No specific job by attribute has been mentioned."}
# user_question = 'Return the task of job 509' # {"attribute": true,"key": "id","value": 509,"think": "The user is looking for a specific job with id 509 and wants to know the task associated with it."}
# user_question = 'Return the id of all jobs with name ROLLING' # {"attribute": true,"key": "name","value": "ROLLING", "think": "The user is searching for a specific job by name, so I extracted the key as 'name' and the value as 'ROLLING'. The question suggests that the user wants to return something related to jobs with this name, but it's not clear if they want all attributes or just one."}
# user_question = 'Return the first task of every job' # {"attribute": false, "think": "The user is asking for a general query about tasks, but does not specify any attribute or value related to a specific job. It's likely that they want all jobs, which means we cannot identify a specific key-value pair related to an attribute."}
# user_question = 'Return the tasks of all jobs with name ROLLING' # {"attribute": true,"key": "name","value": "ROLLING", "think": "The user is looking for a specific job by name, so I need to extract the key 'name' and the value 'ROLLING'."}
# user_question = 'Return all FROM BILLET jobs' # {"attribute": true,"key": "name","value": "FROM BILLET", "think": "The user is searching for a job with a specific name, so I'm extracting the key 'name' and its corresponding value 'FROM BILLET'."}
# user_question = 'Return all jobs with name FROM BILLET' # {"attribute": true,"key": "name","value": "FROM BILLET", "think": "The user is searching for a specific job by its name, which is 'FROM BILLET'"}
# user_question = 'Return all ROLLING jobs' # {"attribute": true,"key": "name","value": "ROLLING", "think": "The question asks for all ROLLING jobs, implying a search by job name."}
user_question = 'Return all job ids'
user_question = 'Return the job with id _90'

user_prompt = """You are an information extraction assistant.

The user will provide a question about the jobs.

Each job is basically a dictionary that contains the following keys:

- name: The name of the job
- arrivaldate: The earliest date the job can start
- duedate: The latest date the job should be finished
- task: The id of the tasks that will be executed during the job
- workcenter: The id of the workcenter where the job will be executed
- id: The id of the job

Your task is NOT to answer the question directly, but to analyze the user's question and determine whether the user is requesting information about a specific job identified by an attribute.

Rules:

1. If the user is searching for a specific job using an attribute and value (for example: id, name, workcenter, etc.), extract:
- the key (attribute name)
- the value of that attribute

2. If the user does not specify a particular attribute of a job (for example: "Return all jobs"), then set:
{"attribute": false}

3. The key must be one of the following:

- name
- arrivaldate
- duedate
- task
- workcenter
- id

4. Always return ONLY valid JSON with no explanation.

5. If the user does NOT mention any of these keywords (id, name, etc..) do NOT make assumptions. If the key is NOT referenced do NOT assume anything. Do NOT confuse index with id, they are completely different things

6. Find the key and values of attributes of the jobs he's searching for, NOT the key/values he wants returned


Output Format:

- If "attribute" is true, return:
{"attribute": true,"key": <string>,"value": <string or integer>, "think": <Your thinking process>}

- If "attribute" is false, return:
{"attribute": false, "think": <Your thinking process>}

NOTE: As you can see, if "attribute" is false ommit: "key" and "value"

Examples

-----
User question:
Return the job with id 63

Output:
{"attribute": true,"key": "id","value": 63}
-----

User question:
What tasks can be executed in job 33?

Output:
{"attribute": true,"key": "id","value": 33}
-----

User question:
What is the name of the job with id 12?

Output:
{"attribute": true,"key": "id","value": 12}
-----

User question:
Return all jobs

Output:
{"attribute": false}
-----

User question:
Return the ids of every job

Output:
{"attribute": false}
-----

User question:
Return all FROM BILLET jobs

Output:
{"attribute": true, "key": "name", "value": "FROM BILLET"}
-----

Remember:

Only detect whether the question refers to a specific job by attribute.
Extract the key, value field if possible (if they are mentioned).
Output strict JSON only.
Although not mentioned in the examples, place your thinking process in the think key of the JSON string"""
user_prompt+=f"""

____________________
User Question:
{user_question}"""

print(user_prompt)
print('==============')

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': user_prompt}])

print('**********************')
print(len(tokenizer.tokenize(json.dumps(user_prompt))))
aa = llm_answer.message.content
print(aa)
print(aa.replace('\n', ''))


'''
def getPrompt(user_question):
   user_prompt = """You are an information extraction assistant.

The user will provide a question about the jobs.

Each job is basically a dictionary that contains the following keys:

- name: The name of the job
- arrivaldate: The earliest date the job can start
- duedate: The latest date the job should be finished
- task: The id of the tasks that will be executed during the job
- workcenter: The id of the workcenter where the job will be executed
- id: The id of the job

Your task is NOT to answer the question directly, but to analyze the user's question and determine whether the user is requesting information about a specific job identified by an attribute.

Rules:

1. If the user is searching for a specific job using an attribute and value (for example: id, name, workcenter, etc.), extract:
- the key (attribute name)
- the value of that attribute
- the field the user wants returned

2. If the user does not specify a particular job (for example: "Return all jobs"), then set:
{"attribute": false}

3. The key must be one of the following:

- name
- arrivaldate
- duedate
- task
- workcenter
- id

4. The return field should indicate what information the user wants:
   "*" → return all information about the job
   "name", "task", "duedate", etc. → return only that field

5. If the user identifies a job but does not specify which field to return, assume they want all information and set "return": "*".

6. Always return ONLY valid JSON with no explanation.

7. If the user does NOT mention any of these keywords (id, name, etc..) do NOT make assumptions. If the key is NOT referenced do NOT assume anything.


Output Format

{"attribute": <boolean>,"key": <string>,"value": <string or integer>,"return": <string>, "think": <Your thinking process>}

If "attribute" is false, return:

{"attribute": false, "think": <Your thinking process>}

Examples

-----
User question:
Return the job with id 63

Output:
{"attribute": true,"key": "id","value": 63,"return": "*"}
-----

User question:
What tasks can be executed in job 33?

Output:
{"attribute": true,"key": "id","value": 33,"return": "task"}
-----

User question:
What is the name of the job with id 12?

Output:
{"attribute": true,"key": "id","value": 12,"return": "name"}
-----

User question:
Return all jobs

Output:
{"attribute": false}
-----

Remember:

Only detect whether the question refers to a specific job by attribute.
Extract the key, value, and requested return field.
Output strict JSON only.
Although not mentioned in the examples, place your thinking process in the think key of the JSON string"""
   user_prompt+=f"""

____________________
User Question:
{user_question}"""
   
   return user_prompt
'''