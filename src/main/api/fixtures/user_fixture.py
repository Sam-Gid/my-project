import pytest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user(api_manager):
    # Создаем обычного пользователя (ROLE_USER).
    create_user_request = CreateUserRequest(username='Sam07', password='Pas!sw0rd', role='ROLE_USER')
    api_manager.admin_steps.create_user(create_user_request)
    return create_user_request


@pytest.fixture
def create_account(api_manager, create_user):
    # Создаем банковский счет для обычного пользователя (create_user).
    account = api_manager.user_steps.create_account(create_user)

    account_deposit_request = AccountDepositRequest(accountId=account.id, amount=1500)
    return account_deposit_request


@pytest.fixture
def create_transfer_funds_accounts(api_manager, create_user):
    accounts = []

    # В цикле создаем два аккаунта для осуществления перевода между ними.
    # Id аккаунтов записываются в переменную "accounts".
    for _ in range(2):
        response = api_manager.user_steps.create_account(create_user)
        accounts.append(response.id)

    # Пополняем баланс аккаунта №1.
    account_deposit_request = AccountDepositRequest(accountId=accounts[0], amount=1500)
    api_manager.user_steps.account_deposit_request(create_user, account_deposit_request)

    transfer_funds_request = TransferFundsRequest(fromAccountId=accounts[0], toAccountId=accounts[1], amount=500)
    return transfer_funds_request


@pytest.fixture
def create_credit_user(api_manager):
    # Создаем пользователя для кредитного счета (ROLE_CREDIT_SECRET).
    user_request = CreateUserRequest(username='Sam07', password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_account(api_manager, create_credit_user):
    # Создаем банковский счет используя кредитный аккаунт (create_credit_user)
    account = api_manager.user_steps.create_account(create_credit_user)

    credit_request_model = CreditRequestModel(accountId=account.id, amount=5000, termMonths=12)
    return credit_request_model


@pytest.fixture
def create_credit_request(api_manager, create_credit_user, create_credit_account):
    response = api_manager.user_steps.valid_credit_request(create_credit_user, create_credit_account)

    credit_repay_request = CreditRepayRequest(creditId=response.creditId, accountId=response.id, amount=5000)
    return credit_repay_request
