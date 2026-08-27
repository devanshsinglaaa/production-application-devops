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


