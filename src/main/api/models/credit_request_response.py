from src.main.api.models.base_model import BaseModel


class CreditRequestResponse(BaseModel):
    id: int
    amount: int
    termMonths: int
    balance: float
    creditId: int
