def getPrompt(user_question):
    prompt = f"""You are given a user question and a JSON file. Based only on this information, generate a concise and relevant title for the conversation.

Requirements:

- The title must be no more than 5 words
- It should clearly reflect the main topic or intent
- Keep it short, specific, and to the point
- Do not include punctuation unless necessary
- Do not add explanations—output only the title
- Never mention a database, instead reference the JSON file

_________________
User Question:
{user_question}"""
    
    return prompt