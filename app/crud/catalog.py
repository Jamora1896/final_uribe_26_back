from sqlalchemy.orm import Session

from app.models.advisor import Advisor
from app.models.local import Local
from app.models.product import Product
from app.schemas import (
    AdvisorCreate, AdvisorUpdate,
    LocalCreate, LocalUpdate,
    ProductCreate, ProductUpdate,
)


# ── ADVISORS ──────────────────────────────────────
def get_advisors(db: Session, active_only: bool = True):
    q = db.query(Advisor)
    return q.filter(Advisor.is_active == True).all() if active_only else q.all()


def get_advisor(db: Session, advisor_id: int):
    return db.query(Advisor).filter(Advisor.id == advisor_id).first()


def create_advisor(db: Session, data: AdvisorCreate):
    obj = Advisor(name=data.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_advisor(db: Session, advisor: Advisor, data: AdvisorUpdate):
    for f, v in data.model_dump(exclude_none=True).items():
        setattr(advisor, f, v)
    db.commit()
    db.refresh(advisor)
    return advisor


def delete_advisor(db: Session, advisor: Advisor):
    db.delete(advisor)
    db.commit()


# ── LOCALS ────────────────────────────────────────
def get_locals(db: Session, active_only: bool = True):
    q = db.query(Local)
    return q.filter(Local.is_active == True).all() if active_only else q.all()


def get_local(db: Session, local_id: int):
    return db.query(Local).filter(Local.id == local_id).first()


def create_local(db: Session, data: LocalCreate):
    obj = Local(name=data.name, address=data.address)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_local(db: Session, local: Local, data: LocalUpdate):
    for f, v in data.model_dump(exclude_none=True).items():
        setattr(local, f, v)
    db.commit()
    db.refresh(local)
    return local


def delete_local(db: Session, local: Local):
    db.delete(local)
    db.commit()


# ── PRODUCTS ──────────────────────────────────────
def get_products(db: Session, active_only: bool = True):
    q = db.query(Product)
    return q.filter(Product.is_active == True).all() if active_only else q.all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, data: ProductCreate):
    obj = Product(name=data.name, price=data.price, stock=data.stock)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_product(db: Session, product: Product, data: ProductUpdate):
    for f, v in data.model_dump(exclude_none=True).items():
        setattr(product, f, v)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()