#from langchain_community.agent_toolkits.json.base import create_json_agent
#from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
#from langchain_community.tools.json.tool import JsonSpec
import json
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

from transformers import AutoTokenizer

with open("C:/Users/Chris/Downloads/diplomat/json_examples/appropriate_from/InputJSON_3_shorter.json", encoding='utf-8') as f:
    json_file = json.load(f)
    print(type(json_file))

### Tools
@tool('get_item', description = 'Gets the value of the key, that the user is asking about. The key must be one of the following values: "workcenter", "jobs", "tasks", "tasksuitableresources", "taskprecedenceconstraints".')
def GetItem(key: str):
    print(f'--- called GetItem with key: {key} ---')
    val_json = {"workcenter": json_file['workcenters']['workcenter'],
     "jobs": json_file['jobs']['job'],
     "tasks": json_file['tasks']['task'],
     "tasksuitableresources": json_file['tasksuitableresources']['tasksuitableresource'],
     "taskprecedenceconstraints": json_file['taskprecedenceconstraints']['taskprecedenceconstraint']}

    return val_json[key]
###


tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

tokens = tokenizer.tokenize(json.dumps(json_file))

#print(f"Tokens: {tokens}")
print(f"Token count: {len(tokens)}")

llm_agent = create_agent(
    model = ChatOllama(model = 'llama3.1'),
    tools = [GetItem]
)
print('Fin')
# messages = [{'role': 'user', 'content': 'List the ids of all the jobs'}]
messages = [{'role': 'user', 'content': 'What tasks does each job require?'}]

print(llm_agent.invoke({'messages': messages}))