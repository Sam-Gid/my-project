import requests
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.transfer_funds_response import TransferFundsResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_user_request import CreateUserRequest


class TestTransferFunds:
    def test_valid_transfer_funds(self):
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

        create_user_request = CreateUserRequest(username='Sam009', password='Pas!sw0rd', role='ROLE_USER')

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

        login_user_request = LoginUserRequest(username='Sam009', password='Pas!sw0rd')

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

        accounts = []

        # В цикле создаем два аккаунта для осуществления перевода между ними.
        # Id аккаунтов записываются в переменную "accounts".
        for _ in range(2):
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

            accounts.append(response.json().get('id'))

        account_one_id, account_two_id = accounts[0], accounts[1]

        deposit_account_request = DepositAccountRequest(accountId=account_one_id, amount=1000.5)

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

        transfer_funds_request = TransferFundsRequest(fromAccountId=account_one_id, toAccountId=account_two_id, amount=500.5)

        response = requests.post(
            url='http://localhost:4111/api/account/transfer',
            json=transfer_funds_request.model_dump(),
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-type': 'application/json'
            }
        )

        transfer_funds_response = TransferFundsResponse(**response.json())

        assert response.status_code == 200
        assert transfer_funds_response.fromAccountIdBalance == 500


    def test_transfer_founds_with_invalid_amount(self):
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

        create_user_request = CreateUserRequest(username='Sam010', password='Pas!sw0rd', role='ROLE_USER')

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

        login_user_request = LoginUserRequest(username='Sam010', password='Pas!sw0rd')

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

        accounts = []

        # В цикле создаем два аккаунта для осуществления перевода между ними.
        # Id аккаунтов записываются в переменную "accounts".
        for _ in range(2):
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

            accounts.append(response.json().get('id'))

        account_one_id, account_two_id = accounts[0], accounts[1]

        boundary_values = [499, 10001]

        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        for i in range(2):
            transfer_funds_request = TransferFundsRequest(fromAccountId=account_one_id, toAccountId=account_two_id, amount=boundary_values[i])

            transfer_funds_response = requests.post(
                url='http://localhost:4111/api/account/transfer',
                json=transfer_funds_request.model_dump(),
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                    'Content-type': 'application/json'
                }
            )

            assert transfer_funds_response.status_code == 400
            assert transfer_funds_response.json().get('error') == 'Amount must be between 500 and 10000'
