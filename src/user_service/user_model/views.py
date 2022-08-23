from __future__ import unicode_literals
from user_model.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
