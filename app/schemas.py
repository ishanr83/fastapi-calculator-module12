from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CalculationBase(BaseModel):
    operation: str
    operand_a: float
    operand_b: float
    user_id: int


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    operand_a: Optional[float] = None
    operand_b: Optional[float] = None


class CalculationRead(CalculationBase):
    id: int
    result: float
    created_at: datetime

    class Config:
        from_attributes = True
