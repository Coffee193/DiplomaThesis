from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponseBadRequest, HttpResponse
from oauth import VerifyAuthRequest, ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired, VerifyJWT, ValidateAndCreateJWT, ReturnHttpInvalidJWT, CreateResponseNewAccess, CreateStreamingResponseNewAccess
from backend.mongo_db_connection import mongo_db
import json
from snowflake_id_gen import GenerateSnowflake
import datetime
from .LLMpipeline import PassLLMThink

###
# For multiplrocessing to work (i.e. to spawn a process) you must run these two lines of code before importing any models.
# When spawning a Process errors are raises that are due to importing models.
# You must run these 2 lines before impoting a model, in the file that spawns a new Process
import django
django.setup()
###
from loginregister.models import User

from loginregister.views import PasswordCheck, CheckDataValue, PasswordCompare
import math
import base64
import os
from ollama import chat
from backend.redis_connection import redis_client
#from backend.process_pool import process_pool
from transformers import AutoTokenizer

import multiprocessing
import concurrent

### remove blow import
import time

# Create your views here.

chats = mongo_db['Chats']
chatdocumentpath = os.environ.get('CHAT_DOCUMENT_PATH')
development = os.environ.get('development')
llm_model = os.environ.get('LLM_MODEL')

@api_view(['GET'])
def getChats(request):
    if(request.method == 'GET'):
        print(request)
        print('LLLLLLLLLLLLLLLLLLLL')
        ver_req_auth = VerifyAuthRequest(request)
        if(ver_req_auth[0] != True):
            return ver_req_auth[1]
        print(ver_req_auth)
        ret = list(chats.aggregate( [{"$match": {"user_id": int(ver_req_auth[1]['iss'])}},
                                     {"$project": {"_id": 1, "name": 1, "date_created": 1}},
                                     {"$sort": {"date_created": 1}}]) ) #sort by date created
        for i in range(0, len(ret)):
            ret[i]["date_created"] = ret[i]["date_created"].timestamp()
            ret[i]["_id"] = str(ret[i]["_id"])
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(ret), jwt_r = ver_req_auth)
    else:
        return HttpResponseBadRequest('Http 400 Bad request')
    
@api_view(['POST'])
def createChats_Old(request):
    if(request.method == 'POST'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            if(data["model"] not in data_models):
                return HttpResponseBadRequest('Http 400 Bad request, model does not exist')
            if(type(data["q"]) != str):
                return HttpResponseBadRequest('Http 400 Bad request, invalid question')
            if(len(data["q"]) == 0):
                return HttpResponseBadRequest('Http 400 Bad Request, question is empty')
                
            chat_id = GenerateSnowflake()
            curr_time = datetime.datetime.now(datetime.timezone.utc)
            chats.insert_one({"_id": chat_id,
                        "name": "Conversation AA",
                        "date_created": curr_time,
                        "user_id": int(ver_req_auth[1]['iss']),
                        "model": data["model"],
                        "chat": [{"q": data["q"], "t": curr_time, "a": "asiojdsi"}]
                        })
            print('^&^&^&')
            print(json.dumps({"_id": chat_id, "name": "Conversation AA", "date_created": curr_time.timestamp()}))
            return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps({"_id": str(chat_id), "name": "Conversation AA", "date_created": curr_time.timestamp()}), jwt_r = ver_req_auth)
        except:
            print('EL GATO')
            return HttpResponseBadRequest('Http 400 Bad request')
    else:
        return HttpResponseBadRequest('Http 400 Bad request, method must be POST')
    
@api_view(['DELETE'])
def deleteChats(request):
    if(request.method == 'DELETE'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            
            if(type(data["_id"]) != str):
                return HttpResponseBadRequest('Http 400 Bad request, invalid id')
            try:
                data["_id"] = int(data["_id"])
            except:
                return HttpResponseBadRequest('Http 400 Bad Request, id could not be converted to int')
            
            chat_del = chats.delete_one({"_id": data["_id"], "user_id": int(ver_req_auth[1]['iss'])})
            if(chat_del.deleted_count != 1):
                return HttpResponseBadRequest('Http 400 Bad Request, Chat was not found')

            return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps('Chat successfully deleted!'), jwt_r = ver_req_auth)
        except:
            return HttpResponseBadRequest('Http 400 Bad request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad request, method must be DELETE')
    
@api_view(['POST'])
def renameChats_old(request):
    if(request.method == 'POST'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            if(type(data["rename"]) != str):
                return HttpResponseBadRequest('Http 400 Bad Request, data type must be str')
            if(len(data["rename"]) > 50):
                return HttpResponseBadRequest('Http 400 Bad Request, conversation name must be 50 characters or less')
            if(len(data["rename"]) < 5):
                return HttpResponseBadRequest('Http 400 Bad Request, conversation name must be more than 5 characters')
            
            # rename
            chat_ret = chats.update_one({"_id": int(data["_id"]), "user_id": int(ver_req_auth[1]['iss'])},
                                        {"$set": {"name": data["rename"]}})
            print(chat_ret)
            if(chat_ret.modified_count == 1):
                return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps('Chat Successfully Renamed'), jwt_r = ver_req_auth)
        except:
            return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request, method must be POST')
    
