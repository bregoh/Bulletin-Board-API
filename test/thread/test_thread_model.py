import pytest
from bulletin.models.board_model import Board
from bulletin.models.thread_model import Thread

BOARD_DATA = {"board_name": "board54"}
THREAD_DATA = {
    "thread_title": "This is good deal",
    "thread_contents": "Yes Yes, the best in town.",
}


@pytest.mark.django_db
def test_thread_model():
    board = Board.objects.create(**BOARD_DATA)
    thread = Thread(board=board, **THREAD_DATA)
    thread.save()

    assert thread.thread_title == THREAD_DATA["thread_title"]
    assert thread.thread_contents == THREAD_DATA["thread_contents"]
    assert thread.thread_id
    assert thread.board
    assert thread.created
    assert thread.updated
