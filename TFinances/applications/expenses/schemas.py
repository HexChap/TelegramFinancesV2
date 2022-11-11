from pydantic import BaseModel, constr


class ExpenseSchema(BaseModel):
    price: float
    note: constr(max_length=64)
    category_id: int
    user_id: int
