import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import datetime
from chromadb.config import Settings


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
print(collection.get())
file_load = 'C:/Users/Chris/Downloads/alice_in_wonderland.md'
file_content = ''
with open(file_load, 'r', encoding='utf-8') as file:
    file_content = file.read()

### split in chunks ###
chunksize = 2000
overlapsize = 500
documents = [file_content[a:a+chunksize] for a in range(0, len(file_content), chunksize-overlapsize)]
doc_ids = [str(i) for i in range(0, len(documents))]
doc_idx = [{"idx": len(''.join(documents[0:idx+1]))} for idx in range(0, len(documents))]
#print(documents)
print('********************')
print(doc_ids)
print('********************')
print(doc_idx)
print('adding...\n\n\n')
for i in range(0, len(documents)):
    collection.add(
        ids=[doc_ids[i]],
        documents=[documents[i]],
        metadatas=[doc_idx[i]]
        )
    
