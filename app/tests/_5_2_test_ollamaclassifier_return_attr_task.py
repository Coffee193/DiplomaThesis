from ollama import chat

user_question = "Return task with id 584" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object (not just a specific attribute), as they mentioned 'task' in their question. No other attributes were specified, so it's safe to assume they want the full task returned."}
user_question = "task with name Rolling" # false 3/3 trimes # {"attribute": false, "think": "The user wants to return the entire task object because it is mentioned as 'task' without specifying any attribute. The keyword 'with name' implies a filtering condition but does not affect what is returned."}
user_question = "Return first task with name Rolling" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object (not just an attribute), so 'attribute' is set to False. The request asks for 'the first task', which implies returning all properties of that specific task."}
user_question = "Return first task" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object, not a specific attribute. Assuming 'first' means the task with id 1 (although this is not explicitly specified in the question), but since it's only asking for what to return and not how to filter, I'll assume it's looking for the full task."}
user_question = "tasks" # false 3/3 times # {"attribute": false, "think": "The user wants to return all tasks without specifying any attribute or condition."}
user_question = "return task 7" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object, but they mentioned 'task', not a specific attribute like 'name' or 'id'. So I'm assuming they want all attributes returned."}
user_question = "return 7 task" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object, so I set 'attribute' to False. The keyword 'task' suggests that they want a specific task with id 7."}"
#user_question = "return 7 tasks" # false 3/3 times # {"attribute": false, "think": "The user is asking to return all tasks, but only mentioned 'tasks', which implies returning the entire task object. There's no mention of any specific attribute or condition like id."}
#user_question = "return the last task" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object, even though they mentioned 'last', which is likely a filtering condition. Since 'last' wasn't explicitly specified as an attribute I'm focusing on what's being returned, not how it's filtered."}
#user_question = 'Return all ROLLING tasks' # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object, but the question mentions a specific condition (tasks with name 'ROLLING'). However, based on the rules, I should only focus on what is being returned, not the filtering conditions. Therefore, the correct interpretation is that the user wants the full task returned."}
#user_question = 'Return the id of all tasks with name ROLLING' # id 3/3 times # {"attribute": true, "return": "id", "think": "The user wants to return a specific attribute (id) of the task, as it is explicitly mentioned in the question. The key 'id' is specified."}
#user_question = 'What is the name of the task with id 77' # name 3/3 times  # {"attribute": true, "return": "name", "think": "The user wants to know a specific attribute of a task. The question explicitly mentions 'name' and conditions that match certain tasks."}
user_question = 'What are the ids of MELTING task' # id 3/3 times # {"attribute": true, "return": "id", "think": "The user is asking for a specific attribute (id) to be returned. The question mentions 'MELTING', which implies they want tasks with that name, but since it's not explicitly mentioned as the condition to return tasks, I'm focusing on what they want returned."}
#user_question = 'Return all tasks' # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire task object without any filtering conditions."}
#user_question = 'Return the name of every task' # name 3/3 times # {"attribute": true, "return": "name", "think": "The user wants to return a specific attribute of each task, which is mentioned as 'name' in the question."}

prompt = """You are an information extraction assistant.

The user will provide a question about the tasks.

Each task is basically a dictionary that contains the following keys:

- name: The name of the task
- id: The id of the task

Your goal is to analyze the user's question and determine what the user wants returned:

- A specific attribute of a task (e.g., name, id), OR
- The entire task object

Rules:

- Focus ONLY on what the user wants returned, not on filtering conditions.
- If the user wants for a specific attribute returned (e.g., "name", "id"), set "attribute": true and specify which attribute in "return".
- If the user wants the full task (even if filtered by some condition like id) returned, set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above AND cannot be anything else.
- If "attribute": false, do NOT include a "return" value.
- Never assume the user wants an attribute returned unless its explicitly specified in the user question. It MUST BE mentioned by its key (name, id).

Remember:
You are identifying what the user wants RETURNED. That is your goal

Output format:

Return ONLY a valid JSON object:

{"attribute": <bool>, "return": "<string>", "think": "<string>"}

- You must ALWAYS return a valid JSON object and nothing else. Do NOT explain yourself.
- Your thinking process should be placed in the 'think' key of dictionary
- Do not put anything outside the JSON object.

Examples:

User: "Return the name of the task with id 63"
Output: {"attribute": true, "return": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the task with id 73"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "What is the name of the task with id 77?"
Output: {"attribute": true, "return": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all tasks"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the id of all tasks with name ROLLING"
Output: {"attribute": true, "return": "id", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all ROLLING tasks"
Output:{"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "What are the ids of MELTING'"
Output:{"attribute": true, "return": "id", "think": "<Your thinking process>"}"""

prompt += f"""

____________________
User Question:
{user_question}"""

#print(prompt)
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
print(llm_answer)
print(llm_answer.replace('\n', ''))
print('***********')