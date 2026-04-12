

class TestCreditRequest:
    def test_valid_credit_request(self, api_manager, create_credit_user, create_credit_account):
        response = api_manager.user_steps.valid_credit_request(create_credit_user, create_credit_account)

        assert response.balance == 5000

    def test_credit_request_without_permission(self, api_manager, create_user, create_account):

        # Используем пользователя без права на кредитование (create_user).
        response = api_manager.user_steps.invalid_role_credit_request(create_user, create_account)

        assert response.status_code == 403

    def test_credit_request_with_invalid_amount(self, api_manager, create_credit_user, create_credit_account):

        # Проверяем, что суммы кредита ниже минимума и выше максимума отклоняются.
        credit_amounts = [4999, 15001]
        for invalid_amount in credit_amounts:
            create_credit_account.amount = invalid_amount
            response = api_manager.user_steps.invalid_amount_credit_request(create_credit_user, create_credit_account)

            assert response.status_code == 400




