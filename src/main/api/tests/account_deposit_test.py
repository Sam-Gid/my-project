import pytest


class TestDepositAccount:
    def test_valid_deposit_account(self, api_manager, create_user_request, account_deposit_request):
        response = api_manager.user_steps.account_deposit_request(create_user_request, account_deposit_request)
        assert response.balance == 5000


    @pytest.mark.parametrize(
        "deposit_amount",
        [999, 9001]
    )
    def test_deposit_account_with_invalid_amount(self, api_manager, create_user_request, account_deposit_request, deposit_amount):
        # Проверяем, что суммы пополнения ниже минимума и выше максимума отклоняются.
        account_deposit_request.amount = deposit_amount
        response = api_manager.user_steps.account_invalid_deposit_request(create_user_request, account_deposit_request)
        assert response.status_code == 400
