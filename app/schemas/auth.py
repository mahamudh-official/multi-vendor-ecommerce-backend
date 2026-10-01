from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone_number: str = Field(min_length=8, max_length=20)

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: str
    is_active: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str

class AccessToken(BaseModel):
    token: str