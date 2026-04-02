from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
import json
from langchain_ollama import ChatOllama

from transformers import AutoTokenizer

with open("C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json", encoding='utf-8') as f:
    data = json.load(f)
    #print(data)
    print(type(data))

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

tokens = tokenizer.tokenize(json.dumps(data))

#print(f"Tokens: {tokens}")
print(f"Token count: {len(tokens)}")

json_spec = JsonSpec(dict_= data, max_value_length = 15000)
json_toolkit = JsonToolkit(spec = json_spec)

json_agent = create_json_agent(
    llm = ChatOllama(model = 'llama3.1'),
    toolkit = json_toolkit,
    verbose = True
)
print('Fin')
print(len(data["tasks"]["task"]))

#print(json_agent.run('How many tasks are there?'))
print(json_agent.run('Ouput all job ids?'))