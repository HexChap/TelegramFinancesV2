from pydantic import BaseModel, constr


class CategorySchema(BaseModel):
    name: constr(max_length=16)
    description: constr(max_length=160)
    user_id: int | None
