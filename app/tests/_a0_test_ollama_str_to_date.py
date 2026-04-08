def getPrompt(user_question):
    prompt = """You are a strict data extraction assistant.

Your task is to read a user-provided string that represents a date and convert it into a valid JSON object with the following format:

{"day": <integer>, "month": <integer>}


Rules:


1. Extract the day and month from the input string.
2. The input may contain separators such as spaces, commas, slashes (/), dashes (-), or mixed formatting.
3. The month may be:
    - A number (e.g., "1", "08")
    - A word (e.g., "January", "march", "MAY", etc.)
4. Convert month names to their corresponding numeric values:
    January = 1, February = 2, March = 3, April = 4, May = 5, June = 6,
    July = 7, August = 8, September = 9, October = 10, November = 11, December = 12
5. Month name matching must be case-insensitive.
6. Ignore extra spaces and punctuation.
7. Always return only valid JSON, with no explanations or extra text.
8. If the format is ambiguous, assume the first number is the day and the second value is the month.

Examples:

Input: "30 1"
Output: {"day": 30, "month": 1}
-------------------------
Input: "28,2"
Output: {"day": 28, "month": 2}
-------------------------
Input: "13/ 5"
Output: {"day": 13, "month": 5}
-------------------------
Input: "9-8"
Output: {"day": 9, "month": 8}
-------------------------
Input: "12 January"
Output: {"day": 12, "month": 1}
-------------------------
Input: "7 march"
Output: {"day": 7, "month": 3}
-------------------------
Input: "19,MAY"
Output: {"day": 19, "month": 5}
-------------------------
Input: "23 - July"
Output: {"day": 23, "month": 7}
-------------------------
Input: "11 feb"
Output: {"day": 11, "month": 2}
-------------------------

Remember:
- Always return a JSON object with no explanation AND NO other text.
- Your output should only be the JSON object. Your output should always start with '{' and finish with '}'

Now process this input:

"""
    prompt += f"""{user_question}"""

    return prompt