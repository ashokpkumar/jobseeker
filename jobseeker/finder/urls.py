from django.urls import path, include
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
    path("create_session",views.create_session, name="create_session"),
    path("retrive_session",views.retrive_session, name="retrive_session"),
    

    path("converter/<from_cur>/<to_cur>", views.converter, name="converter"),
    path("fetch-users", views.fetch_users, name="fetch_users"),
    

    path("create_mongo_user_orm/",views.create_mongo_user_orm, name="create_mongo_user_orm"),
    path("get_mongo_user_orm/",views.get_mongo_user_orm, name="get_mongo_user_orm"),
    path("fetch_mongo_user_orm",views.fetch_mongo_user_orm, name="fetch_mongo_user_orm"),

    path("live", views.live, name="live"),
    path("ready", views.ready, name="ready"),
    
    path("upload", views.upload, name="upload"),

    path('finder/account/', include('allauth.urls'))

    
    # path("lookup/", views.lookup, name="lookup"),
    # path("lookup/", views.lookup, name="lookup")


]