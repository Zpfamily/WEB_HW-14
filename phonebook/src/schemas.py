from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(default="", examples=["Borys", "Nadiia"], min_length=1, max_length=25, title="Ім'я")
    last_name: str = Field(default="", examples=["Kuchyn", "Volkova"], min_length=1, max_length=25, title="Прізвище")
    email: EmailStr
    phone: str | None = Field(
        None, examples=["+380 53 123-4567", "+380 (53) 1234567", "+380531234567"], max_length=25, title="Номер телефону"
    )
    birthday: date | None = None
    comments: str | None = Field(default=None, title="Додаткові дані")
    favorite: bool = False

class ContactFavoriteModel(BaseModel):
    favorite: bool = False

class ContactResponse(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    phone: str | None
    birthday: date | None
    comments: str | None
    favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
        
#new
        
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)
    
class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str | None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RequestEmail(BaseModel):
    email: EmailStr


  