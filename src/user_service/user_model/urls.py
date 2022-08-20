from django.contrib import admin
from django.urls import path
from user_model.views import UserApiView, UserDetailView

urlpatterns = [
    path("api/user/", UserApiView.as_view()),
    path("api/user/<str:username>/", UserDetailView.as_view()),
]
