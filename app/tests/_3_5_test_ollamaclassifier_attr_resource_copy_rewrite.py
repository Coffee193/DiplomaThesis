from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = "Return all resources" # {"attribute": false,"think": "The user asked to return 'all resources', which does not specify a specific resource based on an attribute (id or name)."}
# user_question = "Return all resource ids" # {"attribute": false,"think": "The user is asking to return all resources, but did not specify a particular attribute. The keyword 'ids' implies returning ids of all resources."}
user_question = "Return resouce 2" #<-- classified as id=2 # {  "attribute": true,  "key": "id",  "value": 2,  "think": "The user is searching for a specific resource by its id, which is mentioned as 'resource 2'. Assuming the mention of the number '2' refers to the id of the resource."}
# user_question = "What is the name of the resource with id 3" # {"attribute": true,"key": "id","value": 3, "think": "The user is asking for a specific resource by its id (3), so I will extract the id as the key."}
# user_question = "Return resource with id 7" # {"attribute": true,"key": "id","value": 7, "think": "The user is searching for a specific resource using its id attribute with value 7"}
# user_question = "Return resource ROLLING MILL" # {"attribute": true,"key": "name","value": "ROLLING MILL","think": "The user is searching for a specific resource by name, so I extracted the attribute (name) and its value from the question."}
# user_question = "Return resource rolling mill" # {"attribute": true,"key": "name","value": "rolling mill", "think": "The question mentions a specific resource by name, so I will extract the key and value based on the attribute 'name'."}
# user_question = "How many resources are there" # {"attribute": false, "think": "The user is asking for a count of resources, not specifying any particular attribute or resource."}
# user_question = "Return the first resource" # {"attribute": false,"think": "The question asks for the 'first' resource, but it does not specify which attribute to use. It could be referring to any attribute or no specific attribute at all."}
# user_question = "Return 1 resource" # { "attribute": false, "think": "The question 'Return 1 resource' does not specify a particular attribute or value. It is a general request without any specific reference to id or name."}
# user_question = "Return 1 resources" # {"attribute": false,"think": "The question mentions 'resources', but it does not specify an attribute (id or name) to search for. Therefore, I assume it's a request to return all resources."}

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

2. If the user does not specify a particular attribute of a resource (e.g., “Return all resources”), return:
{"attribute": false}

3. The key must be one of the following:

- name
- id

4. Always return ONLY valid JSON with no explanation.

5. If the user does NOT mention any of these keywords (id, name) do NOT make assumptions. If the key is NOT referenced do NOT assume anything. Do NOT confuse index with id, they are completely different things

6. Find the key and values of attributes of the resources he's searching for, NOT the key/values he wants returned

Output Format:

- If "attribute" is true, return:
{"attribute": true,"key": <string>,"value": <string or integer>, "think": <Your thinking process>}

- If "attribute" is false, return:
{"attribute": false, "think": <Your thinking process>}

NOTE: As you can see, if "attribute" is false ommit: "key" and "value"

Examples

-----
User question:
Return resource with id 7

Output:
{"attribute": true,"key": "id","value": 7}
-----

User question:
Return resource ROLLING MILL

Output:
{"attribute": true,"key": "name","value": "ROLLING MILL"}
-----

User question:
What is the name of the resource with id 3

Output:
{"attribute": true,"key": "id","value": 3}
-----

User question:
Return all resources

Output:
{"attribute": false}
-----

User question:
Return resource 1

Output:
{"attribute": true,"key": "id","value": 1}
-----

Remember:

Only detect whether the question refers to a specific resource by attribute.
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