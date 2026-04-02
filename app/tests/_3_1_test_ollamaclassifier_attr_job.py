from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = "Return the job with arrival date 31/3"
# user_question = "List all jobs"
# user_question = "Give me the jobs"
# user_question = "Return the job with id 8"
# user_question = "Are there any jobs with arrival date 31 2"
# user_question = "List jobs with id 51"
# user_question = "Find jobs that require task 581"
# user_question = "Find jobs that require task with id 581"
# user_question = "Find the last job that requires task with id 581"
# user_question = "Return the first job"
# user_question = "Return the job at index 5"
# user_question = "Return the first job that requires the task with id 580"
# user_question = "Return job 5" #<---implies id here
# user_question = "Return 4 jobs"
# user_question = "Return me the FROM BILLET job" #<---understand theres name here

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

print(user_prompt)
print('==============')

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': user_prompt}])

print('**********************')
print(len(tokenizer.tokenize(json.dumps(user_prompt))))
aa = llm_answer.message.content
print(aa)
print(aa.replace('\n', ''))
