import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager, login_admin_request: LoginUserRequest):
        response = api_manager.admin_steps.login_user(login_admin_request)
        assert response.user.role == "ROLE_ADMIN", "Ошибка: Роль пользователя не соответствует запросу"


    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)
        assert create_user_request.username == response.user.username, (
            "Ошибка: Имя пользователя не соответствует запросу"
        )