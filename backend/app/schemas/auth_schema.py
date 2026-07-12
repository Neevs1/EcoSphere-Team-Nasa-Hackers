from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department_id: int | None = None
    points_balance: int = 0
    xp_total: int = 0

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"
    department_id: int | None = None
    status: bool = True

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
    department_id: int | None = None
    status: bool | None = None
