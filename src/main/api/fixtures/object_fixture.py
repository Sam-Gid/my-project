import logging
from typing import Any, Generator
import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj() -> Generator[list[Any], Any, None]:
    objects: list[Any] = []
    yield objects
    clean_users(objects)

def clean_users(objects: list[Any]):
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f'Error in delete user_id: {u.id}')