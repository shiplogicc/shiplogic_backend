from datetime import datetime
from email.mime import application
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .models import *
from oauth2_provider.models import Application, AccessToken, RefreshToken
from rest_framework.decorators import authentication_classes, permission_classes
import requests
import random
import string
# Create your views here.

@authentication_classes([])
@permission_classes([])
class LoginAPI(APIView):
    def _handleLogin(self, user, request, username, password):
        if not Application.objects.filter(user=user).exists():
            appObj = Application()
            clientId = appObj.client_id
            clientSecret = appObj.client_secret
            appObj.user=user
            appObj.authorization_grant_type="password"
            appObj.client_type="confidential"
            appObj.save()
            UserSecretCredentials.objects.create(user = user, client_id = clientId, client_secret = clientSecret)
        #appObj = Application.objects.filter(user = user)
        usc = UserSecretCredentials.objects.filter(user = user)
        if usc:
            usc = usc.latest('id')
            client_id = usc.client_id
            client_secert = usc.client_secret
            #url = settings.BASE_API_URL+'/o-auth/token/'
            url = "http://"+request.get_host()+'/o/token/'
            print (url)
            data_dict = {"grant_type":"password","username":username,"password":password, "client_id":client_id,"client_secret":client_secert}
            print ("oauth_request", url, data_dict)
            aa = requests.request("POST", url, data=data_dict, verify=False)
            data = json.loads(aa.text)
            print ("oauth_response", data)
            data.pop('scope', None)
            data.pop('refresh_token', None)
            profile_verified = UserLogin.objects.get(user).profile_verified
            if data.get("access_token", None):
                token_obj = AccessToken.objects.filter(user_id = user, token = data.get("access_token", None))
                if token_obj:
                    data["expires"] = token_obj[0].expires
                data["status"] = "success"
            data['profile_verified'] = profile_verified
            return data

    def get(self, request):
        username = request.GET.get('username', None)
        password = request.GET.get('password', None)
        if not username and password:
            return Response({"status":"failed", "err":"Incorrect username/password!"})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                logout(request)
                login(request, user)
                expire_time = datetime.now()
                token = ''

                token_obj = AccessToken.objects.filter(user_id = user, expires__gt = expire_time)
                if token_obj:
                    token_obj = token_obj.latest('id')
                    token = token_obj.token
                    print (user, token)
                    token_obj.expres = datetime.now()
                    return Response(self._handleLogin(user, request, username, password))
                else:
                    return Response(self._handleLogin(user, request, username, password))
            else:
                return Response({"status":"failed", "err":"User deactivated!"})
        else:
            return Response({"status":"failed", "err":"Incorrect username/password!"})
    def post(self, request):
        print ("post",request.POST)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username and password:
            return Response({"status":"failed", "message":"Incorrect username/password!"})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                expire_time = datetime.now()
                token = ''

                token_obj = AccessToken.objects.filter(user_id = user, expires__gt = expire_time)
                if token_obj:
                    token_obj = token_obj.latest('id')
                    token = token_obj.token
                    print (user, token)
                    token_obj.expres = datetime.now()
                    return Response(self._handleLogin(user, request, username, password))
                else:
                    return Response(self._handleLogin(user, request, username, password))
            else:
                return Response({"status":"failed", "message":"User deactivated!"})
        else:
            return Response({"status":"failed", "message":"Incorrect username/password!"})

class ValidateSession(APIView):
    def get(self, request):
        return Response({"status": "success", "message": "Authorized"})

class LogoutApi(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION',None)
        print (request.user, token)
        if token:
            token = token.split(' ')[1]
            token_obj = AccessToken.objects.filter(user_id = request.user, token = token)
            if token_obj:token_obj.delete()
        logout(request)
        return Response({"status": "success", "message": "LoggedOut"})



@authentication_classes([])
@permission_classes([])
class SignUp(APIView):
    def post(self,request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        mobile = request.data.get('mobile_no')
        account_type = request.data.get('account_type')
        if full_name == "" or not full_name:
            return Response({"status": "success", "message": "Full Name can not be Null"})
        if email == "" or not email:
            return Response({"status": "success", "message": "Email ID can not be Null"})
        if email == "" or not mobile:
            return Response({"status": "success", "message": "Mobile can not be Null"})
        
        try:
            user = User.objects.get(username = email)
        except:
            user = User.objects.create(username = email)
        try: 
            user_login = UserLogin.objects.get(user = user) 
            return Response({"status":'success',"message":"User Already Exists"})
        except:
            user_login = UserLogin.objects.create(user = user,fullname = full_name,mobile = mobile,user_type = "customer",email = email,)
            password = ''.join(random.choice(string.ascii_lowercase+string.digits)for _ in range(10))
            user.set_password(password)
            if account_type == 1:
                contact_person = Contact.objects.create(name = full_name,designation = "self",email = email,address_line1 = "demo",address_line2 = "demo",address_line3 = "demo",city = "demo",pincode = "demo",phone = mobile)
                cust = Customer.objects.filter(customer_type = 1)
                if cust:
                    code = cust.code+1
                else:
                    code = 1000
                customer = Customer.objects.create(name = full_name,code = code,email = email,mobile_no = mobile)

            return ({"status": "success", "message": "Username & Password has been sent to you email id ","pasword":password,"account_type":account_type})




        
