from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import LoginSerializer, UserSerializer

from static.constants import Constant
from static.customResponse import CustomResponse


class RegisterUser(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = CustomResponse.response(
                data=serializer.data, message=Constant.USER_CREATED
            )
            return Response(data=response, status=status.HTTP_201_CREATED)

        response = CustomResponse.response(
            message=Constant.USER_NOT_CREATED, error=serializer.errors
        )
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            response = CustomResponse.response(
                data=serializer.data, message=Constant.USER_LOGGED_IN
            )
            return Response(data=response, status=status.HTTP_201_CREATED)

        response = CustomResponse.response(
            message=Constant.INVALID_AUTH_CREDENTIALS,
            error=serializer.errors,
        )
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
