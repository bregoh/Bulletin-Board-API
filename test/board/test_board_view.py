import json

import pytest

from bulletin.models.board_model import Board
from users.models import User

ENDPOINT = "/api/board"
DATA = {"board_name": "board54"}
DATA_TO_UPDATE = {"board_name": "board55"}
SUPER_USER_EMAIL = "admin@admin.com"
USER_EMAIL = "test@admin.com"
PASSWORD = "test1234"


def create_board():
    board = Board(**DATA)
    board.save()
    return board


def create_super_user():
    User.objects.create_superuser(email=SUPER_USER_EMAIL, password=PASSWORD)


def create_user(client):
    client().post(
        "/user/register",
        data={"email": USER_EMAIL, "password": PASSWORD, "username": "admin_test"},
    )


def login(client, email, password):
    response = client().post("/user/login", data={"email": email, "password": password})
    return json.loads(response.content)["data"]


@pytest.mark.django_db
class TestBoardView:
    def test_superuser_can_post_board(self, client):
        # create super user
        create_super_user()

        # login as superuser
        login_data = login(client=client, email=SUPER_USER_EMAIL, password=PASSWORD)

        # send a post request
        response = client().post(
            ENDPOINT,
            data=DATA,
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        respone = json.loads(response.content)["data"]

        assert response.status_code == 201
        assert respone["board_name"] == DATA["board_name"]

    def test_any_user_can_list_board(self, client):
        create_board()
        response = client().get(ENDPOINT)
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_board_data) is list
        assert len(respone_board_data) > 0

    def test_any_user_can_retrieve_board(self, client):
        board = create_board()
        board_id = board.board_id

        response = client().get(f"{ENDPOINT}/{board_id}")
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_board_data) is dict
        assert respone_board_data["board_id"] == str(board_id)

    def test_any_user_can_retrieve_empty_board_with_404(self, client):
        board_id = "9aaa3c62-c4a7-494a-87cf-d4c0e2051b3a"
        response = client().get(f"{ENDPOINT}/{board_id}")
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 404
        assert len(respone_board_data) == 0

    def test_board_admin_can_update_board(self, client):
        # create super user
        create_super_user()

        # login as super user
        login_data = login(client=client, email=SUPER_USER_EMAIL, password=PASSWORD)

        # create board
        board = create_board()
        board_id = board.board_id

        response = client().put(
            f"{ENDPOINT}/{board_id}",
            data=DATA_TO_UPDATE,
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        respone_board_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_board_data) is dict
        assert respone_board_data["board_id"] == str(board_id)
        assert respone_board_data["board_name"] != DATA["board_name"]
        assert respone_board_data["board_name"] == DATA_TO_UPDATE["board_name"]

    def test_board_admin_can_delete_board(self, client):
        # create super user
        create_super_user()

        # login as super user
        login_data = login(client=client, email=SUPER_USER_EMAIL, password=PASSWORD)

        board = create_board()
        board_id = board.board_id

        response = client().delete(
            f"{ENDPOINT}/{board_id}",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        board = Board.objects.filter(board_id=board_id)

        assert response.status_code == 204
        assert board.exists() is False

    def test_board_moderator_can_delete_board(self, client):
        # create super user
        create_user(client)

        # login as super user
        login_data = login(client=client, email=USER_EMAIL, password=PASSWORD)

        board = create_board()
        board_id = board.board_id

        response = client().delete(
            f"{ENDPOINT}/{board_id}",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        board = Board.objects.filter(board_id=board_id)

        assert response.status_code == 401
