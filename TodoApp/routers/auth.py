from typing import Annotated, TypeAlias
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "facundo123",
                "email": "facundoenriquez@example.com",
                "first_name": "Facundo",
                "last_name": "Enriquez",
                "password": "test1234",
                "role": "admin"
            }
        }
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return {"error": "Incorrect username or password"}
    return 'success'
