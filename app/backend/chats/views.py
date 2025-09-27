from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponseBadRequest
from oauth import VerifyAuthRequest, ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired
from backend.mongo_db_connection import mongo_db, mongo_clinet
import json
from snowflake_id_gen import GenerateSnowflake
import datetime

# Create your views here.

chats = mongo_db['Chats']
data_models = ['Llama 3.0', 'ChatGPT 4.0', 'Llama 2.0']

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
def createChats(request):
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
def renameChats(request):
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
            chat_ret = chats.find_one({"_id": conv_id, "user_id": int(ver_req_auth[1]['iss'])}, {"_id": 0, "chat": 1, "model": 1})
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
def answearQuestion(request):
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