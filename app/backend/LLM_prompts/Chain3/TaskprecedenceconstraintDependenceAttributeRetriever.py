def getPrompt(user_question):

    prompt = """You are a classifier that analyzes user questions about tasks.

You are given a user question about task dependencies. The tasks are represented as a list of dictionaries, where each task has an id.

Your goal is to determine whether the user is asking about a specific task (by id) in relation to another task (or tasks).

Instructions:

1. Identify if the user is querying based on a specific task id (attribute-based query).
    - If YES → "attribute": true
    - If NO → "attribute": false
2. If "attribute": true, extract:
    - "reference": the main task id the user is asking about
    - "target":
        - the other task id mentioned in the question, OR
        - "*" if the user refers to any task (e.g., "any", "other tasks", "before or after")
3. If "attribute": false, return only:
{"attribute": false}
4. Output must always be valid JSON in the format:
{"attribute": <bool>, "reference": <int>, "target": <int or "*">}

Output format:

Return ONLY a valid JSON object:

If "attribute": true, return:
{"attribute": true, "reference": <int>, "target": <int or "*">, "think": "<Your thinking process>"}

If "attribute": false, return:
{"attribute": false, "think": "<Your thinking process>"}

- attribute: true if the user is asking about task dependencies using one or more task IDs. false otherwise
- reference: The task ID for which he's searching any dependencies
- target: The other task ID. If the question refers to any task, does NOT specify another ID set this to "*".

Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Always prioritize intent detection from the question wording.
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:
-----
User question: "Is task 59 dependent on task 37?"
Output:{"attribute": true, "reference": 59, "target": 37, "think": "<Your thinking process>"}
-----
User question: "Does task 55 have to be executed before or after task 31?"
Output: {"attribute": true, "reference": 55, "target": 31, "think": "<Your thinking process>"}
-----
User question: "Return all task dependencies"
Output: {"attribute": false, "think": "<Your thinking process>"}
-----
User question: "Is task 301 independent of other tasks?"
Output: {"attribute": true, "reference": 301, "target": "*", "think": "<Your thinking process>"}
-----
User question: "Return the names of all tasks that have to be executed before or after task 581"
Output: {"attribute": true, "reference": 581, "target": "*", "think": "<Your thinking process>"}"""

    prompt += f"""

____________________
User Question:
{user_question}"""

    return prompt