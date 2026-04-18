def getPrompt(file_name):
    prompt = f"""You are interacting with a user who has uploaded a file in JSON format.

Your task is simple:

- Acknowledge that you can see the user has uploaded a JSON file named {file_name}.
- Do not analyze or interpret the file yet.
- Offer help by asking if the user would like you to analyze, explain, validate, or get the JSON data.

Keep your response short, polite, and helpful. Avoid making assumptions about the contents of the file."""
    
    return prompt