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
        if(chunk.done == True):
            print('/n')
            print('I SHIIIIIIIIIIIIIT')
            print(chunk.dict)
            print(chunk.copy)
            return
        print(chunk.message.content, end='', flush=True)

def streamTOredis(chat):
    print('chat with ollama...')
    for chunk in chat:
        if(chunk.done == True):
            print('/n')
            print('I SHIIIIIIIIIIIIIT')
            print(chunk.dict)
            print(chunk.copy)
            redis_client.xadd(
                "chatid",
                {"d": 1}
        )
            return
        #print('adding...')
        redis_client.xadd(
        "chatid",
        {"v": chunk.message.content}
        )

def askchat():
    #question = "How does Alice meet Hatter for the first time?"
    question = "Write a 100 word essay about obesity"
    ch = ollama.chat(model = 'llama3.1', messages=[{'role': 'user', 'content': question}], stream = True)
    threading.Thread(target = streamTOredis, args = (ch,)).start()
    return 'bobobo'

def read_redis(id = 0):
    x = redis_client.xread(streams = {"chatid": id}, count=None, block=1000)
    #print(x)
    ## print(x)
    if("d" in x[0][1][-1][1]):
        print(''.join([y[1]['v'] for y in x[0][1][0:-1]]), end='', flush=True)
        print('\nFinished')
        return
    else:
        print(''.join([y[1]['v'] for y in x[0][1]]), end='', flush=True)
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
    return x[0][1][-1][0]

if __name__ == "__main__":
    print('*****')
    vavu = askchat()
    print('-----')
    print(vavu)
    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;')
    vv = 0
    while True:
        vv = read_redis(vv)
        if(vv == None):
            print('Quittting...')
            break
    print('================')
    iasujhdiashjudjhasuio
    time.sleep(2)
    print('>>>>>>>>>>>>')
    read_redis(vv)

    #print(redis_client.xread(streams = {"chatid": 0}, block=1000, count=5000)[1])
    #print('&&&&&&&&&')