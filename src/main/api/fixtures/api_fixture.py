from typing import Any
import pytest
from src.main.api.classes.api_manager import ApiManager


@pytest.fixture
def api_manager(created_obj: list[Any]):
    return ApiManager(created_obj)