@api_view(['GET'])
def getChatConv(request, conv_id):
    if(request.method == 'GET'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            #chat_ret = chats.aggregate({"$match": {"_id": conv_id}},
            #                           {"$match": {"user_id": int(ver_req_auth[1]['iss'])}},
            #                           {"$project": {"chat": 1, "_id": 0}})
            chat_ret = chats.find_one({"_id": conv_id, "user_id": int(ver_req_auth[1]['iss'])}, {"_id": 0, "chat": 1})
            if(chat_ret == {}):
                return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
            else:
                for i in range(0, len(chat_ret['chat'])):
                    chat_ret['chat'][i]['t'] = chat_ret['chat'][i]['t'].timestamp()
                chat_ret = {'c': chat_ret['chat'], 'm': chat_ret['model']}
                return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(chat_ret), jwt_r = ver_req_auth)
        except:
            return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request, method must be GET')
    
@api_view(['POST'])
def answearQuestion_Old(request):
    if(request.method == 'POST'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            if(type(data["q"]) != str):
                return HttpResponseBadRequest('Http 400 Bad Request, question type must be string')
            if(len(data["q"]) == 0):
                return HttpResponseBadRequest('Http 400 Bad Request, question is empty')
            curr_time = datetime.datetime.now(datetime.timezone.utc)
            answear = 'YOYOYO'
            chat_ret = chats.update_one({"_id": int(data["c"]), "user_id": int(ver_req_auth[1]['iss'])},
                             {"$push": {"chat": {"q": data["q"], "t": curr_time, "a": answear}}})
            if(chat_ret.modified_count == 1):
                return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps({"a": answear}), jwt_r = ver_req_auth)
            else:
                return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
        except:
            return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request, method must be POST')
    
@api_view(['DELETE'])
def DeleteAllChats_old(request):
    if(request.method == 'DELETE'):
        try:
            if('access' not in request.COOKIES or 'refresh' not in request.COOKIES):
                return HttpResponse(json.dumps('no jwt provided'), status = 401)
            jwt_r = VerifyJWT(request)
            if(jwt_r[0] == False):
                return HttpResponse(json.dumps('not authenticated'), status = 403)
            data = json.loads(request.body.decode('utf-8'))
            if('p' not in data or 'vp' not in data):
                return HttpResponse(json.dumps('Http 400 Bad Request, important values are missing'), status = 400)
            if(type(data['p']) != str or type(data['vp']) != str):
                return HttpResponse(json.loads('Http 400 Bad Request, invalid data types'), status = 400)
            if(data['p'] != data['vp']):
                return HttpResponse(json.dumps('Http 400 Bad Request, passed values are not equal'), status = 400)
            if(CheckDataValue(data['p'], 'password') == False):
                return HttpResponse(json.dumps('Bad Request Passowrd'), status = 400)
            user_password = User.objects.filter(id = int(jwt_r[1]['iss'])).values('password')[0]
            if(PasswordCheck(data['p'], user_password['password']) == False):
                return HttpResponse(json.dumps('Password is incorrect'), status = 409)
            chat_del = chats.delete_many({"user_id": int(jwt_r[1]['iss'])})
            if(math.floor(chat_del.raw_result['ok']) == 1):
                return HttpResponse(json.dumps(chat_del.raw_result['n']), status = 200)
            else:
                return HttpResponse(json.dumps('Http 400 Bad request, something went wrong with deleting chats'), status = 400)
        except:
           return HttpResponse(json.dumps('Http 400 Bad Request, something went wrong'), status = 400)
    else:
        return HttpResponse(json.dumps('Http 400 Bad request, method must be DELETE'), status = 405)
    
