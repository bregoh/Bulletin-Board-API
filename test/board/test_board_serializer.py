import pytest

from bulletin.serializers import BoardSerializer

DATA = {"board_name": "board54"}


@pytest.mark.django_db
def test_thread_serializer_valid_data():
    serializer = BoardSerializer(data=DATA)

    assert serializer.is_valid()
    assert len(serializer.errors) == 0
    assert serializer.data["board_name"] == DATA["board_name"]
