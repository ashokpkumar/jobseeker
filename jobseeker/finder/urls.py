from django.urls import path

from . import views

urlpatterns = [
    # path("example", views.index, name="index"),
    # path("adduser", views.insert_user, name="insert_user"),
    # path("new-user/<username>", views.new_user, name="new_user")
    path("login/login", views.login, name="login"),
    path("login/create-user", views.create_user, name="create_user"),
    path("login/fill-newuser/<userid>", views.fill_newuser, name="fill_newuser"),
    path("lookup/", views.lookup, name="lookup"),
    # path("login/get-gender/<genderdata>", views.get_gender, name="get_gender")
]