@api_view(['GET'])
def GetChats(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    ret = list(chats.aggregate( [{"$match": {"user_id": valjwt[3]}},
                                     {"$project": {"_id": 1, "name": 1, "date_created": 1}},
                                     {"$sort": {"date_created": 1}}]) ) #sort by date created
    for i in range(0, len(ret)):
        ret[i]["date_created"] = ret[i]["date_created"].timestamp()
        ret[i]["_id"] = str(ret[i]["_id"])
    
    return CreateResponseNewAccess(valjwt[1], ret, 200)

@api_view(['POST'])
def RenameChat(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('id' not in data or 'v' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data['v']) < 5):
        return HttpResponse(json.dumps('Conversation name must be more than 5 characters'), status = 400)
    if(len(data['v']) > 50):
        return HttpResponse(json.dumps('Conversation name must be less than 50 characters'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Conversation ID'), status = 400)

    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                                        {"$set": {"name": data["v"]}})
    if(chat_ret.modified_count == 1):
        return CreateResponseNewAccess(valjwt[1], 'Chat successfully renamed', 200)
    else:
        return HttpResponse(json.dumps('Conversation ID does not belong to User'), status = 400)
    
@api_view(['DELETE'])
def DeleteChat(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Conversation ID'), status = 400)
    
    #if(redis_client.exists("cg_" + str(data["id"]))):
    #    return HttpResponse(json.dumps('Cannot delete Chat while answer is generating'), status = 409)

    path_del = list(chats.find({"_id": int(data["id"]), "chat.d": {"$exists": "true"}}, {"paths": "$chat.d.path"}))
    
    chat_del = chats.delete_one({"_id": int(data["id"]), "user_id": valjwt[3]})
    if(chat_del.deleted_count == 1):
        filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        for i in path_del:
            for x in i['paths']:
                if(os.path.exists(filepath + '/' + x)):
                    os.remove(filepath + '/' + x)
        return CreateResponseNewAccess(valjwt[1], 'Chat successfully deleted', 200)
    else:
        return HttpResponse(json.dumps('Conversation ID does not belong to User'), status = 400)
    
@api_view(['POST'])
def CreateChat_Old_NoAI(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data['q']) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    
    chat_id = GenerateSnowflake()
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    chats.insert_one({"_id": chat_id,
                        "name": "New Conversation",
                        "date_created": curr_time,
                        "user_id": valjwt[3],
                        "chat": [{"q": data["q"], "t": curr_time, "a": "asiojdsi"}]
                        })
    
    return CreateResponseNewAccess(valjwt[1], {"_id": str(chat_id), "name": "New Conversation", "date_created": curr_time.timestamp()}, 200)

@api_view(['POST'])
def CreateChat(request):
    content_type = request.headers.get('content-type').split(';')[0]
    if(content_type == 'text/plain'):
        return CreateChatQuestion(request)
    elif(content_type == 'multipart/form-data'):
        return CreateChatDocument(request)
    else:
        return HttpResponse(json.dumps('Invalid Question Headers'), status = 400)

def CreateChatQuestion(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 't' not in data or type(data['t']) != bool):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data['q']) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)

    chat_id = GenerateSnowflake()
    curr_time = datetime.datetime.now(datetime.timezone.utc)

    redis_client.set("cg_" + str(chat_id), json.dumps({"q": data["q"]}))
    if(data['t'] == False):
        p = multiprocessing.Process(target = AnswerQuestionLLM, args=[[], data["q"], str(chat_id)])
    else:
        p = p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[[], data["q"], str(chat_id)])
    t = multiprocessing.Process(target = CreateChatTitle, args = [str(chat_id), data["q"]])
    p.start()
    chats.insert_one({"_id": chat_id,
                        "name": "New Conversation",
                        "date_created": curr_time,
                        "user_id": valjwt[3],
                        "think": data['t'],
                        "chat": []
                        })
    t.start()
    
    return CreateResponseNewAccess(valjwt[1], {"_id": str(chat_id), "name": "New Conversation", "date_created": curr_time.timestamp()}, 200)

def CreateChatDocument(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    request_dict = request.data.dict()
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'data' not in request_dict['document'] or 'name' not in request_dict['document'] or 't' not in request_dict['data'] or type(request_dict['data']) != bool):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    data = json.loads(request_dict['data'])
    file = json.loads(request_dict['document'])
    
    print('******')
    print(file['data'][:29])
    print('-----------')
    print(file['name'][-5:])

    #if(len(file['data']) < 22 or file['data'][:21] != 'data:text/xml;base64,' or file['name'][-4:] != '.xml'):
    #    return HttpResponse(json.dumps('Invalid XML file'), status = 400)

    if(len(file['data']) < 30 or file['data'][:29] != 'data:application/json;base64,' or file['name'][-5:] != '.json'):
        return HttpResponse(json.dumps('Invalid XML file'), status = 400)

    chat_id = GenerateSnowflake()

    file_write = base64.b64decode(file['data'][29:])
    file_id = GenerateSnowflake()

    document_info = {"id": file_id, "name": file['name'], "size": str(round(len(file_write)/1024, 1)), "data": file_write.decode('utf-8')}
    redis_client.set("cg_" + str(chat_id), json.dumps({"u": {"id": str(document_info["id"]), "name": document_info["name"], "size": document_info["size"]}, "q": data["q"]}))

    curr_time = datetime.datetime.now(datetime.timezone.utc)
    file_path = WriteDocument(file_write, {"id": str(document_info['id']), "name": document_info['name'], "size": document_info['size']} , str(chat_id))
    if(data['t'] == False):
        p = multiprocessing.Process(target = AnswerQuestionLLM, args=[[], data["q"], str(chat_id), document_info])
    else:
        p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[[], data["q"], str(chat_id), {"id": document_info["id"], "name": document_info["name"], "size": document_info["size"], "path": file_path}])
    if(data["q"] != ""):
        t = multiprocessing.Process(target = CreateChatTitle, args = [str(chat_id), data["q"], document_info["data"], document_info["name"]])
    else:
        t = multiprocessing.Process(target = CreateChatTitle, args = [str(chat_id), data["q"], document_info["data"], document_info["name"]])

    p.start()
    chats.insert_one({"_id": chat_id,
                      "name": "New Conversation",
                      "date_created": curr_time,
                      "user_id": valjwt[3],
                      "think": data['t'],
                      "chat": []})
    t.start()

    return CreateResponseNewAccess(valjwt[1], {"_id": str(chat_id), "name": "New Conversation", "date_created": curr_time.timestamp()}, 200)

@api_view(['GET'])
def GetConversation(request, conv_id):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    chat_ret = chats.find_one({"_id": conv_id, "user_id": valjwt[3]}, {"_id": 0, "chat": 1, "think": 1})
    if(chat_ret == {}):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    else:
        for i in range(0, len(chat_ret['chat'])):
            chat_ret['chat'][i]['t'] = chat_ret['chat'][i]['t'].timestamp()
            if('d' in chat_ret['chat'][i]):
                chat_ret['chat'][i]['d']['id'] = str(chat_ret['chat'][i]['d']['id'])
        chat_ret = {'c': chat_ret['chat'], 't': chat_ret['think']}

        gen_chat = redis_client.get("cg_" + str(conv_id))
        if(gen_chat != None):
            chat_ret['g'] = json.loads(gen_chat) # g -> generation
        return CreateResponseNewAccess(valjwt[1], chat_ret, 200)

