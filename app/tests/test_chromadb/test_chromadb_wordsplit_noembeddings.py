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

###
asnwers = []
iteret = 0
print(len(documents))
for i in documents:
    print(iteret)
    question = "How does Alice meet Hatter for the first time?"
    user_content = f"""
    Based on the following content:

    {i}

    Answer the following question using that content only. If you cant answer it based on the content simply remply with '*' and nothing else:

    {question}
    """
    ch = ollama.chat(model = 'llama3.1', messages=[{'role': 'user', 'content': user_content}])
    if(ch.message.content != '*'):
        asnwers.append({"a": ch.message.content, "c": i})
    else:
        asnwers.append({"a": ch.message.content})
    iteret +=1
print(asnwers)