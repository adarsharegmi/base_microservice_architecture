"""user_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user_model import urls as user_model_urls
from user_login import urls as user_login_urls
from kanban_board import urls as kanban_board_urls
from kanban_user import urls as kanban_user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("user_model/", include(user_model_urls)),
    path("user_login/", include(user_login_urls)),
    path("kanban_board/", include(kanban_board_urls)),
    path("kanban_user/", include(kanban_user_urls)),
]
