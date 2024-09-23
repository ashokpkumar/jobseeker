from django.http import HttpResponse
from .models import User_table
from datetime import datetime
from rest_framework.decorators import api_view


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['POST'])
def insert_user(request):
    user_obj = User_table()

    user_obj.user_id = 1234
    user_obj.first_name = "nikhith"
    user_obj.last_name = "raj"
    user_obj.gender = 1
    user_obj.nationality = "india"
    user_obj.email = "nikhithtest@gmail.com"
    user_obj.phone = "123456789"
    user_obj.country_code = "91"
    user_obj.user_type = 1
    user_obj.created_by = 33
    user_obj.created_time = datetime.now()
    user_obj.modified_by = 32
    user_obj.modified_time = datetime.now()
    user_obj.hidden = False
    
    user_obj.save()

    return HttpResponse("Created a new user.")

@api_view(['POST'])
def new_user(request, username):
    user_obj = User_table()

    user_obj.user_id = 1234
    user_obj.first_name = request.query_params.get("firstname")
    user_obj.last_name = request.query_params.get("lastname")
    user_obj.gender = request.query_params.get("gender")
    user_obj.nationality = request.query_params.get("nationality")
    user_obj.email = request.query_params.get("email")
    user_obj.phone = request.query_params.get("phone")
    user_obj.country_code = request.query_params.get("country_code")
    user_obj.user_type = request.query_params.get("user_type")
    user_obj.created_by = request.query_params.get("created_by")
    user_obj.created_time = datetime.now()
    user_obj.modified_by = request.query_params.get("modified_by")
    user_obj.modified_time = datetime.now()
    user_obj.hidden = True
    
    user_obj.save()

    return HttpResponse("new user created.")