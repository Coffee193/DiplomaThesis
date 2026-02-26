import redis
import ollama
import threading
import asyncio
import time

redis_client = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

question = "How does Alice meet Hatter for the first time?"
ch = ollama.chat(model = 'llama3.1', messages=[{'role': 'user', 'content': question}], stream = True)


def streamTOredis_Old(chat):
    print('chat with ollama...')
    for chunk in chat:
        print(chunk.message.content, end='', flush=True)
        if(chunk.done == True):
            print('/n')
            print('I SHIIIIIIIIIIIIIT')
            print(chunk.dict)
            print(chunk.copy)

def streamTOredis(chat):
    print('chat with ollama...')
    for chunk in chat:
            redis_client.xadd(
            "chatid",
            {"v": chunk.message.content}
            )
            if(chunk.done == True):
                print('/n')
                print('I SHIIIIIIIIIIIIIT')
                print(chunk.dict)
                print(chunk.copy)

def askchat():
    #question = "How does Alice meet Hatter for the first time?"
    question = "Write a 1000 word essay about obesity"
    ch = ollama.chat(model = 'llama3.1', messages=[{'role': 'user', 'content': question}], stream = True)
    threading.Thread(target = streamTOredis, args = (ch,)).start()
    return 'bobobo'

def read_redis(id = 0):
    x = redis_client.xread(streams = {"chatid": id}, block=1000)
    print(x)
    '''
    print(x[0])
    print(x[0][1])
    print('.....')
    print(x[0][1][0])
    print(x[0][1][0][0])
    print(x[0][1][0][1])
    print(x[0][1][0][1]['v'])
    print('***')
    return x[0][1][0][0]
    #id = x[0][1][0][0]
    '''

if __name__ == "__main__":
    print('*****')
    vavu = askchat()
    print('-----')
    print(vavu)
    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;')
    
    vv = read_redis()
    print('================')
    iasujhdiashjudjhasuio
    time.sleep(2)
    print('>>>>>>>>>>>>')
    read_redis(vv)

    #print(redis_client.xread(streams = {"chatid": 0}, block=1000, count=5000)[1])
    #print('&&&&&&&&&')