from api.v1.schemas.Expense import Expense, ExpenseResponse, ExpenseCreate, ExpenseUpdate
from core.db_connection import get_collection_db
from bson import ObjectId
from datetime import datetime

async def create_expense(expense_data: ExpenseCreate):
    try:
        collection = await get_collection_db("expenses")

        if expense_data.date is None :
            expense_data.date =  datetime.now().strftime("%d/%m/%Y")

        categories_collection = get_collection_db("categories")

        category = await categories_collection.find_one({"_id": ObjectId(expense_data.category)})

        if not category:
            raise Exception(f"Category '{expense_data.category}' not found.")

        expense = Expense(
            name=expense_data.name,
            amount=expense_data.amount,
            category=str(category["_id"]),
            date=expense_data.date,
            
        )

        new_expense = await collection.insert_one(expense.dict())

        expense_id = str(new_expense.inserted_id)

        return ExpenseResponse(id=expense_id, **expense.dict())

    except Exception as e:
        raise Exception(f"Error creating expense: {str(e)}")

async def get_expenses():
    try:
        collection = await get_collection_db("expenses")

        expenses = []
        async for document in collection.find():
            expense = ExpenseResponse(
                id=str(document["_id"]),
                name=document["name"],
                amount=document["amount"],
                category=document["category"],
                date=document["date"]
            )
            expenses.append(expense)
        
        return expenses

    except Exception as e:
        raise Exception(f"Error retrieving expenses: {str(e)}")

async def get_expense_by_id(expense_id: str):
    try:
        collection = await get_collection_db("expenses")
        
        expense = await collection.find_one({"_id": ObjectId(expense_id)})

        if expense:
            return ExpenseResponse(
                id=str(expense["_id"]),
                name=expense["name"],
                amount=expense["amount"],
                category=expense["category"],
                date=expense["date"]
            )
        else:
            raise Exception("Expense not found")

    except Exception as e:
        raise Exception(f"Error retrieving expense with the id: {expense_id}. {str(e)}")


async def update_expense(expense_id: str, expense_data: ExpenseUpdate):
    try:
        collection = await get_collection_db("expenses")

        categories_collection = get_collection_db("categories")

        category = await categories_collection.find_one({"_id": ObjectId(expense_data.category)})

        if category and expense_data.category is not str(category["_id"]):
            expense_data.category = str(category["_id"])
        elif not category:
            raise Exception(f"Category '{expense_data.category}' not found.")

        update_data = expense_data.dict()

        # Realizar la actualización
        update_result = await collection.update_one(
            {"_id": ObjectId(expense_id)},
            {"$set": update_data}
        )

        if update_result.modified_count == 1:
            # La actualización tuvo éxito, recuperar el gasto actualizado
            updated_expense = await collection.find_one({"_id": ObjectId(expense_id)})
            if updated_expense:
                return ExpenseResponse(id=str(updated_expense["_id"]), **updated_expense)
            else:
                raise Exception("Expense not found after update")
        else:
            raise Exception("Expense update failed")

    except Exception as e:
        raise Exception(f"Error editing expense with the id: {expense_id}. {str(e)}")
    

async def delete_expense(expense_id: str):
    try:
        collection = await get_collection_db("expenses")

        await collection.delete_one({"_id": ObjectId(expense_id)})

    except Exception as e:
        raise Exception(f"Error deleting expense with the id: {expense_id}. {str(e)}")