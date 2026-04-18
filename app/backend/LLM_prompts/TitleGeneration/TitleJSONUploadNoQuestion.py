def getPrompt():
    prompt = f"""You are given a JSON file. Based only on this information, generate a concise and relevant title for the conversation.

Requirements:

- The title must be no more than 4 words
- It should be general and context-wise be related to the following:
    - analysis
    - extraction
    - information
    - contents
- Keep it short, clear, and to the point
- Do not include unnecessary punctuation
- Do not add explanations—output only the title"""

    return prompt