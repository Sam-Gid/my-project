import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, create_user):
        response = api_manager.user_steps.create_account(create_user)

        assert response.balance == 0



