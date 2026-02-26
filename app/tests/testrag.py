from langchain_community.document_loaders import DirectoryLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores.chroma import Chroma
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
# from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import chromadb

client = chromadb.Client()
saodjkas

data_path = "C:/Users/Chris/Downloads"

# laod documents
loader = DirectoryLoader(data_path, 'alice_in_wonderland.md')
documents = loader.load()
# print(loader)
# print(documents)
# prints: <langchain_community.document_loaders.directory.DirectoryLoader object at 0x000001F42F5DE3C0>
# prints: [Document(metadata={'source': 'C:\\Users\\Chris\\Downloads\\alice_in_wonderland.md'}, page_content="The Project Gutenberg eBook of Alice's Adventures in Wonderland\n\nThis ebook is for the use of anyone anywhere in the United States and most other parts of the world at no cost and with almost no restrictions whatsoever ... 

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 500,
    length_function = len,
    add_start_index = True,
)
chunks = text_splitter.split_documents(documents)

# print(len(chunks))
# print(chunks[0:5])
# prints: 286
# prints: [Document(metadata={'source': 'C:\\Users\\Chris\\Downloads\\alice_in_wonderland.md', 'start_index': 0}, page_content="The Project Gutenberg eBook of Alice's Adventures in Wonderland\n\nThis ebook is for the use of anyone anywhere in the United States  ... # basically list of documents
 
chroma_path = 'C:/Users/Chris/Downloads/chromadb_test'
#db = Chroma.from_documents(
#    chunks, embedding=OllamaEmbeddings(model = 'llama3.1:8b'), persist_directory = chroma_path
#)
#db.persist()
print('bbbb')
embed = OllamaEmbeddings(model='llama3.1:8b')
print('aaaa')
db = Chroma.from_documents(chunks)
print('cccc')
db.add_documents(chunks)
db.persist()