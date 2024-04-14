from datetime import datetime

import pytest
from fastapi import HTTPException

from app.models.user import User
from app.requests.user import UserCreateRequest, UserUpdateRequest
from app.services.user import UserService


class MockSession:
    def __init__(self):
        self.users = []

    def query(self, model):
        return self

    def filter(self, condition):
        if hasattr(condition, "right") and hasattr(condition.right, "value"):
            value = condition.right.value
            if hasattr(condition.left, "key"):
                attribute = condition.left.key
                self.filtered_users = [
                    user for user in self.users if getattr(user, attribute) == value
                ]
            else:
                self.filtered_users = [user for user in self.users if user.id == value]
        return self

    def first(self):
        return self.filtered_users[0] if self.filtered_users else None

    def offset(self, offset):
        self.pagination_offset = offset
        return self

    def limit(self, limit):
        self.pagination_limit = limit
        return self

    def all(self):
        start = self.pagination_offset
        end = start + self.pagination_limit
        return self.users[start:end]

    def count(self):
        return len(self.users)

    def add(self, item):
        if not hasattr(item, "id") or item.id is None:
            item.id = len(self.users) + 1
        if not hasattr(item, "created_at") or item.created_at is None:
            item.created_at = datetime.now()
        if not hasattr(item, "updated_at") or item.updated_at is None:
            item.updated_at = datetime.now()
        self.users.append(item)

    def refresh(self, item):
        if not item.created_at:
            item.created_at = datetime.now()
        if not item.updated_at:
            item.updated_at = datetime.now()

    def commit(self):
        pass

    def delete(self, item):
        self.users.remove(item)

    def order_by(self, *args, **kwargs):
        return self


@pytest.fixture
def mock_db_session():
    return MockSession()


