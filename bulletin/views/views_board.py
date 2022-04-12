from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response

from bulletin.models.board_model import Board
from bulletin.serializers import BoardSerializer
from static.constants import Constant
from static.customResponse import CustomResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import Permission

from users.models import User
from django.contrib.auth.models import Group, Permission


class ListCreateBoards(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(groups__name="board_moderator")

        if request.user.is_superuser or user.exists():
            board = BoardSerializer(data=request.data, context={"request": request})
            if board.is_valid():
                board.save()
                response_data = CustomResponse.response(
                    data=board.data, message=Constant.BOARD_CREATED, error={}
                )
                return Response(data=response_data, status=status.HTTP_201_CREATED)

            response_data = CustomResponse.response(
                data={}, message=Constant.BOARD_CREATE_ERROR, error=board.errors
            )
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        board_data = Board.objects.values()
        response_data = CustomResponse.response(
            data=board_data, message=Constant.BOARD_RETRIEVED, error={}
        )
        return Response(data=response_data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyBoards(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        board_id = kwargs["board_id"]
        board = Board.objects.filter(board_id=board_id)

        if not board.exists():
            response_data = CustomResponse.response(message=Constant.BOARD_NOT_FOUND)
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

        thread_data = board.values().first()
        response_data = CustomResponse.response(
            data=thread_data, message=Constant.BOARD_RETRIEVED, error={}
        )
        return Response(data=response_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        if request.user.has_perm("bulletin.change_board"):
            board_id = kwargs["board_id"]
            board_query_set = Board.objects.filter(board_id=board_id).first()
            board_data = BoardSerializer(instance=board_query_set, data=request.data)

            if board_data.is_valid():
                board_data.save()
                response_data = CustomResponse.response(
                    data=board_data.data, message=Constant.BOARD_UPDATED, error={}
                )
                return Response(data=response_data, status=status.HTTP_200_OK)

            response_data = CustomResponse.response(
                data={}, message=Constant.BOARD_NOT_UPDATED, error=board_data.errors
            )
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = CustomResponse.response(message=Constant.UNAUTHORIZED_ACTION)
        return Response(data=response_data, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm("bulletin.delete_board"):
            board_id = kwargs["board_id"]
            board_data = Board.objects.filter(board_id=board_id)

            if board_data.exists():
                board_data.delete()

            response_data = CustomResponse.response(
                message=Constant.BOARD_DELETED, error={}
            )
            return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)

        response_data = CustomResponse.response(message=Constant.UNAUTHORIZED_ACTION)
        return Response(data=response_data, status=status.HTTP_401_UNAUTHORIZED)


"""
View Class to Add New Thread Moderator

"""


class AddBoardModeratorView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        response = kwargs["status"]

        if response == "declined":
            response_data = CustomResponse.response(
                message=Constant.BOARD_MODERATOR_DECLINED
            )
            return Response(data=response_data, status=status.HTTP_304_NOT_MODIFIED)

        group, created = Group.objects.get_or_create(name="board_moderator")
        permissions = Permission.objects.get(
            name__in=["Can add board", "Can change board"]
        )
        user_id = request.user.user_id
        user = User.objects.get(user_id=user_id)

        for permission in permissions:
            group.user_set.add(user)
            group.permissions.add(permission)
            user.user_permissions.add(permission)

        response_data = CustomResponse.response(message=Constant.BOARD_MODERATOR_ADDED)
        return Response(data=response_data, status=status.HTTP_200_OK)
