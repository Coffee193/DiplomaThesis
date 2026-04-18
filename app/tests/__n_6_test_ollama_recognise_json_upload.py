from ollama import chat

file_name = 'InputJSON.json'
prompt = f"""The user has uploaded a file named {file_name}.

You do not have access to the file contents. Do NOT attempt to infer, assume, or fabricate any data from it.

Your task is to:

- Acknowledge that the uploaded file is a JSON file.
- Offer helpful ways you can assist the user in working with this file, such as:
    - Summarizing the data
    - Extracting specific fields
    - Finding patterns or insights
    - Debugging or validating the JSON structure
Ask the user what they would like to do with the file or to provide more details about their goal.

Do NOT analyze or describe any specific data from the file. Keep the response helpful, clear, and action-oriented."""

# Explain briefly what a JSON file typically contains (structured data, key-value pairs, etc.).
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print('**********************')
print(llm_answer)