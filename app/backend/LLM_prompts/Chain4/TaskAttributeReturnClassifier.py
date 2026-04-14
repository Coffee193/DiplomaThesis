def getPrompt(user_question):

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

    return prompt