# common/schema.py
from pydantic import BaseModel

class OrderMessage(BaseModel):
    id: str
    description: str