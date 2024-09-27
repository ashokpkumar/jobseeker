from django.http import HttpResponse, HttpResponseNotFound
from .models import LookupTable, User_table
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
import uuid
from django import forms
import jwt
from passlib.hash import pbkdf2_sha256
from functools import wraps


def loginrequired(func):
    @wraps(func)
    def inner1(request, *args, **kwargs):
        func(request, *args, **kwargs)
    return inner1


class CreateUserForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField()
    password = forms.CharField()


@api_view(['POST'])
def create_user(request):

    form = CreateUserForm(request.data)

    if not form.is_valid():
        return HttpResponse("Invalid Data")

    email = request.data.get("email")
    phone = request.data.get("phone")
    password = request.data.get("password")

    if email is None or phone is None or password is None:
        return HttpResponse("Email or Phone or Password is none.")

    user_obj = User_table()
    user_obj.user_id = uuid.uuid4()
    user_obj.email = email
    user_obj.phone = phone
    user_obj.password_hash = pbkdf2_sha256.hash(password)

    user_obj.save()
    return HttpResponse("New user created")

@api_view(['POST'])
def fill_newuser(request, userid):
    
    user_obj = User_table.objects.filter(user_id = userid).first()
    if user_obj is None:
        return HttpResponse(f"{userid} not available.")
    else:
       
        user_obj.first_name = request.data.get("firstname")
        user_obj.last_name = request.data.get("lastname")
        user_obj.gender = get_lookup_value("gender", request.data.get("gender"))
        user_obj.nationality = request.data.get("nationality")
       
        user_obj.country_code = request.data.get("country_code")
        user_obj.user_type = get_lookup_value("user_type", request.data.get("user_type"))
        user_obj.created_by = request.data.get("created_by")
        
        user_obj.modified_by = request.data.get("modified_by")
        user_obj.modified_time = datetime.now()
        user_obj.hidden = True

        user_obj.save()
    return HttpResponse("User details added successfully.")

    
@api_view(['POST'])
# @loginrequired
def lookup(request):
    user_obj = LookupTable()
    
    user_obj.id = uuid.uuid4()
    user_obj.master_key = request.data.get("master_key")
    user_obj.key = request.data.get("key")
    user_obj.value = request.data.get("value")

    user_obj.save()        
    return HttpResponse("Entry done in lookup table")


@api_view(['POST'])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    try:
        if int(username):
            user_obj = User_table.objects.filter(phone=username).first()
            if user_obj is None:
                return HttpResponseNotFound("Invalid User")
            elif pbkdf2_sha256.verify(password, user_obj.password_hash) == False: 
                return HttpResponseNotFound("Invalid Password")
            else:
                payload = {
                    "user_id" : user_obj.user_id,
                    "first_name" : user_obj.first_name,
                    "last_name" : user_obj.last_name,
                    "user_email" : user_obj.email,
                    "phone" : user_obj.phone,
                    "i_at" : str(datetime.now()),
                    "exp_at": str(datetime.now() + timedelta(minutes=15))
                }
                return HttpResponse(jwt_encode(payload))
    
    except:
        user_obj = User_table.objects.filter(email=username, password_hash=hash(password)).first()
        if user_obj is None:
            return HttpResponse("Invalid User")
        else:
            payload = {
                "user_id" : user_obj.user_id,
                "first_name" : user_obj.first_name,
                "last_name" : user_obj.last_name,
                "user_email" : user_obj.email,
                "phone" : user_obj.phone,
                "i_at" : str(datetime.datetime.now()),
                "exp_at": str(datetime.datetime.now() + datetime.timedelta(minutes=15))
            }
            return HttpResponse(jwt_encode(payload))
                


def get_lookup_value(master_key, key):
    lookup_obj = LookupTable.objects.filter(master_key=master_key, key=key).first()
    if lookup_obj is not None:
        return lookup_obj.value
    return None

def get_lookup_key(master_key, value):
    lookup_obj = LookupTable.objects.filter(master_key=master_key, value=value).first()
    if lookup_obj is not None:
        return lookup_obj.key
    return None

def jwt_encode(payload):

    return jwt.encode(payload, "secretkey", algorithm="HS256")


def jwt_decode(token):

    return jwt.decode(token, "secretkey", algorithm="HS256")
