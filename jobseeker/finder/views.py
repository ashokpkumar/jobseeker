#Standard Library import
from datetime import datetime, timedelta
import uuid
import logging

#3P import
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view

#modules
from utils.jwt import check_hash_password, hash_password, jwt_encode
from utils.lookup import get_lookup_value
from utils.rbm import CreateUserForm
from utils.validators import adminrequired, check_valid_user, loginrequired, validate_body
from .models import LookupTable, User_table


logger = logging.getLogger("finder")

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
    logger.info("Lookup Created Successfully")    
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