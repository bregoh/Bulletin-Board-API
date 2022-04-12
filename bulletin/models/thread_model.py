import uuid

from django.db import models
from django.utils import timezone

from bulletin.models.board_model import Board
from users.models import User


class Thread(models.Model):
    thread_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    board = models.ForeignKey(Board, related_name="thread", on_delete=models.DO_NOTHING)
    thread_title = models.CharField(max_length=255)
    thread_contents = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = "thread"
        ordering = ["thread_title"]
