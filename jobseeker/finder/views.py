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
        print("before request")
        bearer_token = request.headers.get("authorization")
        required_token = bearer_token.split(" ")
        only_token = required_token[1]
        return_payload = jwt_decode(only_token) # in dict format
        i_exp = return_payload["exp_at"] # date time is in string format
        user_email = return_payload["user_email"]
        i_exp = i_exp.split(".")[0]  # truncates the decimal part in "seconds"
        i_exp = datetime.strptime(i_exp, "%Y-%m-%d %H:%M:%S") # converted to original date time format
        
        if i_exp < datetime.now():
            return HttpResponse("Time has expired.")

        user_obj = User_table.objects.filter(email = user_email).first()
        if not user_obj:
            return HttpResponse("User doesn't exist.")
        request.user_id = user_obj.user_id
        request.first_name = user_obj.first_name
        request.last_name = user_obj.last_name
        request.email = user_obj.email
        request.phone = user_obj.phone
        request.user_type = get_lookup_key("user_type", user_obj.user_type)
        response = func(request, *args, **kwargs)
        print("after request")
        return response
    return inner1

def check_valid_user(func):
    @wraps(func)
    def inner2(request, *args, **kwargs):
        
        user_obj = User_table.objects.filter(user_id = kwargs.get("userid")).first()
        if user_obj is None:
            return HttpResponse("User not available")
        
        if request.user_id != kwargs.get("userid"):   
            return HttpResponse("User not authorized to perform this action.")
        response = func(request, *args, **kwargs)
        return response
    
    return inner2


def adminrequired(func):
    @wraps(func)
    def inner3(request, *args, **kwargs):
        print("before request")
        if request.user_type != "hr_admin":
            return HttpResponse("Admin rights required")
        response = func(request, *args, **kwargs)
        print("after request")
        return response
    return inner3


class CreateUserForm(forms.Form):  # creation of signup table format for the databse
    email = forms.EmailField()
    phone = forms.CharField()
    password = forms.CharField()


@api_view(['POST'])  
def create_user(request):    # this creates a new user with only limited data while signup

    form = CreateUserForm(request.data)

    if not form.is_valid():     # checks the field validations with is_valid() function in the django forms
        return HttpResponse("Invalid Data")

    email = request.data.get("email")
    phone = request.data.get("phone")
    password = request.data.get("password")

    if email is None or phone is None or password is None:
        return HttpResponse("Email or Phone or Password is none.")

    user_obj = User_table() # creation of object form the User_table to access attribute(column) values from that table in database
    user_obj.user_id = uuid.uuid4()  # creates a autometic unique user id
    user_obj.email = email
    user_obj.phone = phone
    user_obj.password_hash = pbkdf2_sha256.hash(password)  # converts regular password into hash with sha256 algorithm

    user_obj.save()
    return HttpResponse("New user created")

@api_view(['POST'])
@loginrequired
@check_valid_user
def fill_newuser(request, userid):  # this function fills the user details with are not given while signup
    
    user_obj = User_table.objects.filter(user_id = userid).first() # gets the user object details based on user id
    if user_obj is None:    # in the above statement userid is directly copied from the table to compare in the api req
        return HttpResponse(f"{userid} not available.")
    else:
       
        user_obj.first_name = request.data.get("firstname")  # gets the user data from api request body in json format
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
@loginrequired
def lookup(request):   # this function enters data in the lookup table with master key, key, value as attributes
    user_obj = LookupTable() # lookup table in the database
    
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
                
@api_view(['PATCH'])
@loginrequired
@adminrequired
def approve_user(request, userid):
    user_obj = User_table.objects.filter(user_id=userid).first()
    user_obj.hidden = False

    user_obj.save()
    return HttpResponse("User approved")



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

    return jwt.decode(token, "secretkey", algorithms=["HS256"])


