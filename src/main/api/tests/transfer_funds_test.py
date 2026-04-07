import requests


class TestTransferFunds:
    def test_transfer_funds(self):
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'admin',
                'password': '123456'
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': 'Max44',
                'password': 'Pas!sw0rd',
                'role': 'ROLE_USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'Max44',
                'password': 'Pas!sw0rd'
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get('token')

        accounts = []

        for _ in range(2):

            # В цикле создаются два аккаунта для осуществления перевода между ними.
            # Id аккаунтов записываются в переменную "accounts".

            create_account_response = requests.post(
                url='http://localhost:4111/api/account/create',
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
            )

            assert create_account_response.status_code == 201
            assert create_account_response.json().get('balance') == 0

            accounts.append(create_account_response.json().get('id'))

        account_one_id, account_two_id = accounts[0], accounts[1]

        deposit_account_one_response = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json={
                'accountId': account_one_id,
                'amount': 1000.5
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

        assert deposit_account_one_response.status_code == 200
        assert deposit_account_one_response.json().get('balance') == 1000.5

        transfer_funds_response = requests.post(
            url='http://localhost:4111/api/account/transfer',
            json={
                "fromAccountId": account_one_id,
                "toAccountId": account_two_id,
                "amount": 500.5
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-type': 'application/json'
            }
        )

        assert transfer_funds_response.status_code == 200
        assert transfer_funds_response.json().get('fromAccountIdBalance') == 500


