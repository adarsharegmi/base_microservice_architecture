from __future__ import unicode_literals
from functools import partial
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user_model.models import User

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from user_model.serializers import UserSerializer
from user_login.decorator import authorize


class UserApiView(APIView):
    # list all user
    def get(self, request, *args, **kwargs):
        """
        list all user
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        register user if the statements are true
        """
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "address": request.data.get("address"),
            "email_id": request.data.get("email_id"),
            "mobile_number": request.data.get("mobile_number"),
            "password": request.data.get("password"),
            "confirm_password": request.data.get("confirm_password"),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, username, *args, **kwargs):
        """
        list specific user by username username is the email address
        """
        try:
            user = User.objects.get(email_id=username)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"res": "no user with the username exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @authorize()
    def put(self, request, username, *args, **kwargs):
        """
        update the user info
        """
        user_instance = User.objects.get(email_id=username)
        if not user_instance:
            return Response({"res": "no relevant user found"}, status=status)
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "address": request.data.get("address"),
            "email_id": request.data.get("email_id"),
            "mobile_number": request.data.get("mobile_number"),
            "password": request.data.get("password"),
            "confirm_password": request.data.get("confirm_password"),
        }
        serializer = UserSerializer(instance=user_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, *args, **kwargs):
        """
        deletes the user
        """
        user_instance = User.objects.get(email_id=username)
        if not user_instance:
            return Response(
                {"res": "object with username doesnot exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_instance.delete()
        return Response({"res": "user is deleted"}, status=status.HTTP_200_OK)
