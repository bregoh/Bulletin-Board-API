import json

import pytest

from bulletin.models.board_model import Board
from bulletin.models.thread_model import Thread
from users.models import User

ENDPOINT = "/api/thread"
BOARD_DATA = {"board_name": "board54"}
BOARD_DATA_TO_UPDATE = {"board_name": "board55"}
THREAD_DATA = {
    "thread_title": "This is good deal",
    "thread_contents": "Yes Yes, the best in town.",
}
THREAD_DATA_TO_UPDATE = {
    "thread_title": "This is BAD deal",
    "thread_contents": "the town's worst of them all.",
}
SUPER_USER_EMAIL = "admin@admin.com"
USER_EMAIL = "test@admin.com"
PASSWORD = "test1234"


def create_board():
    board = Board.objects.create(**BOARD_DATA)
    return board


def create_thread():
    board = create_board()
    thread = Thread(board=board, **THREAD_DATA)
    thread.save()
    return thread


def get_board_id():
    board = Board.objects.all().first()
    return board.board_id


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
class TestThreadView:
    def test_super_user_can_post_thread(self, client):  # create super user
        create_super_user()

        # login as superuser
        login_data = login(client=client, email=SUPER_USER_EMAIL, password=PASSWORD)

        create_board()
        board_id = get_board_id()

        response = client().post(
            ENDPOINT,
            data={**THREAD_DATA, "board": str(board_id)},
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        respone = json.loads(response.content)["data"]

        assert response.status_code == 201
        assert respone["thread_title"] == THREAD_DATA["thread_title"]
        assert respone["board"] == str(board_id)

    def test_list_thread(self, client):
        create_thread()

        response = client().get(ENDPOINT)
        respone_thread_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_thread_data) is list
        assert len(respone_thread_data) > 0

    def test_retrieve_thread(self, client):
        thread = create_thread()
        thread_id = thread.thread_id
        board_id = get_board_id()

        response = client().get(f"{ENDPOINT}/{thread_id}")
        respone_thread_data = json.loads(response.content)["data"]

        assert response.status_code == 200
        assert type(respone_thread_data) is dict
        assert respone_thread_data["thread_id"] == str(thread_id)
        assert respone_thread_data["board_id"] == str(board_id)
        assert respone_thread_data["thread_title"] == THREAD_DATA["thread_title"]
        assert respone_thread_data["thread_contents"] == THREAD_DATA["thread_contents"]

    def test_retrieve_thread_returns_404(self, client):
        thread_id = "9aaa3c62-c4a7-494a-87cf-d4c0e2051b3a"
        response = client().get(f"{ENDPOINT}/{thread_id}")
        respone_thread_data = json.loads(response.content)["data"]

        assert response.status_code == 404
        assert len(respone_thread_data) == 0

    def test_super_user_can_update_thread(self, client):
        # create super user
        create_super_user()

        # login as superuser
        login_data = login(client=client, email=SUPER_USER_EMAIL, password=PASSWORD)

        thread = create_thread()
        thread_id = thread.thread_id
        board_id = get_board_id()

        response = client().put(
            f"{ENDPOINT}/{thread_id}",
            data={**THREAD_DATA_TO_UPDATE, "board": str(board_id)},
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        respone_thread_data = json.loads(response.content)["data"]
        thread_title = respone_thread_data["thread_title"]
        thread_contents = respone_thread_data["thread_contents"]

        assert response.status_code == 200
        assert type(respone_thread_data) is dict
        assert respone_thread_data["thread_id"] == str(thread_id)
        assert respone_thread_data["board"] == str(board_id)
        assert thread_title == THREAD_DATA_TO_UPDATE["thread_title"]
        assert thread_contents == THREAD_DATA_TO_UPDATE["thread_contents"]
        assert thread_title != THREAD_DATA["thread_title"]
        assert thread_contents != THREAD_DATA["thread_contents"]

    def test_super_user_can_delete_thread(self, client):
        # create super user
        create_super_user()

        # login as superuser
        login_data = login(client=client, email=SUPER_USER_EMAIL, password=PASSWORD)

        thread = create_thread()
        thread_id = thread.thread_id

        response = client().delete(
            f"{ENDPOINT}/{thread_id}",
            HTTP_AUTHORIZATION=f'Bearer {login_data["access"]}',
        )
        thread_query = Thread.objects.filter(thread_id=thread_id)

        assert response.status_code == 204
        assert thread_query.exists() is False
