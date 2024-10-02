from django.urls import path

from . import views

urlpatterns = [
    
    path("login/create-user", views.create_user, name="create_user"),
    path("login/login", views.login, name="login"),
    path("login/fill-newuser/<userid>", views.fill_newuser, name="fill_newuser"),
    path("login/approve-user/<userid>", views.approve_user, name="approve_user"),
    path("lookup/", views.lookup, name="lookup"),
    # path("lookup/", views.lookup, name="lookup"),
    # path("lookup/", views.lookup, name="lookup")


]