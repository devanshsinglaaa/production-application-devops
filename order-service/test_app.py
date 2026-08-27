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


# Mock PostgreSQL before importing app
mock_db = MagicMock()

with patch("psycopg2.connect", return_value=mock_db):

    from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_create_order():
    mock_cursor = MagicMock()

    mock_db.cursor.return_value = mock_cursor

    client = app.test_client()

    order_data = {
        "user_id": 1,
        "product_name": "Laptop",
        "quantity": 2,
        "total_price": 1500.00
    }

    response = client.post(
        "/orders",
        json=order_data
    )

    assert response.status_code in [200, 201]

    mock_cursor.execute.assert_called()


def test_get_orders_by_user():
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        (
            "order-1",
            1,
            "Laptop",
            2,
            1500.00
        )
    ]

    mock_db.cursor.return_value = mock_cursor

    client = app.test_client()

    response = client.get("/orders/user/1")

    assert response.status_code == 200


def test_get_orders_for_user_with_no_orders():
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = []

    mock_db.cursor.return_value = mock_cursor

    client = app.test_client()

    response = client.get("/orders/user/999")

    assert response.status_code == 200

    data = response.get_json()

    assert data == []