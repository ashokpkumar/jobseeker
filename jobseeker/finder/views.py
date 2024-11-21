#Standard Library import
from datetime import datetime, timedelta
import uuid
import logging
import requests
import json

#3P import
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view
from pymongo import MongoClient

from django.core.files.storage import default_storage
from django.http import JsonResponse

#modules
from utils.jwt import check_hash_password, hash_password, jwt_encode
from utils.lookup import get_lookup_value, get_lookup_key
from utils.rbm import CreateUserForm
from utils.validators import adminrequired, check_valid_user, loginrequired, validate_body
from .models import LookupTable, User_table, MongoUser, Document
from utils.mongo_utils import connect_mongodb


client = MongoClient("mongodb+srv://nikhithtest:test_1234@nikimongo.913qf.mongodb.net/")
db = client.sample_mflix

logger = logging.getLogger(__name__)

@api_view(['GET'])
def converter(request, from_cur, to_cur):
    response = requests.get(f"https://open.er-api.com/v6/latest/{from_cur}")
    if response.ok == True:
        response_txt = response.text
        response_json = json.loads(response_txt) # converts sting to dict
        rates = response_json.get("rates")
        to_curency_value = rates.get(to_cur)
        return HttpResponse(to_curency_value)
    else:
        return HttpResponse("Error while calling yfinance api.")

@api_view(['POST'])  
@validate_body
def create_user(request):    # this creates a new user with only limited data while signup
    email = request.data.get("email")
    phone = request.data.get("phone")
    password = request.data.get("password")

    user_obj = User_table() # creation of object form the User_table to access attribute(column) values from that table in database
    user_obj.user_id = uuid.uuid4()  # creates a autometic unique user id
    user_obj.email = email
    user_obj.phone = phone
    user_obj.password_hash = hash_password(password)  # converts regular password into hash with sha256 algorithm
    user_obj.save()

    return HttpResponse("New user created")


@api_view(['POST'])
@loginrequired
@validate_body
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
        user_obj.created_by = request.user_id
        user_obj.modified_by = request.user_id
        user_obj.modified_time = datetime.now()
        user_obj.hidden = True
        user_obj.save()
    return HttpResponse("User details added successfully.")

    
@api_view(['POST'])
@loginrequired
@validate_body
def lookup(request):   # this function enters data in the lookup table with master key, key, value as attributes
    user_obj = LookupTable() # lookup table in the database
    user_obj.id = uuid.uuid4()
    user_obj.master_key = request.data.get("master_key")
    user_obj.key = request.data.get("key")
    user_obj.value = request.data.get("value")
    user_obj.save()    
    logger.info("Lookup Created Successfully")    
    return HttpResponse("Entry done in lookup table")


@api_view(['POST'])
@validate_body
def login(request):
    """
    returns jwt code after successful login
    """
    username = request.data.get("username")
    password = request.data.get("password")
    try:
        if int(username):
            user_obj = User_table.objects.filter(phone=username).first()
            if user_obj is None:
                return HttpResponseNotFound("Invalid User")
            elif check_hash_password(password,user_obj.password_hash) == False:
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
                print(HttpResponse(jwt_encode(payload)))
                return JsonResponse({"token":jwt_encode(payload)}) 
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

@api_view(['GET'])
def fetch_users(request):
    user_list = []
    country_code = request.GET.get("country_code")
    user_type = request.GET.get("user_type")
    # user_obj = User_table.objects.filter(country_code=country_code, user_type=user_type, hidden=False).all()
    user_obj = User_table.objects
    if country_code is not None:
        user_obj = user_obj.filter(country_code=country_code)
    if user_type is not None:
        user_obj = user_obj.filter(user_type = get_lookup_value("user_type", user_type))
    user_obj = user_obj.filter(hidden=False).all()

    for user in user_obj:
        user_full_name = user.first_name +" "+ user.last_name
        gender = user.gender
        nationality = user.nationality
        email = user.email
        phone = user.phone
        user_info = {
            "user_full_name" : user_full_name,
            "gender" : gender,
            "nationality" : nationality,
            "email" : email,
            "phone" : phone 
        }
        user_list.append(user_info)
    return HttpResponse(user_list)
             
@api_view(['PATCH'])
@loginrequired
@adminrequired
def approve_user(request, userid):
    user_obj = User_table.objects.filter(user_id=userid).first()
    user_obj.hidden = False
    user_obj.save()
    return HttpResponse("User approved")

@api_view(['POST'])
def create_mongo_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    result = db.movies.insert_one({"name": username,"password":password})
    return HttpResponse("Mongo DB user created")

@api_view(['POST'])
def create_mongo_user_orm(request):
    # username = request.data.get("username")
    # password = request.data.get("password")
    connect_mongodb()
    obj = MongoUser()
    obj.hidden = request.data.get("hidden")
    obj.data = request.data.get("data")
    obj.email = request.data.get("email")
    obj.number = request.data.get("number")
    obj.name = request.data.get("name")
    obj.save()
   # result = db.movies.insert_one({"name": username,"password":password})
    return HttpResponse("Mongo DB user created")


@api_view(['GET'])
def get_mongo_user_orm(request):
    connect_mongodb()
    obj = MongoUser.objects.filter(hidden=True).all()
    obj_dict = []
    for item in obj:
        item_info = {
            "hidden" : item.hidden,
            "data" : item.data,
            "email" : item.email,
            "number" : item.number,
            "name" : item.name
        }
        obj_dict.append(item_info)
    return HttpResponse(obj_dict)

@api_view(['GET'])
def fetch_mongo_user_orm(request):
    connect_mongodb()
    hidden = request.GET.get("hidden")
    data = request.GET.get("data")
    email = request.GET.get("email")
    number = request.GET.get("number")
    name = request.GET.get("name")
    obj = MongoUser.objects
    if hidden is not None:
        obj = obj.filter(hidden=hidden)
    if data is not None:
        obj = obj.filter(data=int(data))
    if email is not None:
        obj = obj.filter(email=email)
    if number is not None:
        obj = obj.filter(number=number)
    if name is not None:
        obj = obj.filter(name=name)
    rest = obj.all()

    obj_dict = []
    for item in rest:
        item_info = {
            "hidden" : item.hidden,
            "data" : item.data,
            "email" : item.email,
            "number" : item.number,
            "name" : item.name
        }
        obj_dict.append(item_info)
    return HttpResponse(obj_dict)

@api_view(['GET'])
def live(request):
    print(datetime.now())
    return HttpResponse(True)


@api_view(['GET'])
def ready(request):
    print(datetime.now())
    return HttpResponse(True)

@api_view(['POST'])
def upload(request):
    file = request.FILES['uploaded_file']
    file_name = default_storage.save(file.name, file)
    print(file_name)
    title = request.data.get("title")
    uploaded_file = request.FILES.get("uploaded_file")
    document = Document(title=title, uploaded_file=uploaded_file)
    document.save()
    return HttpResponse("File uploaded successfully")