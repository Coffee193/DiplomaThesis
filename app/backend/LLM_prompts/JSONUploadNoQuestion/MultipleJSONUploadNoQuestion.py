def getPrompt(file_names):
    prompt = f"""The user has uploaded multiple files named:
{', '.join(file_names)}

You do not have access to the file contents. Do NOT attempt to infer, assume, or fabricate any data from it.

Your task is to:

- Acknowledge that the user successfully uploaded these JSON files.
- Offer helpful ways you can assist the user in working with these file, such as:
- Summarizing the data
- Extracting specific fields
- Finding patterns or insights
- Debugging or validating the JSON structure
Ask the user what they would like to do with these files or to provide more details about their goal.

Do NOT analyze or describe any specific data from these files. Keep the response helpful, clear, and action-oriented."""
    
    return prompt