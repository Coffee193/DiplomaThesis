def getPrompt(user_question):

    prompt = """You are a classifier. Your task is to determine whether a given user question is a boolean question, meaning it can be answered with a simple "Yes" or "No".

Instructions:

- Consider entirely the grammatical structure of the question.
- If the question starts with things like (Can, Is, Are etc..) its a clear indication of boolean questions
- If the question starts with things like (What, Which etc..) its a clear indication of NOT boolean questions

Output Format:

Return ONLY a valid JSON object:

{"attribute": <bool>, "think": "<Your thinking process>"}

- attribute: true if question is boolean, false otherwise

Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:
User Question: "Does task 139 need to be executed before 722?"
Output: {"attribute": true, "think": "<Your thinking process>"}
-------------------
User Question: "Is there a task to be executed before task with id 483?"
Output: {"attribute": true, "think": "<Your thinking process>"}
-------------------
User Question: "What task can i execute after completing task 13?"
Output: {"attribute": false, "think": "<Your thinking process>"}
-------------------
User Question: "Which task should i execute before task 19?"
Output: {"attribute": false, "think": "<Your thinking process>"}
-------------------
User Question: "Return the task that I should complete before task 753?"
Output: {"attribute": false, "think": "<Your thinking process>"}"""

    prompt += f"""

___________________
User Question:
{user_question}"""


    return prompt