def add_users_to_session(session, num_users):
    for i in range(1, num_users + 1):
        user = User(
            id=i,
            username=f"user{i}",
            email=f"user{i}@example.com",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.users.append(user)


@pytest.mark.parametrize("user_id, expected_result", [(1, True), (99, False)])
def test_get_by_id(mock_db_session, user_id, expected_result):
    add_users_to_session(mock_db_session, 5)
    user_service = UserService(db=mock_db_session)

    if expected_result:
        result = user_service.get_by_id(user_id)
        assert result.id == user_id
    else:
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_by_id(user_id)
        assert exc_info.value.status_code == 404


def test_all_with_pagination(mock_db_session):
    add_users_to_session(mock_db_session, 10)
    user_service = UserService(db=mock_db_session)

    users, total, last_page, first_item, last_item = user_service.all(1, 5)
    assert len(users) == 5
    assert total == 10
    assert last_page == 2
    assert first_item == 1
    assert last_item == 5


def test_total(mock_db_session):
    add_users_to_session(mock_db_session, 3)
    user_service = UserService(db=mock_db_session)

    result = user_service.total()

    assert result == 3


def test_find_user(mock_db_session):
    user = User(
        id=1,
        username="testuser1",
        email="user1@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_db_session.users.append(user)

    user_service = UserService(db=mock_db_session)
    result = user_service.find(1)

    assert result.id == user.id
    assert result.username == user.username


def test_save_user(mock_db_session):
    user_service = UserService(db=mock_db_session)
    user_request = UserCreateRequest(
        username="testnewuser", email="new_user@example.com", password="password"
    )

    saved_user = user_service.save(user_request)

    assert isinstance(saved_user, dict)
    assert "id" in saved_user
    assert saved_user["username"] == "testnewuser"
    assert saved_user["email"] == "new_user@example.com"


def test_save_duplicate_email_user(mock_db_session):
    add_users_to_session(mock_db_session, 1)
    user_service = UserService(db=mock_db_session)
    user_request = UserCreateRequest(
        username="testuser2", email="user1@example.com", password="password"
    )

    with pytest.raises(HTTPException) as exc_info:
        user_service.save(user_request)
    assert exc_info.value.status_code == 422


def test_update_user(mock_db_session):
    user = User(
        id=1,
        username="testuser1",
        email="user1@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_db_session.users.append(user)

    user_service = UserService(db=mock_db_session)
    user_request = UserUpdateRequest(
        username="testupdateduser", email="updated_user@example.com"
    )

    result = user_service.update(1, user_request)

    assert result["username"] == "testupdateduser"
    assert result["email"] == "updated_user@example.com"


def test_update_nonexistent_user(mock_db_session):
    user_service = UserService(db=mock_db_session)
    user_request = UserUpdateRequest(username="testuser2", email="user2@example.com")

    with pytest.raises(HTTPException) as exc_info:
        user_service.update(2, user_request)
    assert exc_info.value.status_code == 404


def test_delete_user(mock_db_session):
    user = User(
        id=1,
        username="testuser1",
        email="user1@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_db_session.users.append(user)

    user_service = UserService(db=mock_db_session)
    user_service.delete(1)

    assert len(mock_db_session.users) == 0


def test_delete_nonexistent_user(mock_db_session):
    user_service = UserService(db=mock_db_session)

    with pytest.raises(HTTPException) as exc_info:
        user_service.delete(2)
    assert exc_info.value.status_code == 404


def test_get_by_id_success(mock_db_session):
    user_service = UserService(db=mock_db_session)
    mock_db_session.users.append(
        User(id=1, username="testuser", email="test@example.com")
    )
    user = user_service.get_by_id(1)
    assert user.id == 1
    assert user.username == "testuser"


def test_get_by_id_not_found(mock_db_session):
    user_service = UserService(db=mock_db_session)
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_by_id(999)
    assert exc_info.value.status_code == 404


def test_all_success(mock_db_session):
    user_service = UserService(db=mock_db_session)
    add_users_to_session(mock_db_session, 10)
    users, total, last_page, first_item, last_item = user_service.all(1, 5)
    assert len(users) == 5
    assert total == 10
    assert last_page == 2
    assert first_item == 1
    assert last_item == 5


def test_save_user_success(mock_db_session):
    user_service = UserService(db=mock_db_session)
    user_request = UserCreateRequest(
        username="testnewuser", email="new_user@example.com", password="password"
    )

    saved_user_dict = user_service.save(user_request)

    assert isinstance(saved_user_dict, dict)
    assert "username" in saved_user_dict
    assert saved_user_dict["username"] == "testnewuser"
    assert saved_user_dict["email"] == "new_user@example.com"


def test_update_user_success(mock_db_session):
    user = User(
        id=1,
        username="testuser1",
        email="user1@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_db_session.users.append(user)

    user_service = UserService(db=mock_db_session)
    user_update_request = UserUpdateRequest(
        username="testupdateduser", email="updated_user@example.com"
    )

    updated_user_dict = user_service.update(1, user_update_request)

    assert isinstance(updated_user_dict, dict)
    assert "username" in updated_user_dict
    assert updated_user_dict["username"] == "testupdateduser"
    assert updated_user_dict["email"] == "updated_user@example.com"


def test_update_user_not_found(mock_db_session):
    user_service = UserService(db=mock_db_session)
    user_request = UserUpdateRequest(username="testuser2", email="test2@example.com")
    with pytest.raises(HTTPException) as exc_info:
        user_service.update(999, user_request)
    assert exc_info.value.status_code == 404


def test_delete_user_success(mock_db_session):
    user = User(
        id=1,
        username="testuser1",
        email="user1@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_db_session.users.append(user)

    user_service = UserService(db=mock_db_session)
    deleted_user_response = user_service.delete(1)

    assert deleted_user_response["id"] == 1
    assert deleted_user_response["username"] == "testuser1"
    assert isinstance(deleted_user_response["created_at"], str)
    assert isinstance(deleted_user_response["updated_at"], str)
    assert len(mock_db_session.users) == 0


def test_delete_user_not_found(mock_db_session):
    user_service = UserService(db=mock_db_session)
    with pytest.raises(HTTPException) as exc_info:
        user_service.delete(999)
    assert exc_info.value.status_code == 404
