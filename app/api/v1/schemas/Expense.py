from pydantic import BaseModel
from typing import Optional

class Expense(BaseModel):
    name: str
    amount: float
    category: str
    date: str

class ExpenseCreate(BaseModel):
    name: str
    amount: float
    category: str
    date: Optional[str] = None

class ExpenseUpdate(BaseModel):
    name: str
    amount: float
    category: str
    date: Optional[str]

class ExpenseResponse(BaseModel):
    id: str
    name: str
    amount: float
    category: str
    date: str
    
