import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import datetime
import ollama

file_load = 'C:/Users/Chris/Downloads/alice_in_wonderland.md'
file_content = ''

with open(file_load, 'r', encoding='utf-8') as file:
    file_content = file.read()

file_content = file_content.split()
for i in range(0, len(file_content)):
    file_content[i] = file_content[i] + " "
# print(file_content)


### split in chunks ###
chunksize = 512
overlapsize = 250

documents = [file_content[a:a+chunksize] for a in range(0, len(file_content), chunksize-overlapsize)]
for i in range(0, len(documents)):
    val = ''
    for y in range(0, len(documents[i])):
        val += documents[i][y]
    documents[i] = val

doc_ids = [str(i) for i in range(0, len(documents))]
doc_idx = [{"idx": len(''.join(documents[0:idx+1]))} for idx in range(0, len(documents))]

# print(len(documents))
# print(documents[0])

client = chromadb.Client(Settings(
    is_persistent = True,
    persist_directory = 'C:/Users/Chris/Downloads/chromadb_test_2',
    chroma_http_keepalive_secs = 500000)
    )
collection = client.get_or_create_collection(
    name = 'alice_in_wonderland_word_based_embmodel_qwen3',
    embedding_function = OllamaEmbeddingFunction(model_name = 'qwen3-embedding:8b'),
    metadata = { "created": str(datetime.datetime.now()), "description": "created for testing chromadb", "chunksize": "512token, each token is an english word", "overlap": "250 tokens" },
    )


res = collection.query(
    query_texts=["How does Alice meet the Hatter for the first time?"],
    #query_texts=["Alice meets the Hatter"],
    n_results = 5
)
print('*************************')
print(res)

# add the docs

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


dsadasdas
print(len(documents))
for i in range(0, len(documents)):
    print(i)
    collection.add(
        ids=[doc_ids[i]],
        documents=[documents[i]],
        metadatas=[doc_idx[i]]
        )