from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama
import requests

@tool('getweather', description = 'Return weather information for a given city', return_direct = False)
def getweather(city: str):
    print(f'Tool called on {city}\n-----\n')
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    return response.json()

agent = create_agent(
    model = ChatOllama(model = 'llama3.1'),
    tools = [getweather, ]
)

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'What is 2+2?'}
    ]
})

print(response)
print('***')
print(response['messages'][-1])
print('***')
print(response['messages'][-1].content)