from fastapi import APIRouter, HTTPException
from api.v1.services.expense_service import (
    get_expenses,
    get_expense_by_id,
    create_expense,
    update_expense,
    delete_expense,
)
from api.v1.schemas.Expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter(prefix="/expenses")


@router.post("/", status_code=201, response_model=ExpenseResponse)
async def create_expense_route(expense_data: ExpenseCreate):
    try:
        return await create_expense(expense_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating expense: {str(e)}")


@router.get("/", status_code=200, response_model=list[ExpenseResponse])
async def get_all_expenses_route():
    try:
        return await get_expenses()

    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Error retrieving expenses: {str(e)}"
        )


@router.get("/{expense_id}", status_code=200, response_model=ExpenseResponse)
async def get_expense_by_id_route(expense_id: str):
    try:
        return await get_expense_by_id(expense_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{str(e)}")


@router.put("/{expense_id}", status_code=201, response_model=ExpenseResponse)
async def update_expense_route(expense_id: str, expense_data: ExpenseUpdate):
    try:
        return await update_expense(expense_id, expense_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error editing expense: {str(e)}")


@router.delete("/{expense_id}", status_code=204)
async def delete_expense_route(expense_id: str):
    try:
        await delete_expense(expense_id)
        return {"message": "Expense deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting expense: {str(e)}")
