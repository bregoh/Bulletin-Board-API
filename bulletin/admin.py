from django.contrib import admin

from bulletin.models.board_model import Board
from bulletin.models.thread_model import Thread


admin.site.register(Board)
admin.site.register(Thread)
