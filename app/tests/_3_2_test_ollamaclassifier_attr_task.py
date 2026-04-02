from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = "Return task with id 584"
# user_question = "task with name Rolling"
# user_question = "Return first task with name Rolling"
# user_question = "Return first task"
# user_question = "tasks"
# user_question = "return task 7" # <--- recognises it as id
# user_question = "return 7 task" # <--- recognises it as id
# user_question = "return 7 tasks"
# user_question = "return the last task"

user_prompt = """You are an information extraction assistant.

The user will provide a question about tasks.

Each task is basically a dictionary that contains the following keys:

- name: The name of the task
- id: The id of the task

Your job is NOT to answer the question directly, but to analyze the user's question and determine whether the user is requesting information about a specific task identified by an attribute.

Rules:

1. If the user is searching for a specific task using an attribute and value (for example: id, name), extract:
- the key (attribute name)
- the value of that attribute
- the field the user wants returned

2. If the user does not specify a particular task (for example: "Return all tasks"), then set:
{"attribute": false}

3. The key must be one of the following:

- name
- id

4. The return field should indicate what information the user wants:
   "*" → return all information about the task
   "name", "id" etc. → return only that field

5. If the user identifies a task but does not specify which field to return, assume they want all information and set "return": "*".

6. Always return ONLY valid JSON with no explanation.

7. If the user does NOT mention any of these keywords (id, name) do NOT make assumptions. If the key is NOT referenced do NOT assume anything.


Output Format

{"attribute": <boolean>,"key": <string>,"value": <string or integer>,"return": <string>, "think": <Your thinking process>}

If "attribute" is false, return:

{"attribute": false, "think": <Your thinking process>}

Examples

-----
User question:
Return the task with id 13

Output:
{"attribute": true,"key": "id","value": 13,"return": "*"}
-----

User question:
What is the name of the task with id 12?

Output:
{"attribute": true,"key": "id","value": 12,"return": "name"}
-----

User question:
What are the ids of MELTING?

Output:
{"attribute": true,"key": "name","value": "MELTING","return": "id"}
-----

User question:
Return all tasks

Output:
{"attribute": false}
-----

Remember:

Only detect whether the question refers to a specific task by attribute.
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
