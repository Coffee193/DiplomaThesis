from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

user_question = "Return task with id 584"
user_question = "task with name Rolling"
user_question = "Return first task with name Rolling"
user_question = "Return first task"
user_question = "tasks"
user_question = "return task 7" # <--- recognises it as id
user_question = "return 7 task" # <--- recognises it as id
user_question = "return 7 tasks"
user_question = "return the last task"
user_question = "return the id of the task with name ROLLING"
#user_question = "return the names of all tasks"

user_prompt = """You are an information extraction assistant.

The user will provide a question about the tasks.

Each task is basically a dictionary that contains the following keys:

- name: The name of the task
- id: The id of the task

Your aim is to analyze the user's question and determine whether the user wants returned:
- A specific attribute of one or more tasks (e.g., name, id), OR
- The entire task object

Rules:
- Focus ONLY on what the user wants returned, not on filtering conditions or any other information mentioned. Only on what the user wants returned
- If the user asks for a specific attribute (e.g., "name", "id"), set "attribute": true and specify which attribute in "return".
- If the user asks for the full task (even if filtered by some condition like id), set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above.
- If "attribute": false, do NOT include a "return" value.
Output format:

Return ONLY a valid JSON object and nothing else. Do not explain.
The JSON should be of the form:

{"attribute": <boolean>, "return": <string (if applicable)>}

NOTE: After returning the JSON object always explain your thinking process

Examples:
-------------
User: "Return the name of the task with id 63"
Output: {"attribute": true, "return": "name"}
-------------
User: "Return the task with id 73"
Output: {"attribute": false}
-------------
User: "Return tasks that have the name ROLLING?"
Output: {"attribute": false}
-------------
User: "Return first task with name Rolling"
Output: {"attribute": false}
-------------
User: "Return the id of the last task"
Output: {"attribute": true, "return": "id"}
-------------
User: "What is the last task"
Output: {"attribute": false}"""
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