

class TestTransferFunds:
    def test_valid_transfer_funds(self, api_manager, create_user, create_transfer_funds_accounts):
        response = api_manager.user_steps.transfer_funds_request(create_user, create_transfer_funds_accounts)

        assert response.fromAccountIdBalance == 1000


    def test_transfer_funds_with_invalid_amount(self, api_manager, create_user, create_transfer_funds_accounts):
        funds_amount = [499, 10001]

        # Проверяем, что суммы перевода ниже минимума и выше максимума отклоняются.
        for invalid_amount in funds_amount:
            create_transfer_funds_accounts.amount = invalid_amount
            response = api_manager.user_steps.invalid_transfer_funds_request(create_user, create_transfer_funds_accounts)

            assert response.status_code == 400
