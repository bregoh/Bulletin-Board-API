from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response

from bulletin.models.thread_model import Thread
from bulletin.serializers import ThreadSerializer
from static.constants import Constant
from static.customResponse import CustomResponse

from users.models import User
from django.contrib.auth.models import Group, Permission


class ListCreateThreads(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        thread = ThreadSerializer(data=request.data, context={"request": request})
        if thread.is_valid():
            thread.save()
            response_data = CustomResponse.response(
                data=thread.data, message=Constant.THREAD_CREATED, error={}
            )
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = CustomResponse.response(
            data={}, message=Constant.THREAD_CREATE_ERROR, error=thread.errors
        )
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        thread_data = Thread.objects.values()
        response_data = CustomResponse.response(
            data=thread_data, message=Constant.THREAD_FETCHED, error={}
        )
        return Response(data=response_data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyThreads(RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        thread_id = kwargs["thread_id"]
        thread = Thread.objects.filter(thread_id=thread_id)

        if not thread.exists():
            response_data = CustomResponse.response(message=Constant.THREAD_NOT_FOUND)
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

        thread_data = thread.values().first()
        response_data = CustomResponse.response(
            data=thread_data, message=Constant.THREAD_RETRIEVED, error={}
        )
        return Response(data=response_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        thread_id = kwargs["thread_id"]
        thread_query_set = Thread.objects.filter(thread_id=thread_id).first()
        thread_data = ThreadSerializer(instance=thread_query_set, data=request.data)

        if thread_data.is_valid():
            thread_data.save()
            response_data = CustomResponse.response(
                data=thread_data.data, message=Constant.THREAD_UPDATED, error={}
            )
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = CustomResponse.response(
            data={}, message=Constant.THREAD_NOT_UPDATED, error=thread_data.errors
        )
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        thread_id = kwargs["thread_id"]
        thread_data = Thread.objects.filter(thread_id=thread_id)

        if thread_data.exists():
            thread_data.delete()

        response_data = CustomResponse.response(
            message=Constant.THREAD_DELETED, error={}
        )
        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)


"""
View Class to Add New Thread Moderator

"""


class AddThreadModeratorView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        response = kwargs["status"]

        if response == "declined":
            response_data = CustomResponse.response(
                message=Constant.THREAD_MODERATOR_DECLINED
            )
            return Response(data=response_data, status=status.HTTP_304_NOT_MODIFIED)

        group, created = Group.objects.get_or_create(name="thread_moderator")
        permissions = Permission.objects.get(
            name__in=["Can add thread", "Can change thread"]
        )
        user_id = request.user.user_id
        user = User.objects.get(user_id=user_id)

        for permission in permissions:
            group.user_set.add(user)
            group.permissions.add(permission)
            user.user_permissions.add(permission)

        response_data = CustomResponse.response(message=Constant.THREAD_MODERATOR_ADDED)
        return Response(data=response_data, status=status.HTTP_200_OK)
