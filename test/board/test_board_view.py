import json
import pytest
from bulletin.models.board_model import Board


ENDPOINT = "/api/board"
DATA = {"board_name": "board54"}
DATA_TO_UPDATE = {"board_name": "board55"}


def create_board():
    board = Board(**DATA)
    board.save()
    return board


@pytest.mark.django_db
class TestBoardView:
    def test_post_board(self, client):
        response = client().post(ENDPOINT, data=DATA, format="json")
        respone = json.loads(response.content)["data"]

        assert response.status_code == 201
        assert respone["board_name"] == DATA["board_name"]

    def test_list_board(self, client):
        create_board()
        response = client().get(ENDPOINT)
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_board_data) is list
        assert len(respone_board_data) > 0

    def test_retrieve_board(self, client):
        board = create_board()
        board_id = board.board_id

        response = client().get(f"{ENDPOINT}/{board_id}")
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_board_data) is dict
        assert respone_board_data["board_id"] == str(board_id)

    def test_retrieve_board_returns_404(self, client):
        board_id = "9aaa3c62-c4a7-494a-87cf-d4c0e2051b3a"
        response = client().get(f"{ENDPOINT}/{board_id}")

        assert response.status_code == 404

    def test_update_board(self, client):
        board = create_board()
        board_id = board.board_id

        response = client().put(
            f"{ENDPOINT}/{board_id}", data=DATA_TO_UPDATE, format="json"
        )
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_board_data) is dict
        assert respone_board_data["board_id"] == str(board_id)
        assert respone_board_data["board_name"] != DATA["board_name"]
        assert respone_board_data["board_name"] == DATA_TO_UPDATE["board_name"]

    def test_delete_board(self, client):
        board = create_board()
        board_id = board.board_id

        response = client().delete(f"{ENDPOINT}/{board_id}")
        board = Board.objects.filter(board_id=board_id)

        assert response.status_code == 204
        assert board.exists() is False
