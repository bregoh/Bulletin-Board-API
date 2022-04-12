import pytest

from bulletin.models.board_model import Board
from bulletin.serializers import ThreadSerializer

BOARD_DATA = {"board_name": "board54"}
DATA = {
    "thread_title": "This is good deal",
    "thread_contents": "Yes Yes, the best in town.",
}


def create_board():
    board = Board(**BOARD_DATA)
    board.save()
    return board


@pytest.mark.django_db
def test_thread_serializer_valid_data():
    board = create_board()
    serializer = ThreadSerializer(data={**DATA, "board": str(board.board_id)})

    assert serializer.is_valid()
    assert len(serializer.errors) == 0


@pytest.mark.django_db
def test_thread_serializer_invalid_data():
    serializer = ThreadSerializer(data=DATA)

    assert serializer.is_valid() is False
    assert len(serializer.errors) > 0
