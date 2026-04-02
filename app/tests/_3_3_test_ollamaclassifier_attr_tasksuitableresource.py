from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = 'Which tasks can be done in resource 901?'
# user_question = 'Where can task 57 be executed'
# user_question = 'Which resource can execute task with id 39?'
# user_question = 'Which resource can execute task 39?'
# user_question = 'Can Task 11 be executed in the MELTSHOP?'
# user_question = 'How long does task 52 take?'
# user_question = 'What resource can execute each task?'
# user_question = 'Return all resources and tasks'
# user_question = 'Return all resources and their tasks'
# user_question = 'Return the id of the resource that can execute task 91'
# user_question = 'What task can be executed in the ROLLING MILL'

user_prompt = """You are an information extraction assistant.

The user will provide a question about tasks and resources or task completion time.

Your goal is to determine whether the user is asking for information based on a specific attribute (for example: a specific task id, resource id, resource name etc.).

Instruction:

1. If the question is based on a specific attribute (e.g., “id 57”, “id 13”, “name MELTSHOP”):

- Set "attribute" to true
- Extract what the user already knows (the reference point of the query) (know)
Extract what the user is searching for (search)

2. If the question is general and not based on a specific attribute (doesnt know the attribute (key and value) of reference point):

Return only: {"attribute": false}


Extraction rules:

For "know":
- "info": what the user knows about -> must be either "resource" or "task"
- "key": how it is defined. must be either:
   - "id" if the value is numeric (eg. 13, 57)
   - "name" if the value is text (eg. MELTSHOP)
- "value": the actual value (string or integer)

For "search":
- "info": what the user wants to find → must be one of: "resource", "task", "time"

NOTE: If a field is not known or explicitly stated in the question do not make assumption. Instead return {"attribute": false}

Important rules:

- Always return a valid JSON object only
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Be consistent with lowercase values: "resource", "task", "time"
- If no specific attribute is identified, return only {"attribute": false} only

Examples:

-----
User question: "Which tasks can be done in resource 13?"
Output: {"attribute": true, "know": {"info": "resource", "key": "id", "value": 13}, "search": {"info": "task"}}
-----
User question: "Where can task 57 be executed?"
Output: {"attribute": true, "know": {"info": "task", "key": "id", "value": 57}, "search": {"info": "resource"}}
-----
User question: "How long does task 90 take?"
Output: {"attribute": true, "know": {"info": "task", "key": "id", "value": 90}, "search": {"info": "time"}}
-----
User question: "What resource can execute each task?"
Output: {"attribute": false}
-----
User question: "What tasks can be executed in the MELTSHOP?"
Output: {"attribute": true, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}}
-----
User question: "What resource can execute each task?"
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