@api_view(['POST'])
def AskQuestion(request):
    content_type = request.headers.get('content-type').split(';')[0]
    if(content_type == 'text/plain'):
        #return AnswearQuestion(request)
        return AnswerQuestion(request)
    elif(content_type == 'multipart/form-data'):
        print('^^^^^^^^^^^^')
        return AnswerQuestionWithDocument(request)
    else:
        return HttpResponse(json.dumps('Invalid Question Headers'), status = 400)

def AnswearQuestion(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 'id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data["q"].replace('\n', '')) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    
    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1})
    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        redis_client.set("cg_" + data["id"], 1)
        #*#
        p = multiprocessing.Process(target = AnswerQuationLLM, args = [chat_ret['chat'], data["q"], data["id"]])
        p.start()
        #process_pool.submit(AnswerQuationLLM, chat_ret['chat'], data["q"], data["id"])
        # redis_queue.enqueue(AnswerQuationLLM, chat_ret['chat'], data["q"], data["id"])
        # vuvuvu = AnswerQuationLLM.delay(chat_ret['chat'], data["q"], data["id"])
        # print(vuvuvu)
        # print(type(vuvuvu))
        # print('asked celery...')
        return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [data["id"]], 200)
        # return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [chat_ret["id"], 1, 10])
        return CreateStreamingResponseNewAccess(valjwt[1], AnswearQuestionLLM, [chat_ret['chat'], data["q"], int(data["id"])], 200)
        return StreamingHttpResponse(AnswearQuestionLLM(chat_ret['chat'], data["q"], int(data["id"])), status = 200)
        print(chat_ret)
        print('----------------------------------')
        return CreateResponseNewAccess(valjwt[1], {"a": 'bububu'}, 200)

#@shared_task
def AnswerQuationLLM_Old_HasListNotStream(db_chat, user_question, chat_id):
    llm_chat = []
    # total_answer = ''
    for conv in db_chat:
        llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    llm_chat.append({'role': 'user', 'content': user_question})

    llm_answer = chat(llm_model, messages = llm_chat, stream = True)

    for chunk in llm_answer:
        redis_client.append("ci_" + chat_id, chunk.message.content)
        # yield chunk.message.content
        # total_answer += chunk.message.content
        
        print('talk talk...........')
        if(chunk.done == True):
            total_answer = redis_client.getrange("ci_" + chat_id, 0, -2)
            redis_client.append("ci_" + chat_id, "=$*$=")
            redis_client.expire("ci_" + chat_id, 2)
            print('done streaming....................')
            chats.update_one({"_id": chat_id},
                             {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})

#@shared_task
def AnswerQuationLLM_Old_Celery(db_chat, user_question, chat_id):
    llm_chat = []
    total_answer = ''
    for conv in db_chat:
        llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    llm_chat.append({'role': 'user', 'content': user_question})

    print('SUPAAAAAAA POWAAAAAAA ************')

    try:
        llm_answer = chat(llm_model, messages = llm_chat, stream = True)
    except:
        redis_client.delete("cg_" + chat_id)
        return

    # redis_client.set("cg_" + chat_id, 1) # cg_ -> chat generation

    for chunk in llm_answer:
        
        if(chunk.done == True):
            redis_client.delete("cg_" + chat_id)
            redis_client.xadd("ci_" + chat_id, {"d": 1}) # d -> done # ci_ -> chat id
            redis_client.expire("ci_" + chat_id, 3)
            chats.update_one({"_id": int(chat_id)},
                                        {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})
            return

        total_answer += chunk.message.content
        redis_client.xadd("ci_" + chat_id, {"v": chunk.message.content})

def AnswerQuationLLM(db_chat, user_question, chat_id):
    llm_chat = []
    total_answer = ''
    for conv in db_chat:
        llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    llm_chat.append({'role': 'user', 'content': user_question})

    print('SUPAAAAAAA POWAAAAAAA ************')

    try:
        llm_answer = chat(llm_model, messages = llm_chat, stream = True)
    except:
        redis_client.delete("cg_" + chat_id)
        return

    for chunk in llm_answer:
        
        if(chunk.done == True):
            redis_client.delete("cg_" + chat_id)
            redis_client.xadd("ci_" + chat_id, {"d": 1}) # d -> done # ci_ -> chat id
            redis_client.expire("ci_" + chat_id, 3)
            chats.update_one({"_id": int(chat_id)},
                                        {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})
            return

        total_answer += chunk.message.content
        redis_client.xadd("ci_" + chat_id, {"v": chunk.message.content})

def GetLLMAnswerStream_Old_HasListNotStream(chat_id, breakout_time = 1, max_retries = 10):
    redis_chatid = "ci_" + chat_id
    stream_start = 0

    for i in range(0, max_retries):
        if(redis_client.exists(redis_chatid) == True):
            llm_chunk = redis_client.getrange(redis_chatid, stream_start, -1)
            if(llm_chunk == "=$*$="):
                return
            yield llm_chunk
            stream_start += len(llm_chunk)

    return HttpResponse(json.dumps('Server stream timed out'), status = 504)

