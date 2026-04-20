import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user_request(api_manager: ApiManager) -> CreateUserRequest:
    # Создаем обычного пользователя (ROLE_USER).
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def login_admin_request(api_manager: ApiManager) -> LoginUserRequest:
    login_admin_request = LoginUserRequest(username='admin', password='123456')
    return login_admin_request


@pytest.fixture
def create_account_response(api_manager: ApiManager, create_user_request: CreateUserRequest) -> CreateAccountResponse:
    # Создаем банковский счет для обычного пользователя (create_user).
    create_account_response = api_manager.user_steps.create_account(create_user_request)
    return create_account_response


@pytest.fixture
def account_deposit_request(
        api_manager: ApiManager,
        create_account_response: CreateAccountResponse
) -> AccountDepositRequest:
    account_deposit_request = AccountDepositRequest(accountId=create_account_response.id, amount=5000)
    return account_deposit_request


@pytest.fixture
def create_transfer_accounts(api_manager: ApiManager, create_user_request: CreateUserRequest) -> list[int]:
    accounts = []
    # В цикле создаем два аккаунта.
    # Id аккаунтов записываются в переменную "accounts".
    for _ in range(2):
        response = api_manager.user_steps.create_account(create_user_request)
        accounts.append(response.id)
    return accounts


@pytest.fixture
def funded_account(
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        create_transfer_accounts: list[int]
) -> AccountDepositResponse:
    # Пополняем баланс аккаунта №1.
    account_id = create_transfer_accounts[0]
    account_deposit_request = AccountDepositRequest(accountId=account_id, amount=1500)
    account_deposit_response = api_manager.user_steps.account_deposit_request(create_user_request, account_deposit_request)
    return account_deposit_response


@pytest.fixture
def transfer_funds_request(
        api_manager: ApiManager,
        funded_account: AccountDepositResponse,
        create_transfer_accounts: list[int]
) -> TransferFundsRequest:
    transfer_funds_request = TransferFundsRequest(
        fromAccountId=funded_account.id,
        toAccountId=create_transfer_accounts[1],
        amount=500
    )
    return transfer_funds_request


@pytest.fixture
def create_credit_user_request(api_manager: ApiManager) -> CreateCreditUserRequest:
    # Создаем пользователя для кредитного счета (ROLE_CREDIT_SECRET).
    create_user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(create_user_request)
    return create_user_request


@pytest.fixture
def create_credit_account_response(
        api_manager: ApiManager,
        create_credit_user_request: CreateCreditUserRequest
) -> CreateAccountResponse:
    # Создаем банковский счет используя кредитный аккаунт (create_credit_user)
    create_credit_account_response = api_manager.user_steps.create_account(create_credit_user_request)
    return create_credit_account_response


@pytest.fixture
def credit_request_details(
        api_manager: ApiManager,
        create_credit_account_response: CreateAccountResponse
) -> CreditRequestModel:
    credit_request_model = CreditRequestModel(accountId=create_credit_account_response.id, amount=5000, termMonths=12)
    return credit_request_model


@pytest.fixture
def create_credit(
        api_manager: ApiManager,
        create_credit_user_request: CreateCreditUserRequest,
        credit_request_details: CreditRequestModel
) -> CreditRequestResponse:
    credit_request_response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request_details)
    return credit_request_response


@pytest.fixture
def credit_repay_request(api_manager: ApiManager, create_credit: CreditRequestResponse) -> CreditRepayRequest:
    credit_repay_request = CreditRepayRequest(
        creditId= create_credit.creditId,
        accountId=create_credit.id,
        amount=5000)
    return credit_repay_request