def getPrompt(user_question, file_name):
    prompt = f"""You are given a user query along with a JSON file upload. The user's question is unrelated to the contents of the JSON file.

Your task:

1. Answer the user's question directly and helpfully, as if the JSON file were not present.
2. After fully answering the question, add a brief, polite note acknowledging that the user has uploaded a JSON file named {file_name}.
3. In that note, offer assistance with the file, such as analyzing it, summarizing it, or retrieving specific information from it.
4. Do NOT analyze, interpret, or make any assumptions about the contents of the JSON file.
5. Keep the tone polite, natural, and helpful.

Structure your response as:

- Main answer to the user's question
- A short follow-up paragraph mentioning the uploaded file and offering help

_____________________
User Question:
{user_question}"""
    
    return prompt