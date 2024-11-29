import pytest
from ..models import User_table


@pytest.fixture
def create_user(db):
    user_list = [
        {
            "user_id":"1111",
            "first_name":"nikhith1",
            "last_name":"raj1",
            "email":"nikhithraj1@gmail.com",
            "password":"1111111111",
            "phone":"1111111111"

        },
         {
            "user_id":"2222",
            "first_name":"nikhith2",
            "last_name":"raj2",
            "email":"nikhithraj2@gmail.com",
            "password":"2222222222",
            "phone":"2222222222"

        },
         {
            "user_id":"3333",
            "first_name":"nikhith3",
            "last_name":"raj3",
            "email":"nikhithraj3@gmail.com",
            "password":"3333333333",
            "phone":"3333333333"

        }
    ]
    user = []
    for usr in user_list:
        user.append(User_table(
            user_id=usr.get("user_id"),
            first_name=usr.get("first_name"),
            last_name=usr.get("last_name"),
            email=usr.get("email"),
            password=usr.get("password"),
            phone=usr.get("phone")
        )
        )
    return user
