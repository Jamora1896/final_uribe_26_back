from sqlalchemy.orm import Session

from app.auth import hash_password, verify_password
from app.models.user import User
from app.schemas import UserCreate, UserUpdate


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, data: UserCreate):
    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate):
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user