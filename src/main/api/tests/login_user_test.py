import pytest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager, login_admin_request):
        response = api_manager.admin_steps.login_user(login_admin_request)
        assert response.user.role == 'ROLE_ADMIN'


    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)
        assert create_user_request.username == response.user.username


