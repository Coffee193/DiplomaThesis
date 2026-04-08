from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

#user_question = "Return all resources"
#user_question = "Return all resource ids" <--- Problematic, probably tackle the return elesewhere
#user_question = "Return resouce 2" #<-- classified as id=2
#user_question = "What is the name of the resource with id 3"
#user_question = "Return resource with id 7"
#user_question = "Return resource ROLLING MILL"
#user_question = "Return resource rolling mill"
#user_question = "How many resources are there"
#user_question = "Return the first resource"
#user_question = "Return 1 resource"
#user_question = "Return 1 resources"

'''
user_prompt = """You are an information extraction assistant.

The user will provide a question about resources.

Each resource is basically a dictionary that contains the following keys:

- name: The name of the resource
- id: The id of the resource

Your job is NOT to answer the question directly, but to analyze the user's question and determine whether the user is requesting information about a specific resource identified by an attribute.

Rules:

1. If the user is searching for a specific resource using an attribute and value (for example: id, name), extract:
- key: the attribute used (id or name)
- value: the value of the attribute (integer for id, string for name)
- the field the user wants returned

2. If the user is not asking for a specific resource based on an attribute (e.g., “Return all resources”), return:
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
If the key is NOT referenced think very carefully if the user is refering to an index/position or id. If you believe he's refering to a position in the list of resources return {'attribute': false}


Output Format

{"attribute": <boolean>,"key": <string>,"value": <string or integer>,"return": <string>, "think": <Your thinking process>}

If "attribute" is false, return:

{"attribute": false, "think": <Your thinking process>}

Examples

-----
User question:
Return resource with id 7

Output:
{"attribute": true,"key": "id","value": 7,"return": "*"}
-----

User question:
Return resource ROLLING MILL

Output:
{"attribute": true,"key": "name","value": "ROLLING MILL","return": "*"}
-----

User question:
What is the name of the resource with id 3

Output:
{"attribute": true,"key": "id","value": 3,"return": "name"}
-----

User question:
Return all resources

Output:
{"attribute": false}
-----

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

The user will provide a question about resources.

Each resource is basically a dictionary that contains the following keys:

- name: The name of the resource
- id: The id of the resource

Your job is NOT to answer the question directly, but to analyze the user's question and determine whether the user is requesting information about a specific resource identified by an attribute.

Rules:

1. If the user is searching for a specific resource using an attribute and value (for example: id, name), extract:
- key: the attribute used (id or name)
- value: the value of the attribute (integer for id, string for name)
- the field the user wants returned

2. If the user is not asking for a specific resource based on an attribute (e.g., “Return all resources”), return:
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
If the key is NOT referenced think very carefully if the user is refering to an index/position or id. If you believe he's refering to a position in the list of resources return {'attribute': false}


Output Format

{"attribute": <boolean>,"key": <string>,"value": <string or integer>,"return": <string>, "think": <Your thinking process>}

If "attribute" is false, return:

{"attribute": false, "think": <Your thinking process>}

Examples

-----
User question:
Return resource with id 7

Output:
{"attribute": true,"key": "id","value": 7,"return": "*"}
-----

User question:
Return resource ROLLING MILL

Output:
{"attribute": true,"key": "name","value": "ROLLING MILL","return": "*"}
-----

User question:
What is the name of the resource with id 3

Output:
{"attribute": true,"key": "id","value": 3,"return": "name"}
-----

User question:
Return all resources

Output:
{"attribute": false}
-----

Although not mentioned in the examples, place your thinking process in the think key of the JSON string"""
   user_prompt+=f"""

____________________
User Question:
{user_question}"""

   return user_prompt