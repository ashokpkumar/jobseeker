from django.urls import path

from . import views
from django.contrib import admin


urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("login/create-user", views.create_user, name="create_user"),
    path("login/login", views.login, name="login"),
    path("login/fill-newuser/<userid>", views.fill_newuser, name="fill_newuser"),
    path("login/approve-user/<userid>", views.approve_user, name="approve_user"),
    path("lookup/", views.lookup, name="lookup"),
    path("create_mongo_user/",views.create_mongo_user, name="create_user"),

    path("converter/<from_cur>/<to_cur>", views.converter, name="converter"),
    path("fetch-users", views.fetch_users, name="fetch_users")
    # path("lookup/", views.lookup, name="lookup"),
    # path("lookup/", views.lookup, name="lookup")


]