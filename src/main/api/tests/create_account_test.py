import pytest
import requests
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        login_user_request = LoginUserRequest(username='admin', password='123456')

        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        login_user_response = LoginUserResponse(**response.json())

        assert response.status_code == 200
        assert login_user_response.user.username == 'admin'
        assert login_user_response.user.role == 'ROLE_ADMIN'

        token = response.json().get('token')

        create_user_request = CreateUserRequest(username='Sam012', password='Pas!sw0rd', role='ROLE_USER')

        response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        create_user_response = CreateUserResponse(**response.json())

        assert response.status_code == 200
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

        login_user_request = LoginUserRequest(username='Sam012', password='Pas!sw0rd')

        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        login_user_response = LoginUserResponse(**response.json())

        assert response.status_code == 200
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == 'ROLE_USER'

        token = response.json().get('token')

        response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        create_account_response = CreateAccountResponse(**response.json())

        assert response.status_code == 201
        assert create_account_response.balance == 0