def GetLLMAnswerStream_Old_ReturnedAnswerAsString(chat_id, block_time = 20000):
    if(redis_client.exists("cg_" + chat_id) == True):
        stream_id = "cs_" + chat_id
        series_id = 0
        yield ''
        while True:
            x = redis_client.xread(streams = {stream_id: series_id}, count = None, block = block_time)
            print(x[0][1])
            print('<<<<<<<<<<<<')
            if(len(x) == 0):
                print('***^^^&&&')
                print(x)
                print('Timed Out')
                return 'Timed Out'
            if("d" in x[0][1][-1][1]):
                yield ''.join([y[1]['v'] for y in x[0][1][0:-1]])
                print('Retrieval successfully finished!')
                return
            else:
                yield ''.join([y[1]['v'] for y in x[0][1]])

            series_id = x[0][1][-1][0]
    else:
        return 'Something went wrong with the retrieval'

def GetLLMAnswerStream(chat_id, block_time = 60000, with_title = False):
    print(with_title)
    print('>>START<<')
    if(redis_client.exists("cg_" + chat_id) == True):
        stream_id = "cs_" + chat_id
        series_id = 0
        title_generated = False
        done = False
        yield json.dumps({'v': ''}) # Must have this so that COOKIES are instanly returned to user
        # t -> title, d -> done, v -> value, u -> uploaded document
        # time.sleep(0.5)
        while True:
            x = redis_client.xread(streams = {stream_id: series_id}, count = None, block = block_time)
            print(x)
            print(x[0][1])
            #print(''.join(y[1]['t'] for y in x[0][1] if 't' in y[1]))
            print(any('t' in y[1] for y in x[0][1]))
            print('<<<<<<<<<<<<')
            if(len(x) == 0):
                print('***^^^&&&')
                print(x)
                print('Timed Out')
                return 'Timed Out'
            if(with_title == True and title_generated == False):
                if(any('t' in y[1] for y in x[0][1])):
                    print('Title Generated')
                    yield json.dumps({'t': ''.join(y[1]['t'] for y in x[0][1] if 't' in y[1])})
                    title_generated = True
                if(not any('v' in y[1] for y in x[0][1])):
                    series_id = x[0][1][-1][0]
                    continue
            
            if(any('u' in y[1] for y in x[0][1])):
                print('yeeeeeeeeeeeeeees')
                val_ret = {"u": next(json.loads(y[1]['u']) for y in x[0][1] if 'u' in y[1])}
                if(any('v' in y[1] for y in x[0][1])):
                    val_ret['v'] = ''.join(y[1]['v'] for y in x[0][1] if 'v' in y[1])
                print(val_ret)
                yield json.dumps(val_ret)
                series_id = x[0][1][-1][0]
                continue

            # case where t comes after d
            if("d" in x[0][1][-1][1] or (len(x[0][1]) > 1 and "d" in x[0][1][-2][1]) ):
                yield json.dumps({'v': ''.join(y[1]['v'] for y in x[0][1][0:-1] if 'v' in y[1])})
                print('Is Done')
                done = True
            else:
                yield json.dumps({'v': ''.join(y[1]['v'] for y in x[0][1] if 'v' in y[1])})
            if(done == True):
                if(with_title == True and title_generated == False):
                    continue
                print('Returning Done')
                return

            series_id = x[0][1][-1][0]
    else:
        return 'Something went wrong with the retrieval'

'''
Old answerquestion. Works ok. Problem: if user closes the http connection (ie. Browser closes), then the Stream stops as well.
To tackle this you'll need to launch a separate proccess, in which the LLM writes the answer to redis as RedisStream and does all the other stuff of the function (ex.
Update Mongodb). You cannot start a new process using multiprocessing from within django. You must use Task Queue tools like Celery. All of these tools however, run only
on Linux. So Docker is necessary.
'''
def AnswearQuestion_Old_NoCelery(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 'id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data["q"].replace('\n', '')) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    
    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1})
    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        return CreateStreamingResponseNewAccess(valjwt[1], AnswearQuestionLLM, [chat_ret['chat'], data["q"], int(data["id"])], 200)
        return StreamingHttpResponse(AnswearQuestionLLM(chat_ret['chat'], data["q"], int(data["id"])), status = 200)
        print(chat_ret)
        print('----------------------------------')
        return CreateResponseNewAccess(valjwt[1], {"a": 'bububu'}, 200)
'''
The below function is an exact copy of the above. For the scope of the diploma thesis, it is considered too much to add all those stuff, as it would require to setup
a docker enviroment and configure everything around it. Instead we'll keep it simpler and simply we will not change close the connection or change the conversation tab
while the AI is generating a response
'''
def AnswerQuestion(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 'id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data["q"].replace('\n', '')) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    
    if(redis_client.exists("cg_" + data["id"])):
        return HttpResponse(json.dumps('Cannot ask question. An answer for a previous question is being generated'), status = 409)

    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1, "chat.d": 1, "think": 1})
    print(chat_ret)
    print('*****')

    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        redis_client.set("cg_" + data["id"], json.dumps({"q": data["q"]})) # cg -> chat generation
        #multiprocessing.set_start_method('fork')
        if(chat_ret['think'] == False):
            p = multiprocessing.Process(target = AnswerQuestionLLM, args=[chat_ret['chat'], data["q"], data["id"]])
        else:
            p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[chat_ret['chat'], data["q"], data["id"]])
        p.start()
        return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [data["id"]], 200)
        #return CreateStreamingResponseNewAccess(valjwt[1], AnswerQuestionLLM, [chat_ret['chat'], data["q"], int(data["id"])], 200)

