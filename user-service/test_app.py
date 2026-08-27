#Fix 7 : Added test_app.py in user-service and order-service ( USED AI FOR GENERATING TEST CASES ).
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


# Mock PostgreSQL and Redis before importing app
mock_db = MagicMock()
mock_redis = MagicMock()

with patch("psycopg2.connect", return_value=mock_db), \
     patch("redis.Redis", return_value=mock_redis):

    from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["service"] == "user-service"


def test_list_users():
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        (1, "devansh", "devansh@example.com"),
        (2, "rahul", "rahul@example.com")
    ]

    mock_db.cursor.return_value = mock_cursor

    client = app.test_client()

    response = client.get("/users")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["username"] == "devansh"
    assert data[0]["email"] == "devansh@example.com"


def test_get_user():
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = (
        1,
        "devansh",
        "devansh@example.com"
    )

    mock_db.cursor.return_value = mock_cursor

    client = app.test_client()

    response = client.get("/users/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["username"] == "devansh"
    assert data["email"] == "devansh@example.com"


def test_get_user_not_found():
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None

    mock_db.cursor.return_value = mock_cursor

    client = app.test_client()

    response = client.get("/users/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "User not found"


def test_cache_stats():
    mock_redis.info.return_value = {
        "keyspace_hits": 10,
        "keyspace_misses": 3
    }

    client = app.test_client()

    response = client.get("/cache/stats")

    assert response.status_code == 200

    data = response.get_json()

    assert data["hits"] == 10
    assert data["misses"] == 3