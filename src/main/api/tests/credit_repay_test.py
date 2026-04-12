

class TestCreditRepay:
    def test_credit_repay(self, api_manager, create_credit_user, create_credit_request):
        response = api_manager.user_steps.credit_repay_request(create_credit_user, create_credit_request)

        assert response.amountDeposited == 5000

    def test_credit_repay_with_invalid_amount(self, api_manager, create_credit_user, create_credit_request):
        repay_amounts = [4999, 5001]

        # Проверяем, что суммы пополнений, которые не равны сумме кредита, отклоняются.
        for invalid_amount in repay_amounts:
            create_credit_request.amount = invalid_amount
            response = api_manager.user_steps.invalid_credit_repay_request(create_credit_user, create_credit_request)

            assert response.status_code == 422

    def test_repay_closed_credit(self, api_manager, create_credit_user, create_credit_request):

        # Проверяем, что при повторном погашении кредита получаем ошибку.
            api_manager.user_steps.credit_repay_request(create_credit_user, create_credit_request)
            response = api_manager.user_steps.invalid_credit_repay_request(create_credit_user, create_credit_request)

            assert response.status_code == 422


