from src.main.api.models.base_model import BaseModel


class TransferFundsRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float