from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = "Return task with id 584" # {  "attribute": true,  "key": "id",  "value": "584",  "think": "The user is searching for a specific task using its id, which is provided as '584'."}
# user_question = "task with name Rolling" # {"attribute": true,"key": "name","value": "Rolling", "think": "The user is searching for a task by its name attribute. I found the keyword 'name' and the value 'Rolling'. I assume this is referring to a specific task."}
# user_question = "Return first task with name Rolling" # {"attribute": true,"key": "name","value": "Rolling","think": "The user is searching for a specific task by its name. The keyword 'first' is not explicitly mentioned as an attribute, so I'm assuming it's part of the value. I've extracted the key as 'name' and the value as 'Rolling'. I did not assume any other attribute or value."}
# user_question = "Return first task" # "attribute": false,"think": "The user question does not specify any attribute (id or name) to search for a specific task. Therefore, it is likely asking for all tasks or an unspecified condition."}
# user_question = "tasks" # {  "attribute": false,  "think": "The user question is asking for a general query about tasks, without specifying any attribute or value. Therefore, I assume no specific task is being referred to."}
# user_question = "return task 7" # <--- recognises it as id # {"attribute": true,"key": "id","value": 7,"think": "The user is searching for a specific task by id, so I extracted the 'id' attribute and its value as 7."}
user_question = "return 7 task" # {"attribute": false,"think": "The question 'return 7 task' does not specify a particular attribute or value related to tasks. It only mentions a number (7), but it's unclear what this number refers to without more context."}
# user_question = "return 7 tasks" # {"attribute": false,"think": "The question does not specify a particular attribute or task, so I will assume it is asking for general information about all tasks."}
# user_question = "return the last task" # {  "attribute": false,  "think": "The question 'return the last task' does not specify a particular attribute or value, so it is likely asking for all tasks or a specific task without referencing an attribute."} 
# user_question = 'Return all ROLLING tasks' # {"attribute": true,"key": "name","value": "ROLLING", "think": "The user is searching for a specific task with the name 'ROLLING', as indicated by the phrase 'all ROLLING tasks'."}
# user_question = 'Return the id of all tasks with name ROLLING' # {"attribute": true,"key": "name","value": "ROLLING", "think": "The user is searching for specific tasks using their names, which are provided as 'ROLLING'."}
# user_question = 'What is the name of the task with id 77' # {"attribute": true,"key": "id","value": 77,"think": "The user is searching for a specific task using its id, which is provided as '77'."}
# user_question = 'What are the ids of MELTING' # {"attribute": true,"key": "name","value": "MELTING", "think": "The user is searching for a specific task using its name, which is provided as 'MELTING'."}
# user_question = 'Return all tasks' # {"attribute": false,"think": "The user is asking for a general query without specifying any specific task attribute."}
# user_question = 'Return the name of every task' # {"attribute": false,"think": "The user is asking for a general query without specifying any specific task attribute."}

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

2. If the user does not specify a particular attribute of a task (for example: "Return all tasks"), then set:
{"attribute": false}

3. The key must be one of the following:

- name
- id

4. Always return ONLY valid JSON with no explanation.

5. If the user does NOT mention any of these keywords (id, name) do NOT make assumptions. If the key is NOT referenced do NOT assume anything. Do NOT confuse index with id, they are completely different things

6. Find the key and values of attributes of the jobs he's searching for, NOT the key/values he wants returned

Output Format

- If "attribute" is true, return:
{"attribute": <boolean>,"key": <string>,"value": <string or integer>, "think": <Your thinking process>}

-If "attribute" is false, return:
{"attribute": false, "think": <Your thinking process>}

NOTE: As you can see, if "attribute" is false ommit: "key" and "value"

Examples

-----
User question:
Return the task with id 13

Output:
{"attribute": true,"key": "id","value": 13, "think": "The user is searching for a specific task using its id, which is provided as '584'."}
-----

User question:
What is the name of the task with id 12?

Output:
{"attribute": true,"key": "id","value": 12, "think": "The user is searching for a specific task using its id, which is provided as '77'."}
-----

User question:
What are the ids of MELTING?

Output:
{"attribute": true,"key": "name","value": "MELTING", "think": "The user is searching for a specific task using its name, which is provided as 'MELTING'."}
-----

User question:
Return all tasks

Output:
{"attribute": false, "think": "The user is asking for a general query without specifying any specific task attribute."}
-----

User question:
Return the name of every task

Output:
{"attribute": false, "think": "The user is asking for a general query without specifying any specific task attribute."}
-----

Remember:

Only detect whether the question refers to a specific task by attribute.
Extract the key, value field.
Output strict JSON only.
Although not mentioned in the examples, ALWAYS place your thinking process in the think key of the JSON string."""
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


def getPrompt(user_question):
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
   
   return user_prompt