from http import HTTPStatus
import requests
from requests import Response
from src.main.api.models.credit_request_model import CreditRequestModel
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.requests.requester import Requester


class CreditRequester(Requester):
    def post(self, credit_request_model: CreditRequestModel) -> CreditRequestResponse | Response:
        url = f'{self.base_url}/credit/request'
        response = requests.post(
            url=url,
            json=credit_request_model.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return CreditRequestResponse(**response.json())
        return response