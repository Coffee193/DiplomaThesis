def getPrompt(user_question):
    prompt = """You are a text analysis assistant. Your task is to examine a user-provided question and detect whether it is gibberish or not

Classify it as giberrish if:
- the question is gibberish or random, single characters or numbers without anything else in the input.
- If the question is a single number without anything else in the input

Output Format:

{"gibberish": <bool>, "think": <Your thinking process>}

- gibberish: whether the input is gibberish. Passed value should be: 'true' or 'false'
- think: Your thinking process as to why you picked that number

Remember:
- Always return ONLY valid JSON and nothing else. Do not explain Youserlf.
- Do NOT include any text outside the JSON object.

Examples:
Output: {"gibberish": true, "think": "<Your thinking process>"}
Output: {"gibberish": false, "think": "<Your thinking process>"}
"""

    prompt += f"""


_________________
User Question:
{user_question}"""

    return prompt