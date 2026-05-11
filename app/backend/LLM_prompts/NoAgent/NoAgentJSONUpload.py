def getPrompt(user_question, documents):
    if(len(documents) == 1):
        prompt = f"""The user uploaded a file:
--- {documents[0]['name']} ---
{documents[0]['data']}
--- End of {documents[0]['name']} ---"""
    else:
        prompt = f"""The user uploaded {len(documents)} files:"""
        for doc in documents:
            prompt += f"""
--- {doc['name']} ---
{doc['data']}
--- End of {doc['name']} ---"""
            
    if(user_question != ''):
        prompt += f"""

User Question:
{user_question}"""
        
    return prompt