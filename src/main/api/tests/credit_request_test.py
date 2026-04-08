import requests
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_user_request import CreateUserRequest


class TestCreditRequest:
    def test_credit_request(self):
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

        create_user_request = CreateUserRequest(username='Sam004', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

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

        login_user_request = LoginUserRequest(username='Sam004', password='Pas!sw0rd')

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
        assert login_user_response.user.role == 'ROLE_CREDIT_SECRET'

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

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json=credit_request_model.model_dump(),
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        credit_request_response = CreditRequestResponse(**response.json())

        assert response.status_code == 201
        assert credit_request_response.balance == 5000


    def test_credit_request_without_permission(self):
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

        # Создаем пользователся без права на кредитование (ROLE_USER).
        create_user_request = CreateUserRequest(username='Sam005', password='Pas!sw0rd', role='ROLE_USER')

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

        login_user_request = LoginUserRequest(username='Sam005', password='Pas!sw0rd')

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

        credit_request_model = CreditRequestModel(accountId=account_id, amount=5000, termMonths=12)

        credit_request_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json=credit_request_model.model_dump(),
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        assert credit_request_response.status_code == 403


    def test_credit_request_with_invalid_amount(self):
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

        create_user_request = CreateUserRequest(username='Sam006', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

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

        login_user_request = LoginUserRequest(username='Sam006', password='Pas!sw0rd')

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
        assert login_user_response.user.role == 'ROLE_CREDIT_SECRET'

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

        boundary_values = [4999, 15001]

        # Проверяем, что суммы кредита ниже минимума и выше максимума отклоняются.
        for i in range(2):
            credit_request_model = CreditRequestModel(accountId=account_id, amount=boundary_values[i], termMonths=12)

            credit_request_response = requests.post(
                url='http://localhost:4111/api/credit/request',
                json=credit_request_model.model_dump(),
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            )

            assert credit_request_response.status_code == 400
            assert credit_request_response.json().get('error') == 'Amount must be between 5000 and 15000'

