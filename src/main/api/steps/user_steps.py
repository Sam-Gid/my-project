from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response


    def account_deposit_request(self, create_user_request: CreateUserRequest, create_account_request):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(create_account_request)
        return response


    def account_invalid_deposit_request(self, create_user_request: CreateUserRequest, create_account_request):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(create_account_request)
        return response


    def transfer_funds_request(
            self, create_user_request: CreateUserRequest,
            transfer_funds_request: TransferFundsRequest
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_FUNDS,
            ResponseSpecs.request_ok()
    ).post(transfer_funds_request)
        return response


    def invalid_transfer_funds_request(
            self, create_user_request: CreateUserRequest,
            transfer_funds_request: TransferFundsRequest
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_FUNDS,
            ResponseSpecs.request_bad()
    ).post(transfer_funds_request)
        return response


    def valid_credit_request(
            self, create_user_request: CreateUserRequest,
            credit_request_model: CreditRequestModel
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request_model)
        return response


    def invalid_role_credit_request(
            self, create_user_request: CreateUserRequest,
            credit_request_model: CreditRequestModel
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden()
        ).post(credit_request_model)
        return response


    def invalid_amount_credit_request(
            self, create_user_request: CreateUserRequest,
            credit_request_model: CreditRequestModel
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(credit_request_model)
        return response


    def credit_repay_request(
            self,
            create_user_request: CreateUserRequest,
            credit_repay_request: CreditRepayRequest
    ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response


    def invalid_credit_repay_request(
        self,
        create_user_request: CreateUserRequest,
        credit_repay_request: CreditRepayRequest
    ):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)
        return response


