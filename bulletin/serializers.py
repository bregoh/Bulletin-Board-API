from rest_framework.serializers import ModelSerializer
from bulletin.models.thread_model import Thread
from bulletin.models.board_model import Board


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class ThreadSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"
