def getPrompt():
    prompt = """Suppose the user has provided input that is gibberish or random characters. Based only on this information, generate a short title

Rules:

- The title must be no more than 2 words
- Keep it short
- Return only the title, nothing else.
- Do not include punctuation unless necessary
- Do not add explanations—output only the title
- Be polite, neutral in tone
- The title should not be offending"""

    return prompt