from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = 'Which tasks can be done in resource 901?' # {"attribute": true, "know": {"info": "resource", "key": "id", "value": 901}, "search": {"info": "task"}, "think": "identified a specific attribute (id) and extracted the reference point of the query as a resource with id 901"}
# user_question = 'Where can task 57 be executed' #{"attribute": true, "know": {"info": "task", "key": "id", "value": 57}, "search": {"info": "resource"}, "think": "Looking for a resource where task 57 can be executed"}
# user_question = 'Which resource can execute task with id 39?' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 39}, "search": {"info": "resource"}, "think": "Identified specific attribute 'id 39' related to a task. Now searching for resources that can execute this task"}
# user_question = 'Which resource can execute task 39?' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 39}, "search": {"info": "resource"}, "think": "identified specific attribute 'task id' and user wants to find 'resource'" }
# user_question = 'Can Task 11 be executed in the MELTSHOP?' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 11}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to know its executable resources. We have identified the task ID as 11."}
# user_question = 'How long does task 52 take?' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 52}, "search": {"info": "time"}, "think": "The user is asking for the completion time of a specific task with id 52."}
# user_question = 'What resource can execute each task?' # {"attribute": false} # <-- No thinking
# user_question = 'Return all resources and tasks' # {"attribute": false} # <-- No thinking
# user_question = 'Return all resources and their tasks' # {"attribute": false, "think": "The question is asking for a general list of resources and their tasks without specifying any attribute or reference point. It cannot be answered based on the provided rules."}
# user_question = 'Return the id of the resource that can execute task 91' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 91}, "search": {"info": "resource"}, "think": "The user is asking for information about a specific task and wants to find the resource that can execute it. We know the task id is 91."}
# user_question = 'What task can be executed in the ROLLING MILL' # {"attribute": true, "know": {"info": "resource", "key": "name", "value": "ROLLING MILL"}, "search": {"info": "task"}, "think": "User is looking for a specific task that can be executed in the resource named ROLLING MILL"}
# user_question = 'Return the ids of all resources and tasks' # {"attribute": false, "think": "The user is asking for a general query about retrieving ids without specifying any attribute"}
# user_question = 'Return all resources where task 77 can be executed' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 77}, "search": {"info": "resource"}, "think": "The user is asking for a specific task and wants to find the resources where this task can be executed."}
# user_question = 'Return the id of every resource where task 77 can be executed' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 77}, "search": {"info": "resource"}, "think": "Identified a specific task ID and need to find resources that support it"}
# user_question = 'What is the operation time for task 73' # {"attribute": true, "know": {"info": "task", "key": "id", "value": 73}, "search": {"info": "time"}, "think": "Extracted specific task id (73) and determined user wants to find operation time"}
# user_question = 'What tasks need to operate for more than 30minutes?' # {"attribute": true, "know": {"info": "time", "key": "value", "value": 30}, "search": {"info": "task"}, "think": ["Identified specific attribute: time", "Extracted known attribute value: 30 minutes", "Determined user wants to find tasks"] }
user_question = 'Return the names of all resources and their tasks' # {"attribute": false}
user_question = 'How long does each task take?' # {"attribute": false, "think": "The user is asking for information about task completion time in general, without specifying any specific attribute or reference point."}

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

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Be consistent with lowercase values: "resource", "task", "time"
- If no specific attribute is identified, return only {"attribute": false} only
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:

-----
User question: "Which tasks can be done in resource 13?"
Output: {"attribute": true, "know": {"info": "resource", "key": "id", "value": 13}, "search": {"info": "task"}, "think": <Your thinking process>}
-----
User question: "Where can task 57 be executed?"
Output: {"attribute": true, "know": {"info": "task", "key": "id", "value": 57}, "search": {"info": "resource"}, "think": <Your thinking process>}
-----
User question: "How long does task 90 take?"
Output: {"attribute": true, "know": {"info": "task", "key": "id", "value": 90}, "search": {"info": "time"}, "think": <Your thinking process>}
-----
User question: "What resource can execute each task?"
Output: {"attribute": false, "think": <Your thinking process>}
-----
User question: "What tasks can be executed in the MELTSHOP?"
Output: {"attribute": true, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": <Your thinking process>}
-----
User question: "What resource can execute each task?"
Output: {"attribute": false, "think": <Your thinking process>}"""
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

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Be consistent with lowercase values: "resource", "task", "time"
- If no specific attribute is identified, return only {"attribute": false} only
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:

-----
User question: "Which tasks can be done in resource 13?"
Output: {"attribute": true, "know": {"info": "resource", "key": "id", "value": 13}, "search": {"info": "task"}, "think": <Your thinking process>}
-----
User question: "Where can task 57 be executed?"
Output: {"attribute": true, "know": {"info": "task", "key": "id", "value": 57}, "search": {"info": "resource"}, "think": <Your thinking process>}
-----
User question: "How long does task 90 take?"
Output: {"attribute": true, "know": {"info": "task", "key": "id", "value": 90}, "search": {"info": "time"}, "think": <Your thinking process>}
-----
User question: "What resource can execute each task?"
Output: {"attribute": false, "think": <Your thinking process>}
-----
User question: "What tasks can be executed in the MELTSHOP?"
Output: {"attribute": true, "know": {"info": "resource", "key": "name", "value": "MELTSHOP"}, "search": {"info": "task"}, "think": <Your thinking process>}
-----
User question: "What resource can execute each task?"
Output: {"attribute": false, "think": <Your thinking process>}"""
   user_prompt+=f"""

____________________
User Question:
{user_question}"""
   
   return user_prompt