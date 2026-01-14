from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, Transaction

router = APIRouter(prefix="/bank")

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