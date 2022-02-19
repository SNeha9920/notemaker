import json

from django.core.mail import send_mail
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from rest_framework import status
from datetime import datetime, time, timedelta
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import requests
from django.db import transaction
from django.db.models import Q
from uuid import uuid4
from urllib3.exceptions import InsecureRequestWarning
from django.utils.html import escape
from django.contrib.auth.hashers import *
from .models import Tokens
from rest_framework.response import Response

HEADERS = {"":""}
BASE_URL = ""

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Create your views here.

# TOKEN CHECKER
def TokenChecker(Wrapped):
    def wrapper(*args, **kwargs):
        request = args[0]

        try:
            tokenval = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            userid = request.META['HTTP_AUTHORIZATION'].split(' ')[2]
        except (KeyError, IndexError):
            return HttpResponse('<h1>Unauthorized(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = Signup.objects.get(id=userid)
        except Signup.DoesNotExist:
            return HttpResponse('<h1>Unauthorized(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = Tokens.objects.get(user=user)
        except Tokens.DoesNotExist:
            return HttpResponse('<h1>Unauthorized(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

        # VALID LOGIN
        if token.value == tokenval and token.valid_upto > timezone.now():
            return Wrapped(*args, **kwargs)

        else:
            return HttpResponse('<h1>Token Expired(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

    return wrapper

# COMMON SIGNUP FOR ALL USERS
@csrf_exempt
@api_view(['POST', 'PUT'])
def user_signup(request):
    if request.method == 'PUT' or request.method == 'POST':
        data = request.data
        # print(data)

        if not data['email'] or not data['first_name'] or not data['last_name'] or not data['gender'] or not data['mobile_no'] or not data['password']:
            return JsonResponse({"Message": "Coudln't get data from site"}, status=status.HTTP_204_NO_CONTENT)

        else:
            existing_email = Signup.objects.filter(email=data['email'])
            if not existing_email:
                data['password'] = make_password(data['password'],salt=None,hasher='default')
                general_serialized = SignupSerializer(data=data)
                if general_serialized.is_valid():
                    general_serialized.save()
            else:
                return JsonResponse({"Message": "Email Already Exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return JsonResponse({"Message": "Account Created Successfully"}, status=status.HTTP_201_CREATED)


    else:
        # Wrong Request method
        return JsonResponse({"Message": "Wrong Request Method"}, status=status.HTTP_400_BAD_REQUEST)



#COMMON LOGIN FOR ALL USERS
@csrf_exempt
@api_view(['POST', 'PUT'])
def user_login(request):
    if request.method == 'PUT' or request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({"Message": "Coudln't get data from site"}, status=status.HTTP_204_NO_CONTENT)


        try:
            userobj = Signup.objects.get(email=email)
            if userobj.status == False:
                return JsonResponse({"Message": "Invalid Login"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({"Message": "Invalid Login"}, status=status.HTTP_401_UNAUTHORIZED)

        user_serializer = SignupSerializer(userobj)

        if check_password(password,userobj.password):
            # Login Accepted
            try:
                token = Tokens.objects.get(user=userobj)
                token.delete()
            except Tokens.DoesNotExist:
                pass
            token_code = str(uuid4())
            Tokens.objects.create(value=token_code, valid_upto=timezone.now() + timedelta(minutes=120), user=userobj)

            o = user_serializer.data
            o['auth_token'] = token_code
            return Response(data=o, status=status.HTTP_200_OK)

        else:
            # Bad Login
            return JsonResponse({"Message": "Invalid Login"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Wrong Request method
        return JsonResponse({"Message": "Wrong Request Method"}, status=status.HTTP_400_BAD_REQUEST)


# COMMON LOGOUT FOR ALL USERS
@csrf_exempt
@api_view(['POST', 'PUT'])
def logout(request, userid):
    if request.method == 'POST' or request.method == 'PUT':
        if not userid:
            return JsonResponse({"Message": "Coudln't get data from site"}, status=status.HTTP_204_NO_CONTENT)
        else:
            userobj = Signup.objects.get(id=userid)

            try:
                tokenobj = Tokens.objects.get(user=userobj)
                tokenobj.delete()
                return JsonResponse({"Message": "Logged Out"}, status=status.HTTP_200_OK)

            except Tokens.DoesNotExist:
                return JsonResponse({"Message": "Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Wrong Request method
        return JsonResponse({"Message": "Wrong Request Method"}, status=status.HTTP_400_BAD_REQUEST)


# ACCOUNT DELETION
@api_view(['POST'])
def user_delete(request, userid):
    if request.method == 'POST':
        userobj = Signup.objects.get(id=userid)
        try:
            tokenobj = Tokens.objects.get(user=userobj)
            tokenobj.delete()
            Signup.objects.filter(id=userid).update(status=False, updated_at=timezone.now())
            return HttpResponse('Account Deleted Successfully')

        except Tokens.DoesNotExist:
            return HttpResponse('Account Deletion Failed')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})


# PROFILE UPDATE
@api_view(['PUT','POST', 'GET'])
def user_profile(request):
    if request.method == 'PUT' or request.method == 'POST':
        data = request.data.get('')
        try:
            Signup.objects.filter(id=data.id).update(email=data.email, first_name=data.first_name, last_name=data.last_name, gender=data.gender, mobile_no=data.mobile_no, updated_at=timezone.now())
            return HttpResponse('Account Updated Successfully')
        except:
            return HttpResponse('Account Updating Failed')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})

######################################################################################################################################

#CREATE JOURNALS
@api_view(['POST'])
def create_journals(request):
    if request.method == 'POST':
        data = request.data
        try:
            if data['password']:
                data['password'] = make_password(data['password'], salt=None, hasher='default')
            journal_serialized = JournalsSerializer(data=data)
            if journal_serialized.is_valid():
                journal_serialized.save()
            return HttpResponse('Journals created successfully')
        except:
            return HttpResponse('No Journals created')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})

#ALL JOURNALS
@api_view(['GET'])
def all_journals(request, id):
    if request.method == 'GET':
        try:
            journal = []
            journalobj = Journals.objects.select_related('journal').filter(journal_id=id)
            for i in journalobj:
                journal.append(JournalsSerializer(i).data)

            return Response(data=journal, status=status.HTTP_200_OK)

        except:
            return HttpResponse('No Journals exists')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})


#UPDATE JOURNALS
@api_view(['PUT', 'POST'])
def update_journals(request):
    if request.method == 'POST' or request.method == 'PUT':
        data = request.data
        try:
            Journals.objects.filter(id=data['id']).update(name=data['name'], cover=data['cover'], isset_password=data['isset_password'], password=data['password'])
            return HttpResponse('Journals updated successfully')
        except:
            return HttpResponse('Journals updation failed')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})


# JOURNAL DELETION
@api_view(['POST'])
def journal_delete(request, id):
    if request.method == 'POST':
        try:
            Journals.objects.filter(id=id).delete()
            return HttpResponse('Journal Deleted Successfully')

        except Journals.DoesNotExist:
            return HttpResponse('Journal Deletion Failed')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})


