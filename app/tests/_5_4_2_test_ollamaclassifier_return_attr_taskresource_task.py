from ollama import chat

# This prompt is only for search= Task
user_question = 'Which tasks can be done in resource 901?' # false 3/3 times # {"attribute": false, "think": "The user wants to return all tasks that can be executed in a specific resource, so I'm assuming they want the entire task object. The word 'tasks' is used instead of 'task', implying multiple results are expected."}
user_question = 'Which tasks can be done in resource 2?' # {"attribute": false, "think": "The user is asking for information about the tasks that can be executed in a specific resource. Since 'resource 2' is mentioned but no specific attribute of the task is specified, I assume they want to see all related tasks without filtering by any condition."}
user_question = 'Which tasks can be done in resource with id 1?' # false 3/3 times # {"attribute": false, "think": "The user is searching for the full task object, as indicated by 'which' and 'can be done', implying a complete task rather than just an attribute. The focus is on tasks, not filtering conditions regarding resources."}
user_question = 'Can Task 11 be executed in the MELTSHOP?' # id 3/3 times # {"attribute": true, "key": "id", "value": 11, "think": "The user is asking for a specific task by its id and checking if it can be executed in a resource."}
user_question = 'Can rask 55 be executed in resource with name ROLLING MILL?' # id 3/3 times # {"attribute": true, "key": "id", "value": 55, "think": "The user is searching for a specific task id (55) and the task's attribute is specified as 'id'. I ignored the filtering condition regarding the resource."}
user_question = 'How long does task 584 take?' # time 3/3 times # {"attribute": true, "key": "time", "think": "The user is searching for the 'time' attribute of a specific task with id 584."}
user_question = 'Return all resources and tasks' # <-- No thinking # {"attribute": false, "think": "The user wants the full task returned, which includes both resource and task information"}
user_question = 'Return all resources and their tasks' # {"attribute": false, "think": "The user is asking for the full task object to be returned, indicating they are looking for information about both the resource and its associated tasks. However, since the goal is to focus on what the user searches for regarding the task only, I conclude that the user wants to return all tasks."}
user_question = 'What task can be executed in the ROLLING MILL' # false 3/3 times # {"attribute": false, "think": "The user is searching for a specific task that can be executed in the ROLLING MILL. Since 'task' is not specified as an attribute to return, I assume they want to retrieve the entire task object."}
user_question = 'What is the operation time for task 587' # time 3/3 times # {"attribute": true, "key": "time", "think": "The user searches for a specific attribute 'time' of a task. Since the user asks about the operation time for a specific task (task 587), I assume they want to return only that attribute."}
## user_question = 'What tasks need to operate for more than 30minutes?' # {"attribute": true, "know": {"info": "time", "key": "value", "value": 30}, "search": {"info": "task"}, "think": ["Identified specific attribute: time", "Extracted known attribute value: 30 minutes", "Determined user wants to find tasks"] }
user_question = 'Return the operation times of all tasks that can be executed in the ROLLING MILL' # time 3/3 times # {"attribute": true, "key": "time", "think": "The user wants to return a specific attribute (operation time) of tasks that can be executed in the ROLLING MILL. The key 'time' is explicitly mentioned, indicating that the user is searching for this particular attribute."}
user_question = 'can task 584 be executed in resource _2?' # id 3/3 times # {"attribute": true, "key": "id", "value": 584, "think": "The user is searching for a specific attribute of the task, which is the id. The value of this id is 584."}
user_question = 'Can ROLLING task be executed in resource 1?' # name 3/3 times # {"attribute": true, "key": "name", "value": "ROLLING", "think": "The user is asking about a specific attribute of the tasks, which is the name. They are searching for a task with the name 'ROLLING' that can be executed in resource 1."}
user_question = 'Return all task ids that can be executed in resource _1' # id 3/3 times # {"attribute": true, "key": "id", "think": "The user is searching for a specific attribute of the task, which is the id. This is because the question explicitly mentions 'task ids'. The value is not specified, so it will require additional filtering to determine what resource '_1' means."}
user_question = 'Can ROLLING tasks be executed in the ROLLING MILL?' # name 3/3 times # {"attribute": true, "key": "name", "value": "ROLLING", "think": "The user is searching for a specific task attribute (name) that matches the value 'ROLLING', and this task should also match another condition (execution in resource with name ROLLING MILL), but since the goal is to focus on what the user searches for regarding the task, I ignored the filtering condition about resources"}
user_question = 'How long does each task take?' # time 3/3 times # {"attribute": true, "key": "time", "think": "The user is asking for the time attribute of tasks, which corresponds to their execution duration."}

prompt = """You are an information extraction assistant.

The user will provide a question about resources and tasks. The user is searching for something regarding the tasks. Focus on the tasks ONLY

Each task is basically a dictionary that contains the following keys:

- name: The name of the task
- id: The id of the task
- time: execution time or duration of a task

Your goal is to analyze the user's question and determine what the user searches for regarding the task:

- A specific attribute of a task (e.g., name, id, time), OR
- The entire task object

Rules:

- Focus ONLY on what the user searches for regarding the task ONLY. Ignore filtering conditions regarding the resource
- If the user wants for a specific attribute returned (e.g., "name", "id"), set "attribute": true and specify which attribute in "key". If the user also searches for a specific value of that key place it in "value"
- If the user wants the full task (even if filtered by some condition like id) returned, set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above AND cannot be anything else.
- If "attribute": false, do NOT include a "return" value.
- Never assume the user searches for a specific attribute unless its explicitly specified in the user question. It MUST BE mentioned by its key (name, id, time).

Remember:
You are identifying what the user searches for regarding the "resource" ONLY. That is your goal. Ignore filtering conditions regarding the tasks and ignore any task-related logic.

Output format:

Return ONLY a valid JSON object:

{"attribute": <bool>, "key": "<string>", "value": <integer or string>, "think": "<string>"}

- You must ALWAYS return a valid JSON object and nothing else. Do NOT explain yourself.
- Your thinking process should be placed in the 'think' key of dictionary
- Do not put anything outside the JSON object.

Examples:

User: "Return the name of the tasks that can be completed in resource 1"
Output: {"attribute": true, "key": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "What tasks can be executed in resource with id 3"
Output:{"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all tasks that can be executed in the ROLLING MILL"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all task ids that can be executed in resource _1"
Output: {"attribute": true, "key": "id", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all tasks and their resources"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the operation times of all tasks that can be executed in the ROLLING MILL"
Output: {"attribute": true, "key": "time", "think": "<Your thinking process>"}
------------------------------------------------
User: "can task 584 be executed in resource _2?"
Output:{"attribute": true, "key": "id", "value": 584, "think": "<Your thinking process>"}
------------------------------------------------
User: "Can task 77 be executed in ROLLING MILL?"
Output:{"attribute": true, "key": "id", "value": 77, "think": "<Your thinking process>"}
------------------------------------------------
User: "Can ROLLING tasks be executed in resource with id 5?"
Output:{"attribute": true, "key": "name", "value": "ROLLING", "think": "<Your thinking process>"}
------------------------------------------------
User: "Can task 55 be executed in resource with name ROLLING MILL?"
Output:{"attribute": true, "key": "id", "value": 55, "think": "<Your thinking process>"}
------------------------------------------------
User: "How long does each task take?"
Output:{"attribute": true, "key": "time", "think": "<Your thinking process>"}"""

prompt += f"""

______________
User Question:
{user_question}"""

#print(prompt)
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
print(llm_answer)
print(llm_answer.replace('\n', ''))
print('***********')