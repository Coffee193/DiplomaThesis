import redis
import ollama
import threading
import asyncio
import time

redis_client = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

def streamTOredis(chat):
    print('chat with ollama...')
    '''
    for chunk in chat:
            redis_client.rpush("chatid", chunk.message.content)
            if(chunk.done == True):
                print('/n')
                print('I SHIIIIIIIIIIIIIT')
                print(chunk.dict)
                print(chunk.copy)
    '''
    for chunk in chat:
            redis_client.append("chatid", chunk.message.content)
            if(chunk.done == True):
                redis_client.append("chatid", "=$*$=")
                redis_client.expire("chatid", 2)
                print('/n')
                print('I SHIIIIIIIIIIIIIT')
                print(chunk.dict)
                print(chunk.copy)

def streamFROMredis(chatid, timeout, start=0):
    if redis_client.exists(chatid) == 0:
        time.sleep(timeout)
        if redis_client.exists(chatid) == 0:
            print(';;;')
            oijuiojiojoi
    
    return redis_client.getrange(chatid, start, -1)


def askchat():
    #question = "How does Alice meet Hatter for the first time?"
    question = "Write a 1000 word essay about obesity"
    ch = ollama.chat(model = 'llama3.1', messages=[{'role': 'user', 'content': question}], stream = True)
    threading.Thread(target = streamTOredis, args = (ch,)).start()
    return 'bobobo'

if __name__ == "__main__":
    vuvu = askchat()
    print('***')
    print(vuvu)
    print('***')
    time.sleep(3)
    while redis_client.exists('chatid') == 0:
        time.sleep(1)
    r = 0
    #for _ in range(0, 3):
    while True:
        v = streamFROMredis('chatid', 1, r)
        if(v == "=$*$="):
            print("stream ended")
            break
        print(v, end = '', flush = True)
        r += len(v)
        #print(r)
        #print('*******')