'''
old answerquestionllm. Works. It was the initial function called by AnswerQuestion. Since these 2 are packed together, they share the same issues
'''
def AnswearQuestionLLM_Old_NoCelery(db_chat, user_question, chat_id):
    llm_chat = []
    total_answer = ''
    for conv in db_chat:
        llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    llm_chat.append({'role': 'user', 'content': user_question})

    llm_answer = chat(llm_model, messages = llm_chat, stream = True)

    for chunk in llm_answer:
        yield chunk.message.content
        total_answer += chunk.message.content
        
        print('talk talk...........')
        if(chunk.done == True):
            print('done streaming....................')
            chats.update_one({"_id": chat_id},
                             {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})
'''
The below function is an exact copy of the above.
'''
def AnswerQuestionLLM(db_chat, user_question, chat_id, document_dict = None):
    llm_chat = []
    total_answer = ''

    for conv in db_chat:
        if 'd' in conv:
            if 'q' in conv:
                user_prompt = f"""User uploaded a document, the data of whuch are the following:
{conv['d']['data']}
--------------------
Then the User asked the following question based on the data provided previously: {conv['q']}
"""
            else:
                user_prompt = f"""User uploaded a document, the data of which are the following:
{conv['d']['data']}
"""
            llm_chat += [{'role': 'user', 'content': user_prompt}, {'role': 'assistant', 'content': conv['a']}] 

        else:
            llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    
    if(document_dict == None):
        llm_chat.append({'role': 'user', 'content': user_question})
    else:
        if(user_question == ''):
            user_prompt = f"""The user uploaded a file, the data of which are the following:
{document_dict['data']}

----------------------------

Read the data carefully and based on that data, state what type of file it is and what is it about. Then make a statement about offering your assistance with any task

================

Example:
It seems you've uploaded a scheduling plan in XML format. I can help with various tasks related to this file. I'll do my best to assist you with extracting information or performing calculations on the data.
"""
        else:
            user_prompt = f"""The user uploaded a file, the data of which are the following:
{document_dict['data']}

----------------------------

Read the data carefully and based on that data, answer the following question:
{user_question}
"""
        
        llm_chat.append({'role': 'user', 'content': user_prompt})

    print('SUPAAAAAAA POWAAAAAAA ************')

    try:
        llm_answer = chat(llm_model, messages = llm_chat, stream = True)
    except:
        redis_client.delete("cg_" + chat_id)
        return

    # redis_client.set("cg_" + chat_id, 1) # cg_ -> chat generation

    for chunk in llm_answer:
        
        if(chunk.done == True):
            redis_client.delete("cg_" + chat_id)
            redis_client.xadd("cs_" + chat_id, {"d": 1}) # d -> done # cs_ -> chat stream
            redis_client.expire("cs_" + chat_id, 3)
            if(document_dict == None):
                lololo = chats.update_one({"_id": int(chat_id)},
                                            {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})
            else:
                push_val = {"t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer, "d": document_dict}
                if(user_question != ''):
                    push_val['q'] = user_question
                lololo = chats.update_one({"_id": int(chat_id)},
                                          {"$push": {"chat": push_val}})
            return

        total_answer += chunk.message.content
        redis_client.xadd("cs_" + chat_id, {"v": chunk.message.content})

@api_view(['GET'])
def ResumeAnswerStream(request, conv_id):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [str(conv_id), 20000, True if request.GET.get('t') == '' else False], 200)

def AA(popo):
    print(';;;;;;;;')
    time.sleep(5)
    print(popo)
    return True

def AnswerQuestionWithDocument(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    request_dict = request.data.dict()
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'id' not in request_dict['data'] or 'data' not in request_dict['document'] or 'name' not in request_dict['document']):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    data = json.loads(request_dict['data'])
    file = json.loads(request_dict['document'])
    
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    #if(len(file['data']) < 22 or file['data'][:21] != 'data:text/xml;base64,' or file['name'][-4:] != '.xml'):
    #    return HttpResponse(json.dumps('Invalid XML file'), status = 400)
    if(len(file['data']) < 30 or file['data'][:29] != 'data:application/json;base64,' or file['name'][-5:] != '.json'):
        return HttpResponse(json.dumps('Invalid XML file'), status = 400)
    
    if(redis_client.exists("cg_" + data["id"])):
        return HttpResponse(json.dumps('Cannot ask question. An answer for a previous question is being generated'), status = 409)
    
    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1, "chat.d": 1, "think": 1})

    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        file_write = base64.b64decode(file['data'][21:])
        file_id = GenerateSnowflake()

        document_info = {"id": file_id, "name": file['name'], "size": str(round(len(file_write)/1024, 1)), "data": file_write.decode('utf-8')}
        redis_client.set("cg_" + data["id"], json.dumps({"u": {"id": str(document_info["id"]), "name": document_info["name"], "size": document_info["size"]}, "q": data["q"]}))

        file_path = WriteDocument(file_write, {"id": str(document_info['id']), "name": document_info['name'], "size": document_info['size']} , data['id'])
        #d = multiprocessing.Process(target = WriteDocument, args=[file['data'], file_id, file["name"], data['id']])
        if(chat_ret['think'] == False):
            p = multiprocessing.Process(target = AnswerQuestionLLM, args=[chat_ret['chat'], data["q"], data["id"], document_info])
        else:
            document_info = {"id": document_info["id"], "name": document_info["name"], "size": document_info["size"], "path": file_path}
            p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[chat_ret['chat'], data["q"], data["id"], document_info])
        #d.start()
        p.start()

        return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [data["id"]], 200)
    
    
    file_write = base64.b64decode(file['data'][21:])
    file_id = GenerateSnowflake()
    
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    answear = 'YOYOYO'
    chat_val = {"d": {"name": file['name'], "path": data['id'] + '_' + str(file_id) + '.xml', "size": str(round(len(file_write)/1024, 1))}, "t": curr_time, "a": answear}
    if(len(data["q"].replace('\n', '')) != 0):
        chat_val["q"] = data["q"]
    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                        {"$push": {"chat": chat_val}})
    
    if(chat_ret.modified_count == 1):
        filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        with open(chatdocumentpath + '/' + data['id'] + '_' + str(file_id) + '.xml', 'wb') as file:
            file.write(file_write)
        return CreateResponseNewAccess(valjwt[1], {"a": answear}, 200)
    else:
        return HttpResponse(json.dumps('Conversation does not belong to User'), status = 400)

