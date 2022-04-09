import uuid
from django.db import models
from django.utils import timezone


class Board(models.Model):
    board_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    board_name = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = "board"
        ordering = ["board_name"]
