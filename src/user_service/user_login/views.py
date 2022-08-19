from http.client import HTTPResponse
import json
from django.shortcuts import render
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from user_model.models import User

# the function for validating the user
def user_validation(uname, password):
    user_data = User.objects.filter(email=uname, password=password)
    return True if user_data else False


# this function for getting username and password
@csrf_exempt
def user_login(request):
    uname = request.POST.get("username")
    password = request.POST.get("password")
    resp = {}

    if uname and password:
        respdata = user_validation(uname, password)
        if respdata:
            resp["status"] = "Success"
            resp["status_code"] = "200"
            resp["message"] = "User login successfully"
        else:
            resp["status"] = "Failed"
            resp["status_code"] = "400"
            resp["message"] = "Invalid credentials"
    else:
        resp["status"] = "Failed"
        resp["status_code"] = "400"
        resp["message"] = "all fields are mandatory"
    return HTTPResponse(json.dumpps(resp), content_type="application/json")
