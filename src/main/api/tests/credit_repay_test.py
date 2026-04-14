import pytest


class TestCreditRepay:
    def test_credit_repay(self, api_manager, create_credit_user_request, credit_repay_request):
        response = api_manager.user_steps.credit_repay_request(create_credit_user_request, credit_repay_request)
        assert response.amountDeposited == 5000


    @pytest.mark.parametrize(
        'repay_amount',
        [4999, 5001]
    )
    def test_credit_repay_with_invalid_amount(self, api_manager, create_credit_user_request, credit_repay_request, repay_amount):
        # Проверяем, что суммы пополнений, которые не равны сумме кредита, отклоняются.
        credit_repay_request.amount = repay_amount
        response = api_manager.user_steps.invalid_credit_repay_request(create_credit_user_request, credit_repay_request)
        assert response.status_code == 422


    def test_repay_closed_credit(self, api_manager, create_credit_user_request, credit_repay_request):
        # Проверяем, что при повторном погашении кредита получаем ошибку.
            api_manager.user_steps.credit_repay_request(create_credit_user_request, credit_repay_request)
            response = api_manager.user_steps.invalid_credit_repay_request(create_credit_user_request, credit_repay_request)
            assert response.status_code == 422


