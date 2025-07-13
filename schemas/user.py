from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=127)


class UserCreate(UserBase):
    name: str = Field(min_length=3, max_length=75)


class UserLogin(UserBase):
    pass