import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import datetime
from chromadb.config import Settings
import ollama

client = chromadb.Client(Settings(
    is_persistent = True,
    persist_directory = 'C:/Users/Chris/Downloads/chromadb_test_2',
   chroma_http_keepalive_secs = 500000)
    )
collection = client.get_or_create_collection(
    name = 'alice_in_wonderland',
    embedding_function = OllamaEmbeddingFunction(model_name = 'llama3.1:latest'),
    metadata = { "created": str(datetime.datetime.now()), "description": "created for testing chromadb", "chunksize": "2000words", "overlap": 500 },
    )

res = collection.query(
    query_texts=["How does Alice meet the Hatter?"],
    n_results = 3
)
#print(res)
#print('*************\n\n\n')
content = ''
for i in res['documents'][0]:
    content += i
    content += '\n\n-----\n\n'

#question = "How does Alice meet Hatter?"
question = "How does Alice meet Hatter for the first time?"
user_content = f"""
Based on the following content:

{content}

Answer the following question using that content only:

{question}
"""
ch = ollama.chat(model = 'llama3.1', messages=[{'role': 'user', 'content': user_content}])
print(ch.message.content)
print('\n\n\n*******\n\n\n')
print(user_content)