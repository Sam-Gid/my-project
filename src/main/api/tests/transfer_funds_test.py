import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


class TestTransferFunds:
    def test_valid_transfer_funds(
            self,
            api_manager,
            create_user_request,
            transfer_funds_request,
            funded_account,
            db_session: Session
    ):
        funded_account_balance = funded_account.balance
        expected_balance = funded_account_balance - transfer_funds_request.amount

        response = api_manager.user_steps.transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.fromAccountIdBalance == expected_balance, (
            f'Ошибка: Неверный баланс отправителя. '
            f'Ожидалось: {expected_balance}, получено: {response.fromAccountIdBalance}'
        )

        source_account = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId)
        target_account = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId)
        assert source_account.balance == expected_balance, (
            f'Ошибка: Неверный баланс отправителя в БД. '
            f'Ожидалось: {expected_balance}, получено: {source_account.balance}'
        )
        assert target_account.balance == transfer_funds_request.amount, (
            f'Ошибка: Неверный баланс получателя в БД (target_account_balance). '
            f'Ожидалось: {transfer_funds_request.amount}, получено: {target_account.balance}'
        )


    @pytest.mark.parametrize(
        "transfer_amount",
        [499, 10001]
    )
    def test_transfer_funds_with_invalid_amount(
            self,
            api_manager,
            create_user_request,
            transfer_funds_request,
            funded_account,
            transfer_amount,
            db_session: Session):
        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        funded_account_balance = funded_account.balance
        transfer_funds_request.amount = transfer_amount

        response = api_manager.user_steps.invalid_transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.status_code == 400, f'Ожидался статус-код: 400, получен: {response.status_code}'

        source_account = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId)
        target_account = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId)

        assert source_account.balance == funded_account_balance, (
            f'Ошибка: Баланс отправителя изменился после перевода невалидной суммы. '
            f'Ожидалось: {funded_account_balance}, получено: {source_account.balance}'
        )
        assert target_account.balance == 0, (
            f'Ошибка: Баланс получателя изменился после невалидного перевода. '
            f'Ожидалось: 0, получено: {target_account.balance}'
        )