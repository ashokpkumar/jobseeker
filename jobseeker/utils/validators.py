

from functools import wraps
from datetime import datetime
from django.http import HttpResponse
from finder.models import User_table
from utils.lookup import get_lookup_key
from utils.jwt import jwt_decode
from utils.rbm import rbm_map


def loginrequired(func):
    @wraps(func)
    def inner1(request, *args, **kwargs):
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
        if request.user_type != "hr_admin":
            return HttpResponse("Admin rights required")
        response = func(request, *args, **kwargs)
        return response
    return inner3

def validate_body(func):
    @wraps(func)
    def inner4(request, *args, **kwargs):
        print("before request")
        validator_class = rbm_map[request.__name__]
        form = validator_class(request.data)
        if not form.is_valid():     
            return HttpResponse("Invalid Data")
        response = func(request, *args, **kwargs)
        print("after request")
        return response
    return inner4
