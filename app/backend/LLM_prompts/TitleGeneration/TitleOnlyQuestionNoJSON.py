def getPrompt(user_question):
    prompt = f"""You are given a user's question. Based only on that question, generate a concise and relevant title that summarizes the core topic.

Requirements:

- Maximum 3 words
- Clear and specific
- No punctuation at the end
- No extra text or explanation
- Output only the title

____________
User Question:
{user_question}"""
    
    return prompt