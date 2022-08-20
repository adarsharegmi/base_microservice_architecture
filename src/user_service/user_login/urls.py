from django.contrib import admin
from django.urls import path
from user_login.views import user_login

urlpatterns = [
    path("api/login/", user_login),
]
