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
# user_question = "Return the job with arrival date 31/3" # {"query": "attribute", "think": "The user wants to retrieve a specific item based on an attribute, which is 'arrival date'. The value of the attribute is given as '31/3', indicating the arrival date. This will require filtering or searching for items with that specific attribute and value."}
# user_question = "Return the job with id 8" # {"query": "attribute", "think": "The user is looking for a specific item based on an attribute 'id' and value '8', so I'm assuming it's an attribute-based query."}
# user_question = "Are there any jobs with arrival date 31 2" # {"query": "attribute", "think": "The user is asking for a specific attribute and value, the job with arrival date 31 2"}
# user_question = "What jobs require the task with id 584" # {"query": "attribute", "think": "The user is asking for a specific item based on an attribute value, in this case, the task with id 584."}
# user_question = "List jobs with id 51" # {"query": "attribute", "think": "The user is asking for a list of items based on an attribute 'id'"}
# user_question = "Find jobs that require task 581" # {"query": "attribute", "think": "find items based on attribute, user is asking about jobs with a specific requirement"}
# user_question = "Find jobs that require task with id 581" # {"query": "attribute", "think": "The user is asking about a specific attribute of a task, which is the id 581."}
# user_question = "Find the last job that requires task with id 581" # {"query": "complex", "value": -1, "think": "The user is asking for the last item based on a position and an attribute constraint, where the attribute is 'requires task with id 581'"}

# COMPLEX
# user_question = "Return the first job that requires the task with id 580" # {"query": "complex", "value": 0, "think": "The user wants to return a specific job based on its position and an attribute constraint, which is finding a task with id 580."}
# user_question = "Find the last job that requires task with id 581" # {"query": "complex", "value": -1, "think": "The user is asking for the last item based on a position and an attribute constraint, where the attribute is 'requires task with id 581'"}

### TASK ###
vars possible: name, id

# NONE #
# user_question = "Return tasks" # {"query": "none", "think": "The user is asking to return tasks, but the question doesn't specify a position or attribute, so it's unclear what they're referring to."}
# user_question = "tasks" # {"query": "none", "think": "The question 'tasks' is a list name, but it does not ask for any specific item or attribute."}

# POSITION #
# user_question = "Return first task" # {"query": "position", "value": 0, "think": "The user wants the first item in the list"}

# ATTRIBUTE #
# user_question = "Return task with id 584" # {"query": "attribute", "think": "user asked for a task by its attribute, specifically the id"}
# user_question = "task with name Rolling" # {"query": "attribute", "think": "The user is referring to an item based on its name, which is 'Rolling'. This is a characteristic or attribute of the item."}

# COMPLEX #
# user_question = "Return first task with name Rolling" # {  "query": "complex",  "value": 0,  "think": "user asked for the first item and used an attribute constraint 'with name' to filter"}

### RESOURCES ###
vars possible: name, id, resourceavailability

### TASKSUITABLERESOURCES ###
vars possible: resourcereference, taskreference, setupcode, operationtimeperbatchinseconds

# NONE #

# POSITION #

# ATTRIBUTE #
# user_question = "Which tasks can be done in resource 1?" # {"query": "attribute", "think": "Identifying tasks related to a specific resource"}
# user_content = 'Where can task 1 be executed' -> Registers as position

# COMPLEX #

### TASKPRECEDENCECONSTRAINT ###
vars possible: preconditiontaskreference, postconditiontaskreference

##### IMPORTANT #####
TASKSUITABLERESOURCES and TASKPRECEDENCECONSTRAINT should be treated by different prompts as questions regarding them have a special kind of wording different to
the other attributes
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

user_question = 'Is task 11 independent of other tasks?'

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

If the user refers to a specific item based on an attribute or some value, return:
{"query": "attribute", "think": <Your thinking process>}

Examples:
-"Find the item with id 57" -> {"query": "attribute"}
-"Show the item with name John" -> {"query": "attribute"}
-"Get the product where sku is A123" -> {"query": "attribute"}
-"Are there any shirts whith color blue" -> {"query": "attribute"}

3. Complex Query (Combination of Position-based and Attribute-based)

If the user refers to an item using both a position and an attribute constraint, return:
{"query": "complex", "value": <index>, "think": <Your thinking process>}
The index value should be calculated using the zero-based indexing mentioned above

Examples:
"Show the first task with id 10" -> {"query": "complex", "value": 0}
"Give me the second item with name John" -> {"query": "complex", "value": 1}
"Show the last task with id 5" -> {"query": "complex", "value": -1}

4. None

If the user question doesn't match any of the above, return:
{"query": "none", "think": <Your thinking process>}

Rules:

Return only valid JSON
Do not include explanations
Use zero-based indexing for positions
If the question references item number N, convert it to N-1
The output should be a JSON string and nothing else.
The JSON string should not have any new line characters
Words like 'all', 'any', 'list' should be ommited when thinking and should not affect your judgement. Your job is to find if the user asks about an attribute or position and these words should not affect the broader context of the question

Output format (return exactly one JSON object):

{"query": "none", "think": <Your thinking process>}

or

{"query": "position", "value": <index>, "think": <Your thinking process>}

or

{"query": "complex", "value": <index>, "think": <Your thinking process>}

or

{"query": "attribute", "think": <Your thinking process>}

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
aa = llm_answer.message.content
print(aa)
print(aa.replace('\n', ''))