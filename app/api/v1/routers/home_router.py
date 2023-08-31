from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/", status_code=200)
def home():
    try:
        return "¡Bienvenido a la api de gastos!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")