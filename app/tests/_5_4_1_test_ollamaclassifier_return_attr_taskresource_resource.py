from ollama import chat

# This prompt is only for search= Resource
user_question = 'Where can task 57 be executed' # false 3/3 times # {"attribute": false, "think": "The user is asking for a condition where task 57 can be executed. Therefore, the entire resource object that satisfies this condition should be returned."}
user_question = 'Which resource can execute task with id 39?' # false 3/3 times {"attribute": false, "think": "The user is searching for a specific resource that can execute the given task. Since the question does not specify any attribute of the resource, I assume they want to retrieve the entire resource object."}
user_question = 'Which resource can execute task 39?' # false 3/3 times # {"attribute": false, "think": "Since the user is asking which resource can execute a task, it implies they want the entire resource object returned. The question focuses on the resource's ability to execute a task, rather than a specific attribute of the resource."}
user_question = 'Can Task 11 be executed in the MELTSHOP?' # name 3/3 times # {"attribute": true, "key": "name", "value": "MELTSHOP", "think": "The user wants to search for a specific attribute 'name' of the resource because it mentioned 'the MELTSHOP', which is likely a name of a resource."}
user_question = 'What resource can execute each task?' # false 3/3 times # {"attribute": false, "think": "The user is searching for the full resource object. They are asking which resource can execute each task, implying that they want to see all resources and their properties."}
user_question = 'Return all resources and tasks' # false 3/3 times # {"attribute": false, "think": "The user asked to return all resources and tasks, which means they want the entire resource object returned. I didn't find any attribute specified in the question, so it must be asking for the full resource."}
user_question = 'Return all resources and their tasks' # false 3/3 times # {"attribute": false, "think": "The user is asking for the full resource object regardless of the task-related condition. The key words 'all resources' indicates that the entire resource is required."}
user_question = 'Return the id of the resource that can execute task 91' # id 3/3 times # {"attribute": true, "key": "id", "think": "The user wants a specific attribute returned, which is 'id', and they are looking for a resource that can execute task 91, so I'm assuming they want to find the id of that resource."}
# Problematic: user_question = 'Return the ids of all resources and tasks' # id 3/3 times # {"attribute": true, "key": "id", "value": null, "think": "The user is asking for the ids of all resources and tasks. Since 'tasks' are not an attribute of a resource, I'm assuming they want the id of each task, which is related to each resource."}
user_question = 'Return all resources where task 77 can be executed' # false 3/3 times # {"attribute": false, "think": "The user is searching for all resources, so I'm assuming they want the full resource object returned. The presence of 'task 77' in the question suggests a filtering condition related to tasks, but according to the rules, I should focus only on what the user searches for regarding the resource, which in this case is the entire resource object."}
user_question = 'Return the id of every resource where task 77 can be executed' # id 3/3 times # {"attribute": true, "key": "id", "think": "The user wants to retrieve a specific attribute 'id' from each relevant resource. The relevant resources are those where task 77 can be executed."}
user_question = 'Return all resources where task 584 can be executed' # false 3/3 times # {"attribute": false, "think": "The user is asking for the full resource object when a specific task (task 584) can be executed. Since the task's condition is mentioned and not the attribute of the resource itself, I infer that they want the entire resource returned."}
user_question = 'Return the id of every resource where task 584 can be executed' # id 3/3 times # {"attribute": true, "key": "id", "think": "The user is searching for a specific attribute (id) of the resources. The condition regarding task 584 is ignored as per the rules."}
user_question = 'Return the id of every resource where task with id 77 can be executed' # id 3/3 times # {"attribute": true, "key": "id", "think": "The user is looking for a specific attribute of the resource, which is the id. This is specified by the keyword 'id' in the question."}
user_question = 'Return the name of every resource where task with id 77 can be executed' # name 3/3 times {"attribute": true, "key": "name", "think": "The user wants to return a specific attribute (name) related to the resources. The question specifies 'every resource', which implies they want all attributes for each matching resource. However, since name is explicitly mentioned, it focuses on this attribute."}
user_question = 'Return the id of every resource where ROLLING can be executed' # id 3/3 times # {"attribute": true, "key": "id", "think": "The user is searching for a specific attribute 'id' of each resource, as indicated by the phrase 'the id of every resource'. The word 'every' implies they want all resources."}
user_question = 'Return the name of the resources where task 584 can be executed' # {"attribute": true, "key": "name", "think": "The user wants to return a specific attribute of the resource, which is 'name', because it explicitly mentioned 'the name of the resources'. It's searching for resources where task 584 can be executed, but that's about filtering conditions regarding tasks and not what they're looking for about the resource itself."}
user_question = 'Return the resource in which task 584 can be executed' # {"attribute": false, "think": "The user is searching for a specific resource based on its ability to execute a task, so I'm not assuming they want a specific attribute. The question is focused on returning the entire resource object."}
user_question = 'In which resources can task 584 be executed?' # {"attribute": false, "think": "The user is asking for a list of resources where task 584 can be executed. Since it's not specifying any specific attribute, I assume they want the full resource object returned."}
user_question = 'What are the working periods of the resource where task 584 can be executed?' # {"attribute": true, "key": "period", "think": "The user is searching for a specific attribute regarding the resource, which is the 'period' key. This is because they asked about the working periods of the resource, implying they want to know something about its availability."}
user_question = 'Can ROLLING MILL execute task 58?' # {"attribute": true, "key": "name", "value": "ROLLING MILL", "think": "The user is searching for a specific attribute of the resource (the name), so I set 'attribute' to True. The key is 'name', and the value is the name of the resource which is 'ROLLING MILL'."}

