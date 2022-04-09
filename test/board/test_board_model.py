import pytest
from bulletin.models.board_model import Board

DATA = {"board_name": "board54"}


@pytest.mark.django_db
def test_board_model():
    board = Board(**DATA)
    board.save()

    assert board.board_name == DATA["board_name"]
    assert board.board_id
    assert board.created
    assert board.updated
