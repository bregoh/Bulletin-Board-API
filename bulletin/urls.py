from django.urls import path

from bulletin.views.views_board import (
    ListCreateBoards,
    RetrieveUpdateDestroyBoards,
    AddBoardModeratorView,
)
from bulletin.views.views_thread import (
    ListCreateThreads,
    RetrieveUpdateDestroyThreads,
    AddThreadModeratorView,
)

urlpatterns = [
    path("board", ListCreateBoards.as_view(), name="lc-board"),
    path(
        "board/moderate/<str:status>", AddBoardModeratorView.as_view(), name="rud-board"
    ),
    path(
        "board/<uuid:board_id>", RetrieveUpdateDestroyBoards.as_view(), name="rud-board"
    ),
    path("thread", ListCreateThreads.as_view(), name="lc-thread"),
    path(
        "thread/moderate/<str:status>",
        AddThreadModeratorView.as_view(),
        name="lc-thread",
    ),
    path(
        "thread/<uuid:thread_id>",
        RetrieveUpdateDestroyThreads.as_view(),
        name="rud-thread",
    ),
]
