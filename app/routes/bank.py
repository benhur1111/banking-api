from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas import UserCreate, Transaction, AccountCreate, AccountResponse, TransactionRequest, TransactionRecord, TransactionHistory

router = APIRouter(prefix="/bank")

# In-memory storage for accounts
accounts = {}
account_counter = 0

# In-memory storage for transactions
transactions = {}  # account_id -> list of transactions
transaction_counter = 0

@router.post("/accounts", response_model=AccountResponse)
def create_account(account: AccountCreate):
    """Create a new bank account with initial balance."""
    global account_counter
    account_counter += 1
    
    account_id = account_counter
    accounts[account_id] = {
        "account_id": account_id,
        "customer_name": account.customer_name,
        "balance": account.initial_balance
    }
    
    return accounts[account_id]

@router.post("/accounts/{account_id}/deposit", response_model=AccountResponse)
def deposit_account(account_id: int, txn: TransactionRequest):
    """Deposit funds to an account."""
    global transaction_counter
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transaction_counter += 1
    accounts[account_id]["balance"] += txn.amount
    
    # Record transaction
    if account_id not in transactions:
        transactions[account_id] = []
    
    transactions[account_id].append({
        "transaction_id": transaction_counter,
        "account_id": account_id,
        "type": "deposit",
        "amount": txn.amount,
        "timestamp": datetime.now()
    })
    
    return accounts[account_id]

@router.post("/accounts/{account_id}/withdraw", response_model=AccountResponse)
def withdraw_account(account_id: int, txn: TransactionRequest):
    """Withdraw funds from an account."""
    global transaction_counter
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if accounts[account_id]["balance"] < txn.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    transaction_counter += 1
    accounts[account_id]["balance"] -= txn.amount
    
    # Record transaction
    if account_id not in transactions:
        transactions[account_id] = []
    
    transactions[account_id].append({
        "transaction_id": transaction_counter,
        "account_id": account_id,
        "type": "withdrawal",
        "amount": txn.amount,
        "timestamp": datetime.now()
    })
    
    return accounts[account_id]

@router.get("/accounts/{account_id}/history", response_model=TransactionHistory)
def get_transaction_history(account_id: int):
    """Fetch transaction history for an account."""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_transactions = transactions.get(account_id, [])
    return {
        "account_id": account_id,
        "customer_name": accounts[account_id]["customer_name"],
        "transactions": account_transactions
    }

users = {}

@router.post("/users")
def create_user(user: UserCreate):
    user_id = len(users) + 1
    users[user_id] = {"name": user.name, "balance": 0}
    return {"user_id": user_id}

@router.post("/deposit/{user_id}")
def deposit(user_id: int, txn: Transaction):
    if user_id not in users:
        raise HTTPException(404, "User not found")
    users[user_id]["balance"] += txn.amount
    return users[user_id]