from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from oauth import VerifyJWT, ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired
from snowflake_id_gen import GenerateSnowflake
import datetime
import secrets
import string
from .models import Referal
from loginregister.models import User

@api_view(['POST'])
def CreateReferal(request):
    if(request.method == 'POST'):
        if 'access' not in request.COOKIES or 'refresh' not in request.COOKIES:
            return HttpResponse(json.dumps('no jwt provided'), status = 401)
        jwt_r = VerifyJWT(request)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('Not authenticated'), status = 403)
        referal_id = GenerateSnowflake()
        curr_time = datetime.datetime.now(datetime.timezone.utc)
        referal_value = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))
        user_ret = list(User.objects.filter(id = int(jwt_r[1]['iss'])).values('is_admin'))[0]
        if(user_ret['is_admin'] == False):
            return HttpResponse(json.dumps('User is not admin'), status = 400)
        referal_ret = Referal.objects.create(id = referal_id,
                                           date_created = curr_time,
                                           user_id = int(jwt_r[1]['iss']),
                                           value = referal_value,
                                           userid_redeem = None,
                                           date_redeem = None)
        
        ret_json = {"date_created": str(referal_ret.date_created.replace(microsecond=0)),
                    "value": referal_ret.value}
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(ret_json),
                                                                         jwt_r = jwt_r)
        
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)
    
@api_view(['GET'])
def GetAllReferals(request):
    if request.method == 'GET':
        if 'access' not in request.COOKIES or 'refresh' not in request.COOKIES:
            return HttpResponse(json.dumps('no jwt provided'), status = 401)
        jwt_r = VerifyJWT(request)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('Not authenticated'), status = 403)
        referal_ret = list(Referal.objects.filter(user_id = int(jwt_r[1]['iss'])).order_by('-date_created').values('value', 'date_created', 'userid_redeem__email', 'date_redeem', 'userid_redeem__phone'))
        if(len(referal_ret) != 0):
            for i in range(0, len(referal_ret)):
                referal_ret[i]['date_created'] = str(referal_ret[i]['date_created'].replace(microsecond=0))
                if(referal_ret[i]['date_redeem'] != None):
                    referal_ret[i]['date_redeem'] = str(referal_ret[i]['date_redeem'].replace(microsecond=0))
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(referal_ret),
                                                                         jwt_r = jwt_r)
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)