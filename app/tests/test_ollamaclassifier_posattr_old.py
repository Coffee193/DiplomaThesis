from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

'''
### JOB ###
vars possible: name, arrivaldate, duedate, jobtaskreference, jobworkcenterreference, id

# NONE
# user_question = "List all jobs" # {"query": "none", "think": "The question is asking for a list of jobs, but it's too vague to determine which type of query to use."}
# user_question = "Give me the jobs" # {"query": "none", "think": "The question is not specific enough to determine a query type, and it doesn't refer to an item by its position or attribute value"}

# POSITION
# user_question = "Return the first job" # {"query": "position", "value": 0, "think": "The user is asking for the first item in the list, so I'll interpret it as a position-based query with value 0."}
# user_question = "Return the job at index 5" # {"query": "position", "value": 5, "think": "The user is asking for a specific item by its position in the list."}
# user_question = "Return the fifth job" # {"query": "position", "value": 4, "think": "The user is asking for a specific position in the list, referring to 'the fifth' job"}

# ATTRIBUTE
# user_question = "Return the job with arrival date 31/3" # {"query": "attribute", "key": "arrival date", "value": "31/3", "think": "The user is referring to a specific attribute (arrival date) and value, so it's likely an attribute-based query"}
# user_question = "Return the job with id 8" # {"query": "attribute", "key": "id", "value": 8, "think": "The user wants to retrieve a specific job based on its id, so I assume it's an attribute query."}
# user_question = "Are there any jobs with arrival date 31 2" # {"query": "attribute", "key": "arrival date", "value": "31 2", "think": "trying to find jobs based on a specific attribute value"}
# user_question = "What jobs require the task with id 584" # {"query": "attribute", "key": "id", "value": 583, "think": "The user is asking for jobs that have a specific task with id 584, so I'm looking for tasks with id 583 (using zero-based indexing)"}

'''

with open("C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json") as f:
    data = json.loads(f.read())

print(data['jobs']['job'])
#t = tokenizer.tokenize(json.dumps(data))
#print('\n***')
#print(t)
#print(len(t))

'''
1. All / Any Items

If the user question refers about a specific attribute or position regardless of whether there are keywords such as 'any', 'all' in the question, you sound NOT return this. If the user asks about all items, any items, or makes a general question about the entire list NOT specifying any specific position or attribute, return:
{"query": "any", "think": <Your thinking process>}

Examples:
-"Show all items"
-"List the items"
-"Do any items have status active?"
-"What are the names of the items?"
'''

user_question = "What jobs require the task with id 584"

user_prompt = """You are a query interpreter. Your task is to determine what type of query the user is making.

There are three possible query types.

1. All / Any Items

If the user asks about all items, any items, or makes a general question about the list NOT specifying any specific position or attribute, return:
{"query": "any"}

Examples:
-"Show all items"
-"List the items"
-"Do any items have status active?"
-"What are the names of the items?"

2.Position-Based Query

If the user refers to an item by its position in the list, return:
{"query": "position", "value": <index>}

Use zero-based indexing.

Position mappings:
-first -> 0
-second -> 1
-third -> 2
-fourth -> 3
-fifth -> 4
-last -> -1
-item number N -> N-1
-element number N -> N-1

Examples:
-"Show the first item" -> {"query": "position", "value": 0}
-"Give me item number 3" -> {"query": "position", "value": 2}
-"Show the last element" -> {"query": "position", "value": -1}

3. Attribute-Based Query

If the user refers to a specific item based on an attribute value, return:
{"query": "attribute", "key": "<attribute_name>", "value": <attribute_value>}

Examples:
-"Find the item with id 57" -> {"query": "attribute", "key": "id", "value": 57}
-"Show the item with name John" -> {"query": "attribute", "key": "name", "value": "John"}
-"Get the product where sku is A123" -> {"query": "attribute", "key": "sku", "value": "A123"}

Rules:

Return only valid JSON
Do not include explanations
Use zero-based indexing for positions
If the question references item number N, convert it to N-1
If the question references the whole list or multiple items, return {"query": "any"}
If the question references a specific attribute and value, return an attribute query

Output format (return exactly one JSON object):

{"query": "any"}

or

{"query": "position", "value": <index>}

or

{"query": "attribute", "key": "<attribute_name>", "value": <attribute_value>}


"""

user_prompt_verbose = """You are a query interpreter. Your task is to determine what type of query the user is making.

There are three possible query types.

1.Position-Based Query

If the user refers to an item by its position in the list, return:
{"query": "position", "value": <index>, "think": <Your thinking process>}

Use zero-based indexing.

Position mappings:
-first -> 0
-second -> 1
-third -> 2
-fourth -> 3
-fifth -> 4
-last -> -1
-item number N -> N-1
-element number N -> N-1

Examples:
-"Show the first item" -> {"query": "position", "value": 0}
-"Give me item number 3" -> {"query": "position", "value": 2}
-"Show the last element" -> {"query": "position", "value": -1}

2. Attribute-Based Query

If the user refers to a specific item based on an attribute value, return:
{"query": "attribute", "key": "<attribute_name>", "value": <attribute_value>, "think": <Your thinking process>}

#NOTE: Attributes like: 'name', 'id', etc.. should NOT be confused with positioned-based queries. They are part of an attribute-based query. In case of ids do NOT use zero-based indexing.

Examples:
-"Find the item with id 57" -> {"query": "attribute", "key": "id", "value": 57}
-"Show the item with name John" -> {"query": "attribute", "key": "name", "value": "John"}
-"Get the product where sku is A123" -> {"query": "attribute", "key": "sku", "value": "A123"}

3. None

If the user question doesn't match any of the above, return:
{"query": "none", "think": <Your thinking process>}

Rules:

Return only valid JSON
Do not include explanations
Use zero-based indexing for positions
If the question references item number N, convert it to N-1
If the question references the whole list or multiple items, return {"query": "any"}
If the question references a specific attribute and value, return an attribute query
The output should be a JSON string and nothing else.

Output format (return exactly one JSON object):

{"query": "none", "think": <Your thinking process>}

or

{"query": "position", "value": <index>, "think": <Your thinking process>}

or

{"query": "attribute", "key": "<attribute_name>", "value": <attribute_value>, "think": <Your thinking process>}

Think before answering. Your answer (query) should match your thinking process

"""

user_prompt += f"""User Question:
{user_question}"""
user_prompt_verbose += f"""User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': user_prompt_verbose}])

#print(llm_answer)
print('==============')
print(user_prompt_verbose)
print('====')
print(len(tokenizer.tokenize(json.dumps(user_prompt_verbose))))
print(llm_answer.message.content)