prompt = """You are an information extraction assistant.

The user will provide a question about resources and tasks. The user is searching for something regarding the resource. Focus on the resource ONLY

Each resource is basically a dictionary that contains the following keys:

- name: The name of the resource
- id: The id of the resource
- period: The non-working periods (the time periods at which the resource is idle, it is NOT working)

Your goal is to analyze the user's question and determine what the user searches for regarding the resource:

- A specific attribute of a resource (e.g., name, id, period), OR
- The entire resource object

Rules:

- Focus ONLY on what the user searches for regarding the resource ONLY. Ignore filtering conditions regarding the task
- If the user wants for a specific attribute returned (e.g., "name", "id"), set "attribute": true and specify which attribute in "key". If the user also searches for a specific value of that key place it in "value"
- If the user wants the full resource (even if filtered by some condition like id) returned, set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above AND cannot be anything else.
- If "attribute": false, do NOT include a "return" value.
- Never assume the user searches for a specific attribute unless its explicitly specified in the user question. It MUST BE mentioned by its key (name, id, period).

Remember:
You are identifying what the user searches for regarding the "resource" ONLY. That is your goal. Ignore filtering conditions regarding the tasks and ignore any task-related logic.

Output format:

Return ONLY a valid JSON object:

{"attribute": <bool>, "key": "<string>", "value": <integer or string>, "think": "<string>"}

- You must ALWAYS return a valid JSON object and nothing else. Do NOT explain yourself.
- Your thinking process should be placed in the 'think' key of dictionary
- Do not put anything outside the JSON object.

Examples:

User: "Return the name of the resources where task 77 is done"
Output: {"attribute": true, "key": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "What resource can execute task with id 59"
Output:{"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all resources where task 584 can be executed"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Can resource 1 execute task 35"
Output: {"attribute": true, "key": "id", "value": 1, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all resources and their tasks"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "How many resources can execute the ROLLING task?"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Can resource ROLLING MILL execute task 98?"
Output:{"attribute": true, "key": "name", "value": "ROLLING MILL", "think": "<Your thinking process>"}
------------------------------------------------
User: "What are the working periods of resouces that can execute ROLLING task"
Output:{"attribute": true, "key": "period", "think": "<Your thinking process>"}
------------------------------------------------
User: "Can the MELTSHOP do the task with id 585?"
Output:{"attribute": true, "key": "name", "value": "MELTSHOP", "think": "<Your thinking process>"}"""

prompt += f"""

______________
User Question:
{user_question}"""

#print(prompt)
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
print(llm_answer)
print(llm_answer.replace('\n', ''))
print('***********')