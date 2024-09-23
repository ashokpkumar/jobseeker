from django.urls import path

from . import views

urlpatterns = [
    path("example", views.index, name="index"),
    path("adduser", views.insert_user, name="insert_user"),
    path("new-user/<username>", views.new_user, name="new_user")
]