########################################################################################################################################

#CREATE PAGES
@api_view(['POST'])
def create_pages(request):
    if request.method == 'POST':
        data = request.data
        try:
            page_serialized = PagesSerializer(data=data)
            if page_serialized.is_valid():
                page_serialized.save()
            return HttpResponse('Page created successfully')
        except:
            return HttpResponse('No Page exists')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})



#ALL PAGES
@api_view(['GET'])
def all_pages(request, id):
    if request.method == 'GET':
        try:
            page = []
            pageobj = Pages.objects.select_related('page').filter(page_id=id)
            for i in pageobj:
                page.append(PagesSerializer(i).data)
            return Response(data=page, status=status.HTTP_200_OK)
        except:
            return HttpResponse('No Page exists')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})


# UPDATE PAGES
@api_view(['PUT', 'POST'])
def update_pages(request):
    if request.method == 'POST' or request.method == 'PUT':
        data = request.data
        try:
            Pages.objects.filter(id=data['id']).update(title=data['title'], content=data['content'])
            return HttpResponse('Pages updated successfully')
        except:
            return HttpResponse('Pages updation failed')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})


# PAGE DELETION
@api_view(['POST'])
def page_delete(request, id):
    if request.method == 'POST':
        try:
            Pages.objects.filter(id=id).delete()
            return HttpResponse('Page Deleted Successfully')

        except Journals.DoesNotExist:
            return HttpResponse('Page Deletion Failed')
    else:
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})