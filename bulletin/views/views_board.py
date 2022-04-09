from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from bulletin.serializers import BoardSerializer
from bulletin.models.board_model import Board
from static.customResponse import CustomResponse
from static.constants import Constant


class ListCreateBoards(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        board = BoardSerializer(data=request.data)
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

    def delete(self, request, *args, **kwargs):
        board_id = kwargs["board_id"]
        board_data = Board.objects.filter(board_id=board_id)

        if board_data.exists():
            board_data.delete()

        response_data = CustomResponse.response(
            message=Constant.BOARD_DELETED, error={}
        )
        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)
