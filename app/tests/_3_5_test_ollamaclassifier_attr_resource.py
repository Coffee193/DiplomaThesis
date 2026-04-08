from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

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

   return user_prompt