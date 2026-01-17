from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    customer_name: str
    initial_balance: float = Field(ge=0, description="Initial balance must be >= 0")

class AccountResponse(BaseModel):
    account_id: int
    customer_name: str
    balance: float

class TransactionRequest(BaseModel):
    amount: float = Field(gt=0, description="Amount must be > 0")

class TransactionRecord(BaseModel):
    transaction_id: int
    account_id: int
    type: str
    amount: float
    timestamp: datetime

class TransactionHistory(BaseModel):
    account_id: int
    customer_name: str
    transactions: list[TransactionRecord]

class UserCreate(BaseModel):
    name: str

class Transaction(BaseModel):
    amount: int