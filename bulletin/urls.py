from django.contrib import admin
from django.urls import path
from bulletin.views.views_board import ListCreateBoards, RetrieveUpdateDestroyBoards
from bulletin.views.views_thread import ListCreateThreads, RetrieveUpdateDestroyThreads

urlpatterns = [
    path("board", ListCreateBoards.as_view(), name="lc-board"),
    path(
        "board/<uuid:board_id>", RetrieveUpdateDestroyBoards.as_view(), name="rud-board"
    ),
    path("thread", ListCreateThreads.as_view(), name="lc-thread"),
    path(
        "thread/<uuid:thread_id>",
        RetrieveUpdateDestroyThreads.as_view(),
        name="rud-thread",
    ),
]