def WriteDocument(file_data, document_info, conv_id):
    file_type = document_info['name'].split(".")[-1]
    file_path = chatdocumentpath + '/' + conv_id + '_' + document_info['id'] + '.' + file_type
    with open(file_path, 'wb') as file:
        file.write(file_data)

    redis_client.xadd("cs_" + conv_id, {"u": json.dumps(document_info)})
    return file_path

def AnswearQuestion_NewOld_NoAI(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 'id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data["q"].replace('\n', '')) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    answear = 'YOYOYO'
    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                        {"$push": {"chat": {"q": data["q"], "t": curr_time, "a": answear}}})
    if(chat_ret.modified_count == 1):
        return CreateResponseNewAccess(valjwt[1], {"a": answear}, 200)
    else:
        return HttpResponse(json.dumps('Conversation does not belong to User'), status = 400)

@api_view(['DELETE'])
def DeleteAllChats(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('v' not in data or 't' not in data or data['t'] != 'password'):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    
    user_password = User.objects.filter(id = valjwt[3]).values('password')[0]
    if(PasswordCompare(data['v'], user_password['password']) == False):
        return CreateResponseNewAccess(valjwt[1], 'Password is incorrect', 409)
    
    path_del = list(chats.find({"user_id": valjwt[3], "chat.d": {"$exists": "true"}}, {"paths": "$chat.d.path"}))

    chat_del = chats.delete_many({"user_id": valjwt[3]})
    if(math.floor(chat_del.raw_result['ok']) == 1):
        filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        for i in path_del:
            for x in i['paths']:
                if(os.path.exists(filepath + '/' + x)):
                    os.remove(filepath + '/' + x)
        return CreateResponseNewAccess(valjwt[1], chat_del.raw_result['n'], 200)
    else:
        return HttpResponse(json.dumps('Could not delete the Chats'), status = 400)
    
def AnswearQuestionWithDocument(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    request_dict = request.data.dict()
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'id' not in request_dict['data'] or 'data' not in request_dict['document'] or 'name' not in request_dict['document']):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    data = json.loads(request_dict['data'])
    file = json.loads(request_dict['document'])
    
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    if(len(file['data']) < 22 or file['data'][:21] != 'data:text/xml;base64,' or file['name'][-4:] != '.xml'):
        return HttpResponse(json.dumps('Invalid XML file'), status = 400)
    
    file_write = base64.b64decode(file['data'][21:])
    file_id = GenerateSnowflake()

    curr_time = datetime.datetime.now(datetime.timezone.utc)
    answear = 'YOYOYO'
    chat_val = {"d": {"name": file['name'], "path": data['id'] + '_' + str(file_id) + '.xml', "size": str(round(len(file_write)/1024, 1))}, "t": curr_time, "a": answear}
    if(len(data["q"].replace('\n', '')) != 0):
        chat_val["q"] = data["q"]
    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                        {"$push": {"chat": chat_val}})
    
    if(chat_ret.modified_count == 1):
        #filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        with open(chatdocumentpath + '/' + data['id'] + '_' + str(file_id) + '.xml', 'wb') as file:
            file.write(file_write)
        return CreateResponseNewAccess(valjwt[1], {"a": answear}, 200)
    else:
        return HttpResponse(json.dumps('Conversation does not belong to User'), status = 400)
    
