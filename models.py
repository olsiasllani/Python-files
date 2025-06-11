from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=18, le=99)

    class Config:
        str_strip_whitespace = True  # përputhet me Pydantic v2
