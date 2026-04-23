from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from oauth import ValidateAndCreateJWT, ReturnHttpInvalidJWT, CreateResponseNewAccess
from snowflake_id_gen import GenerateSnowflake
import datetime
import secrets
import string
from .models import Referal
from loginregister.models import User

    
@api_view(['GET'])
def GetAllReferals(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    referal_ret = list(Referal.objects.filter(user_id = valjwt[3]).order_by('-date_created').values('value', 'date_created', 'userid_redeem__email', 'date_redeem', 'userid_redeem__phone'))
    if(len(referal_ret) != 0):
        for i in range(0, len(referal_ret)):
            referal_ret[i]['date_created'] = str(referal_ret[i]['date_created'].replace(microsecond=0))
            if(referal_ret[i]['date_redeem'] != None):
                referal_ret[i]['date_redeem'] = str(referal_ret[i]['date_redeem'].replace(microsecond=0))
    
    return CreateResponseNewAccess(valjwt[1], referal_ret, 200)

@api_view(['POST'])
def CreateReferal(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    referal_id = GenerateSnowflake()
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    referal_value = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))
    user_ret = list(User.objects.filter(id = valjwt[3]).values('is_admin'))[0]
    if(user_ret['is_admin'] == False):
        return HttpResponse(json.dumps('User is not admin'), status = 400)
    referal_ret = Referal.objects.create(id = referal_id,
                                        date_created = curr_time,
                                        user_id = valjwt[3],
                                        value = referal_value,
                                        userid_redeem = None,
                                        date_redeem = None)
    
    ret_json = {"date_created": str(referal_ret.date_created.replace(microsecond=0)),
                "value": referal_ret.value}
    return CreateResponseNewAccess(valjwt[1], ret_json, 200)