def CreateChatTitle(chat_id, user_question = "", document_content = None, document_name = None, max_doc_token_len = 3000):
    llm_classify = 2
    if(document_content != None and user_question == ""):
        llm_classify = 1
    elif(document_content != None):

        prompt_classify = f"""You are an AI assistant that generates titles for conversations involving uploaded files.

Your first task is to determine the type of user request.

CLASSIFY THE REQUEST INTO ONE OF TWO CATEGORIES:

1. GENERAL FILE REQUEST
Use this when:
- The user uploads a file and asks nothing
- The user question makes no sense, is a random string
- The user asks general questions such as:
- "What is this file about?"
- "What are the contents of this file?"
- "Explain this file"
- "Summarize this document"
- "Describe this file"


2. SPECIFIC FILE INFORMATION REQUEST

Use this when the user asks about specific information inside the file, such as:
- requesting data
- asking questions about particular fields
- requesting extraction or explanation of specific content
- referring to specific sections, values, or records
- The user input contains gibberish, random characters, meaningless text, or input that cannot be interpreted (e.g., "asdjkl123!@#", "??!!aa", random symbols, or nonsensical strings). These should default to this category.

--------
Return only the number 1 or 2 and nothing else

User Question:
{user_question}
"""
        llm_chat = [{'role': 'user', 'content': prompt_classify}]
        try:
            llm_classify = int(chat(llm_model, messages = llm_chat).message.content)
        except:
            return
        
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
    tokens = tokenizer.tokenize(document_content)
    if(len(tokens) > max_doc_token_len):
        document_content = tokenizer.convert_tokens_to_string(tokens[0 : max_doc_token_len])
    print('|||||||||||||||||||')
    print(document_content)

    if(llm_classify == 1):
        title_prompt = f"""You are an AI assistant that analyzes uploaded files.
Your task is to generate ONLY a short descriptive title for the file.

Rules:
1. Output ONLY the title.
2. Do NOT include explanations, sentences, or bullet points.
3. Do NOT include extra text before or after the title.
4. Use simple, clear wording.
5. Avoid complex or technical vocabulary.

Examples of valid outputs:
PDF File Analysis
XML File Breakdown
JSON File Overview
CSV Data Summary
Schedule Planning File Contents
Text Document Overview

The response must contain exactly one short title.
{f"\nUser Question:\n{user_question}" if user_question != "" else ""}
--- File: {document_name} ---
{document_content}
--- End of {document_name} ---"""
    else:
        title_prompt = f"""You are an AI assistant that creates concise, descriptive titles for chat conversations.

Given the conversation below, generate a short title (max 5-7 words) that clearly captures the main topic or purpose of the discussion.

Guidelines:
- Be specific and informative, not vague
- Avoid unnecessary filler words
- Do not include punctuation like quotes or periods at the end
- Use title case (capitalize major words)
- Focus on the core intent of the conversation
- If the input doesn't make sense, simply output one of the following: Unclear Input | Unclear Request | Incomplete Input
- If the input is friendly and general, don't make the title too complicated
- focus solely on the core intent of the conversation and avoid adding unnecessary, extra words. Do not be verbose
- Avoid adding the words 'Needed' 'Description', especially at the end of the title
- If asked about certain information, avoid assuming where that information comes from (Database, File, USB device) unless mentioned

User Question:
{user_question}
"""
        if document_content != None:
            title_prompt += f"""
--- File: {document_name} ---
{document_content}
--- End of {document_name} ---"""

    llm_chat = [{'role': 'user', 'content': title_prompt}]
    try:
        llm_title = chat(llm_model, messages = llm_chat)
    except:
        return
    
    llm_title = llm_title.message.content
    chats.update_one({"_id": int(chat_id)},
                     {"$set": {"name": llm_title}})
    
    redis_client.xadd("cs_" + chat_id, {"t":llm_title})
    
@api_view(['POST'])
def Slow_Func_Test(request):
    print('aaaa...')
    for _ in range(0, 3):
        time.sleep(3)
        print('bububu')
    return HttpResponse(json.dumps('lulaaaaaaa'), status = 200)

def AnswerQuestionLLMThink(db_chat, user_question, chat_id, document_dict = None):
    llm_chat = []
    total_answer = ''

    for conv in db_chat:
        if 'd' in conv:
            if 'q' in conv:
                prompt = f"""User Question:
{conv['q']}

-----------------------
The user has also uploaded a file located at:
{conv['d']['path']}"""
            else:
                prompt = f"""The user has uploaded a file located at:
{conv['d']['path']}"""

            llm_chat += [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': conv['a']}] 
        else:
            llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]

    if document_dict == None:
        llm_chat.append({'role': 'user', 'content': user_question})
    else:
        if(user_question == ''):
            prompt = f"""You are interacting with a user who has uploaded a file in JSON format.

Your task is simple:

- Acknowledge that you can see the user has uploaded a JSON file named {document_dict['name']}.
- Do not analyze or interpret the file yet.
- Offer help by asking if the user would like you to analyze, explain, validate, or get the JSON data.

Keep your response short, polite, and helpful. Avoid making assumptions about the contents of the file."""
            llm_chat.append({'role': 'user', 'content': prompt})
        else:
            llm_chat.append({'role': 'user', 'content': user_question})

    try:
        llm_answer = PassLLMThink(llm_model, user_question, document_dict['path'] if document_dict != None else None)
        #llm_answer = chat(llm_model, messages = llm_chat, stream = True)
    except:
        redis_client.delete("cg_" + chat_id)
        return
    
    for chunk in llm_answer:
        
        if(chunk.done == True):
            redis_client.delete("cg_" + chat_id)
            redis_client.xadd("cs_" + chat_id, {"d": 1}) # d -> done # cs_ -> chat stream
            redis_client.expire("cs_" + chat_id, 3)
            if(document_dict == None):
                chats.update_one({"_id": int(chat_id)},
                                {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})
            else:
                push_val = {"t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer, "d": document_dict}
                if(user_question != ''):
                    push_val['q'] = user_question
                chats.update_one({"_id": int(chat_id)},
                                {"$push": {"chat": push_val}})
            return

        total_answer += chunk.message.content
        redis_client.xadd("cs_" + chat_id, {"v": chunk.message.content})