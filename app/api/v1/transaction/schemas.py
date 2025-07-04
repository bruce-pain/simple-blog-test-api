from pydantic import BaseModel, EmailStr
from enum import Enum
from app.core.base.schema import BaseResponseModel

# Transaction type enum
class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

# Transaction data model
class TransactionData(BaseModel):
    id: str
    email: EmailStr
    amount: float
    type: TransactionType
    created_at: str
    updated_at: str

# Request model for creating a new transaction
class CreateTransactionRequest(BaseModel):
    email: EmailStr
    amount: float
    type: TransactionType

# Response model for a single transaction
class TransactionResponse(BaseResponseModel):
    data: TransactionData

# Response model for creating a new transaction
class CreateTransactionResponse(BaseResponseModel):
    data: TransactionData