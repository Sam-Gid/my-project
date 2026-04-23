import pytest
from http import HTTPStatus
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.helpers.account_helpers import get_db_balance, get_last_transaction
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest


class TestTransferFunds:
    def test_valid_transfer_funds(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            transfer_funds_request: TransferFundsRequest,
            funded_account: AccountDepositResponse,
            db_session: Session
    ):
        sender, recipient = transfer_funds_request.fromAccountId, transfer_funds_request.toAccountId
        amount = transfer_funds_request.amount

        # Получаем из таблицы в БД баланс отправителя и получателя ДО перевода.
        sender_balance_before = get_db_balance(db_session, sender)
        recipient_balance_before = get_db_balance(db_session, recipient)

        api_manager.user_steps.transfer_funds_request(create_user_request, transfer_funds_request)

        # Получаем последнюю транзакцию отправителя и получателя.
        sender_transaction =  get_last_transaction(api_manager, create_user_request, sender)
        recipient_transaction = get_last_transaction(api_manager, create_user_request, recipient)
        assert sender_transaction.amount == -amount
        assert recipient_transaction.amount == amount

        # Получаем из таблицы в БД баланс отправителя и получателя ПОСЛЕ перевода.
        sender_balance_after = get_db_balance(db_session, sender)
        recipient_balance_after = get_db_balance(db_session, recipient)
        assert amount == sender_balance_before - sender_balance_after
        assert amount == recipient_balance_after - recipient_balance_before


    @pytest.mark.parametrize(
        "transfer_amount",
        [499, 10001]
    )
    def test_transfer_funds_with_invalid_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            transfer_funds_request: TransferFundsRequest,
            transfer_amount: int,
            funded_account: AccountDepositResponse,
            db_session: Session):
        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        transfer_funds_request.amount = transfer_amount

        # Получаем из таблицы в БД баланс отправителя и получателя ДО перевода.
        sender_balance_before = get_db_balance(db_session, transfer_funds_request.fromAccountId)
        recipient_balance_before = get_db_balance(db_session, transfer_funds_request.toAccountId)

        response = api_manager.user_steps.invalid_transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Ошибка: Неправильный статус код. '
            f'Ожидалось: {HTTPStatus.BAD_REQUEST}, получено: {response.status_code}'
        )

        # Получаем из таблицы в БД баланс отправителя и получателя ПОСЛЕ перевода.
        sender_balance_after = get_db_balance(db_session, transfer_funds_request.fromAccountId)
        recipient_balance_after = get_db_balance(db_session, transfer_funds_request.toAccountId)

        assert sender_balance_after == sender_balance_before, (
            f'Ошибка: Баланс отправителя изменился после перевода невалидной суммы. '
            f'Ожидалось: {sender_balance_before}, получено: {sender_balance_after}'
        )
        assert recipient_balance_after == recipient_balance_before, (
            f'Ошибка: Баланс получателя изменился после невалидного перевода. '
            f"Ожидалось: {recipient_balance_before}, получено: {recipient_balance_after}"
        )