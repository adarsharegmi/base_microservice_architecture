import json
from django.shortcuts import render
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_model.models import User

# fuction for fetching the user data
def user_data(uname):
    user_data = User.objects.filter(email_id=uname)
    for data in user_data.values():
        return data


# function for gettign username and password
@csrf_exempt
def user_info(request):
    if request.method == "POST":
        if "application/json" in request.META["CONTENT_TYPE"]:
            val1 = json.loads(request.body)
            uname = val1.get("username")
            resp = {}

            if uname:
                respdata = user_data(uname)
                dict1 = {}
                if respdata:
                    dict1["First Name"] = respdata.get("first_name", "")
                    dict1["Last Name"] = respdata.get("last_name", "")
                    dict1["Mobile Number"] = respdata.get("mobile_number", "")
                    dict1["Email Id"] = respdata.get("email_id", "")
                    dict1["Address"] = respdata.get("address", "")

                    if dict1:
                        resp["status"] = "Success"
                        resp["status_code"] = "200"
                        resp["data"] = dict1
                    else:
                        resp["status"] = "Failed"
                        resp["status_code"] = "400"
                        resp["message"] = "user not found"
            else:
                resp["status"] = "Failed"
                resp["status_code"] = "400"
                resp["message"] = "Fields is mandatory."
        else:
            resp["status"] = "Failed"
            resp["status_code"] = "400"
            resp["message"] = "Request type is not matched."
    else:
        resp["status"] = "Failed"
        resp["status_code"] = "400"
        resp["message"] = "Request type is not matched."
    return HttpResponse(json.dumps(resp), content_type="application/json")
