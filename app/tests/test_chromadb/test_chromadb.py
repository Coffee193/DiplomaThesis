import sys
from langchain_community.document_loaders import DirectoryLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from ollama import chat
from langchain_ollama import ChatOllama

print('***')
print(sys.version)
print('***')

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

openaikey = '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'

chroma_path = 'C:/Users/Chris/Downloads/chromadb_test'

'''
print('AOAOAO')
db = Chroma.from_documents(
    chunks, embedding=OllamaEmbeddings(model = 'llama3.1:latest'), persist_directory = chroma_path
)
print('MUIMUI')
# db.persist()
print('*** finished ***')
'''

'''
print('AOAOAO')
db = Chroma.from_documents(
    chunks, embedding=OpenAIEmbeddings(api_key = openaikey), persist_directory = chroma_path
)
print('*** finished ***')

iujsad
'''

db = Chroma(persist_directory = chroma_path, embedding_function = OllamaEmbeddings(model = 'llama3.1:latest'))
# db = Chroma(persist_directory = chroma_path, embedding_function = OpenAIEmbeddings(api_key = openaikey))
query_text = "How does Alice meet the Hatter?"
res = db.similarity_search_with_relevance_scores(query_text, 3)

for i in res:
    print(i[0].metadata['start_index'])
    print(i[0].page_content)
    print(i[1])
    print('_____________________________________________________')

content = "\n\n---\n\n".join([doc.page_content for doc, _ in res])
question ="How does Alice meet the Hatter?"
user_prompt = f"""
Based on these pieces of text:
{content}

Answer the following question: {question} 
"""

print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print(user_prompt)
print('asking...\n\n')


aa = chat('llama3.1', messages = [
    {'role': 'user', 'content': user_prompt}
])
print(aa)
print('\n\n')
print(aa.message.content)

ihuiojhoiujoi
prompt_template ="""
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in res])
print('*****')
print(context_text)

fin_template = ChatPromptTemplate.from_template(prompt_template)
print('\n=======\n')
print(fin_template)

prompt = fin_template.format(context = context_text, question = query_text)
print('\n;;;\n')
print(prompt)
print(type(prompt))

model = ChatOllama(model='llama3.1')
aa = model.invoke(input=prompt)
print('\n\n\n???\n\n\n')
print(aa)
