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
        response = api_manager.user_steps.transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.fromAccountIdBalance == funded_account_balance - transfer_funds_request.amount, \
            'Ошибка, перевод не выполнен'

        source_account = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId)
        target_account = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId)

        assert source_account.balance == funded_account_balance - transfer_funds_request.amount, \
            'Ошибка, баланс source_account в БД не обновлен'
        assert target_account.balance == transfer_funds_request.amount, \
            'Ошибка, баланс target_account в БД не обновлен'


    @pytest.mark.parametrize(
        "fund_amount",
        [499, 10001]
    )
    def test_transfer_funds_with_invalid_amount(
            self,
            api_manager,
            create_user_request,
            transfer_funds_request,
            funded_account,
            fund_amount,
            db_session: Session):
        funded_account_balance = funded_account.balance

        source_account = Account.get_account_by_id(db_session, transfer_funds_request.fromAccountId)
        target_account = Account.get_account_by_id(db_session, transfer_funds_request.toAccountId)

        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        transfer_funds_request.amount = fund_amount
        response = api_manager.user_steps.invalid_transfer_funds_request(create_user_request, transfer_funds_request)
        assert response.status_code == 400, 'Ошибка, перевод исполнен'
        assert source_account.balance == funded_account_balance, 'Ошибка, баланс source_account в БД обновлен'
        assert target_account.balance == 0, 'Ошибка, баланс target_account в БД обновлен'
