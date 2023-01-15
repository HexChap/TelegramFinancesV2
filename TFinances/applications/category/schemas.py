from pydantic import BaseModel, constr


class CategorySchema(BaseModel):
    name: constr(max_length=16) | None
    description: constr(max_length=160) | None
    user_id: int | None
