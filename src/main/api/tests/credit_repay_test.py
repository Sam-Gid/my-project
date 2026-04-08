import requests
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class TestCreditRepay:
    def test_credit_repay(self):
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

        create_user_request = CreateUserRequest(username='Sam001', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

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

        login_user_request = LoginUserRequest(username='Sam001', password='Pas!sw0rd')

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

        credit_id = response.json().get('creditId')

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)

        response = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json=credit_repay_request.model_dump(),
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        credit_repay_response = CreditRepayResponse(**response.json())

        assert response.status_code == 200
        assert credit_repay_response.amountDeposited == 5000


    def test_credit_repay_with_invalid_amount(self):
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

        create_user_request = CreateUserRequest(username='Sam002', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

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

        login_user_request = LoginUserRequest(username='Sam002', password='Pas!sw0rd')

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

        credit_id = response.json().get('creditId')

        boundary_values = [4999, 5001]

        # Проверяем, что суммы пополнений, которые не равны сумме кредита, отклоняются.
        for i in range(2):
            credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=boundary_values[i])

            credit_repay_response = requests.post(
                url='http://localhost:4111/api/credit/repay',
                json=credit_repay_request.model_dump(),
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            )

            expected_error = ['The amount is not enough. Credit balance: -5000',
                              'Insufficient funds. Current balance: 5000.00, required: 5001.00'
            ]
            assert credit_repay_response.status_code == 422
            assert credit_repay_response.json().get('error') in expected_error


    def test_repay_closed_credit(self):
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

        create_user_request = CreateUserRequest(username='Sam003', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')

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

        login_user_request = LoginUserRequest(username='Sam003', password='Pas!sw0rd')

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

        credit_id = response.json().get('creditId')

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)

        response = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json=credit_repay_request.model_dump(),
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        credit_repay_response = CreditRepayResponse(**response.json())

        assert response.status_code == 200
        assert credit_repay_response.amountDeposited == 5000

        repay_closed_credit_response = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json={
                'creditId': credit_id,
                'accountId': account_id,
                'amount': 5000
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        expected_error = 'Insufficient funds. Current balance: 0.00, required: 5000.00'
        assert repay_closed_credit_response.status_code == 422
        assert repay_closed_credit_response.json().get('error') == expected_error

