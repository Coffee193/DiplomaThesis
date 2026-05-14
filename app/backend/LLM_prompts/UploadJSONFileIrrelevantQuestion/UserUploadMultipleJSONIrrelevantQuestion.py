def getPrompt(file_name, user_question):
    prompt = f"""You are given a user query along with multiple JSON file uploads. The user's question is unrelated to the contents of the JSON files.

Your task:

1. Answer the user's question directly and helpfully, as if the JSON files were not present.
2. After fully answering the question, add a brief, polite note acknowledging that the user has uploaded JSON files named:
{', '.join(file_name)}.
3. In that note, offer assistance with these files, such as analyzing them, summarizing them, or retrieving specific information from them.
4. Do NOT analyze, interpret, or make any assumptions about the contents of the JSON files.
5. Keep the tone polite, natural, and helpful.

Structure your response as:

- Main answer to the user's question
- A short follow-up paragraph mentioning the uploaded files and offering help

_____________________
User Question:
{user_question}"""
    
    return prompt