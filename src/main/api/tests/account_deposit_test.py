import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


class TestDepositAccount:
    def test_valid_deposit_account(
            self,
            api_manager,
            create_user_request,
            account_deposit_request,
            db_session: Session
    ):
        response = api_manager.user_steps.account_deposit_request(create_user_request, account_deposit_request)
        assert response.balance == account_deposit_request.amount, 'Ошибка: Баланс аккаунта не пополнен'

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == response.balance, ('Ошибка: Баланс аккаунта не пополнен. '
                                                             'Поле "Баланс" в БД не изменено'
                                                             )


    @pytest.mark.parametrize(
        "deposit_amount",
        [999, 9001]
    )
    def test_deposit_account_with_invalid_amount(
            self,
            api_manager,
            create_user_request,
            account_deposit_request,
            deposit_amount,
            create_account_response,
            db_session: Session
    ):
        # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются.
        account_deposit_request.amount = deposit_amount
        response = api_manager.user_steps.account_invalid_deposit_request(create_user_request, account_deposit_request)
        assert response.status_code == 400, 'Ошибка: Пополнен баланс аккаунта'

        account_from_db = Account.get_account_by_id(db_session, account_deposit_request.accountId)
        assert account_from_db.balance == create_account_response.balance, 'Ошибка: Баланс аккаунта в БД изменен'