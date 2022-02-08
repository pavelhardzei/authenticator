import pytest
from project import app


@pytest.fixture
def api_client():
    yield app.test_client()
