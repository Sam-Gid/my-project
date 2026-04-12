

class TestDepositAccount:
    def test_valid_deposit_account(self, api_manager, create_user, create_account):
        response = api_manager.user_steps.account_deposit_request(create_user, create_account)

        assert response.balance == 1500


    def test_deposit_account_with_invalid_amount(self, api_manager, create_user, create_account):
        deposit_amounts = [999, 9001]

        # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются.
        for invalid_amount in deposit_amounts:
            create_account.amount = invalid_amount
            response = api_manager.user_steps.account_invalid_deposit_request(create_user, create_account)

            assert response.status_code == 400
