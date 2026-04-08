from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

#user_question = "Return the job with arrival date 31/3"
#user_question = "List all jobs"
#user_question = "Give me the jobs"
#user_question = "Return the job with id 8"
#user_question = "Are there any jobs with arrival date 31 2"
user_question = "List jobs with id 51"
#user_question = "Find jobs that require task 581"
#user_question = "Find jobs that require task with id 581"
#user_question = "Find the last job that requires task with id 581"
#user_question = "Return the first job"
#user_question = "Return the job at index 5"
#user_question = "Return the first job that requires the task with id 580"
#user_question = "Return job 5" #<---implies id here
#user_question = "Return 4 jobs"
#user_question = "Return me the FROM BILLET job" #<---understand theres name here
#user_question = "Return the name of the job that requires task 32"
#user_question = "Return the id of all jobs"

user_prompt = """You are an information extraction assistant.

The user will provide a question about the jobs.

Each job is basically a dictionary that contains the following keys:

- name: The name of the job
- arrivaldate: The earliest date the job can start
- duedate: The latest date the job should be finished
- task: The id of the tasks that will be executed during the job
- workcenter: The id of the workcenter where the job will be executed
- id: The id of the job

Your task is to analyze the user's question and determine whether the user wants returned:
- A specific attribute of one or more jobs (e.g., name, id, duedate, etc.), OR
- The entire job object

Rules:
- Focus ONLY on what the user wants returned, not on filtering conditions or any other information mentioned. Only on what the user wants returned
- If the user asks for a specific attribute (e.g., "name", "task", "duedate"), set "attribute": true and specify which attribute in "return".
- If the user asks for the full job (even if filtered by some condition like id), set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above.
- If "attribute": false, do NOT include a "return" value.
Output format:

Return ONLY a valid JSON object and nothing else. Do not explain.
The JSON should be of the form:

{"attribute": <boolean>, "return": <string (if applicable)>}

NOTE: After returning the JSON object always explain your thinking process

Examples:
-------------
User: "Return the name of the job with id 63"
Output: {"attribute": true, "return": "name"}
-------------
User: "Return the job with id 73"
Output: {"attribute": false}
-------------
User: "What tasks can be executed in job 33?"
Output: {"attribute": true, "return": "task"}
-------------
User: "What is the name of the job with id 12?"
Output: {"attribute": true, "return": "name"}
-------------
User: "Return all jobs"
Output: {"attribute": false}
-------------
User: "What is the duedate of job 502"
Output: {"attribute": true, "return": "duedate"}"""
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

# and nothing else. Do not explain.
# . Then explain why you returned that value