from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.auth import create_access_token
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, data.username):
        raise HTTPException(400, "El usuario ya existe")
    return crud.create_user(db, data)


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    return {
        "access_token": create_access_token({"sub": user.username}),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user