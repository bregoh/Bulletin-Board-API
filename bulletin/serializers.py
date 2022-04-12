from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from bulletin.models.board_model import Board
from bulletin.models.thread_model import Thread

from users.models import User


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

    def create(self, validated_data):
        group, created = Group.objects.get_or_create(name="board_admin")
        content_type = ContentType.objects.get(app_label="bulletin", model="board")
        permissions = Permission.objects.filter(content_type=content_type.id)
        user_id = self.context["request"].user.user_id
        user = User.objects.get(user_id=user_id)

        for permission in permissions:
            group.user_set.add(user)
            group.permissions.add(permission)
            user.user_permissions.add(permission)

        board = Board.objects.create(**validated_data)
        return board


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

    def create(self, validated_data):
        group, created = Group.objects.get_or_create(name="thread_admin")
        content_type = ContentType.objects.get(app_label="bulletin", model="thread")
        permissions = Permission.objects.filter(content_type=content_type.id)
        user_id = self.context["request"].user.user_id
        user = User.objects.get(user_id=user_id)

        for permission in permissions:
            group.user_set.add(user)
            group.permissions.add(permission)
            user.user_permissions.add(permission)

        return validated_data
