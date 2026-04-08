import requests
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class TestDepositAccount:
    def test_valid_deposit_account(self):
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

        create_user_request = CreateUserRequest(username='Sam007', password='Pas!sw0rd', role='ROLE_USER')

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

        login_user_request = LoginUserRequest(username='Sam007', password='Pas!sw0rd')

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

        account_id = response.json().get('id')

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=1000.5)

        response = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json=deposit_account_request.model_dump(),
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        deposit_account_response = DepositAccountResponse(**response.json())

        assert response.status_code == 200
        assert deposit_account_response.balance == 1000.5


    def test_deposit_account_with_invalid_amount(self):
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

        create_user_request = CreateUserRequest(username='Sam008', password='Pas!sw0rd', role='ROLE_USER')

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

        login_user_request = LoginUserRequest(username='Sam008', password='Pas!sw0rd')

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

        account_id = response.json().get('id')

        boundary_values = [999, 9001]

        # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются.
        for i in range(2):
            deposit_account_request = DepositAccountRequest(accountId=account_id, amount=boundary_values[i])

            deposit_account_response = requests.post(
                url='http://localhost:4111/api/account/deposit',
                json=deposit_account_request.model_dump(),
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            )

            assert deposit_account_response.status_code == 400
            assert deposit_account_response.json().get('error') == 'Amount must be between 1000 and 9000'

