from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_users(db)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    return crud.update_user(db, user, data)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    crud.delete_user(db, user)