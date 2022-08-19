import json
from django.shortcuts import render
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user_service.user_model.models import User

## functiont to insert the data into the table


def data_insert(fname, lname, mobile_number, email_id, password, address):
    user_data = User(
        first_name=fname,
        last_name=lname,
        address=address,
        email_id=email_id,
        password=password,
        mobile_number=mobile_number,
    )
    user_data.save()
    return True


### this function will get the data from the front end side
@csrf_exempt
def registration_req(request):
    """gets the data from the front end side"""
    fname = request.POST.get("first_name")
    lname = request.POST.get("last_name")
    address = request.POST.get("address")
    email_id = request.POST.get("email_id")
    mobile_number = request.POST.get("mobile_number")
    password = request.POST.get("password")
    cnf_password = request.POST.get("confirm_password")
    resp = {}

    # validation for the data fields
    if (
        fname
        and lname
        and email_id
        and mobile_number
        and password
        and cnf_password
        and address
    ):

        # check valid mobile number
        if len(mobile_number) == 10:
            # check for password and cnf password
            if password == cnf_password:
                respdata = data_insert(
                    fname=fname,
                    lname=lname,
                    mobile_number=mobile_number,
                    address=address,
                    email_id=email_id,
                    password=password,
                )

                if respdata:
                    resp["status"] = "Success"
                    resp["status_code"] = "200"
                    resp["message"] = "User is created successfully"

                # for else condition
                else:
                    resp["status"] = "Failed"
                    resp["status_code"] = "400"
                    resp["message"] = "Unable to register user, please try again"
            else:
                # for mismatching password
                resp["status"] = "Failed"
                resp["status_code"] = "400"
                resp["message"] = "password and confirm password mismatched"
        else:
            resp["status"] = "Failed"
            resp["status_code"] = "400"
            resp["message"] = "Invalid phone number"
    else:
        resp["status"] = "Failed"
        resp["status_code"] = "400"
        resp["message"] = "Field value is missing"

    return HttpResponse(json.dumps(resp), content_type="application/json")
