from django.http import HttpResponse
from .models import User_table
from datetime import datetime
from rest_framework.decorators import api_view


@api_view(['POST'])
def login(request): 

    username = request.data.get("username")
    given_password = request.data.get("password")

    try:
        username = int(username)
    
        user_obj = User_table.objects.filter(phone = username).first()
        if user_obj is None:
            return HttpResponse(f"{username} not available.")
        if user_obj.password_hash == given_password:
            return HttpResponse(f"{username} is valid.")
        else:
            return HttpResponse("Invalid Password.")
    
    except:
        
        if username.find(".") > -1 and username.find("@") > -1:
            user_obj = User_table.objects.filter(email = username).first()
            if user_obj is None:
                return HttpResponse(f"{username} not available.")
            if user_obj.password_hash == given_password:
                return HttpResponse(f"{username} is valid.")
            else:
                return HttpResponse("Invalid Password.")
        else:
            return HttpResponse("Invalid Username")


    # if "@" and "." in given_username:
    #     if given_username in User_table.email:
    #         password_hash = hash(given_password)
    #         if password_hash in User_table.password_hash:
    #             return_message = f"Success. User {user_obj.first_name} {user_obj.last_name} is available."
    #         else:
    #             return_message = "Wrong password."
    #     else:
    #         return_message = "User not available."
    # return return_message




    user_obj.save()
    return 