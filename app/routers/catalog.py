from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import (
    AdvisorCreate, AdvisorOut, AdvisorUpdate,
    LocalCreate, LocalOut, LocalUpdate,
    ProductCreate, ProductOut, ProductUpdate,
)

router = APIRouter(tags=["Catalog"])


# ── ADVISORS ──────────────────────────────────────
@router.get("/advisors", response_model=list[AdvisorOut])
def list_advisors(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_advisors(db)


@router.post("/advisors", response_model=AdvisorOut, status_code=201)
def create_advisor(data: AdvisorCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.create_advisor(db, data)


@router.patch("/advisors/{advisor_id}", response_model=AdvisorOut)
def update_advisor(advisor_id: int, data: AdvisorUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_advisor(db, advisor_id)
    if not obj:
        raise HTTPException(404, "Asesor no encontrado")
    return crud.update_advisor(db, obj, data)


@router.delete("/advisors/{advisor_id}", status_code=204)
def delete_advisor(advisor_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_advisor(db, advisor_id)
    if not obj:
        raise HTTPException(404, "Asesor no encontrado")
    crud.delete_advisor(db, obj)


# ── LOCALS ────────────────────────────────────────
@router.get("/locals", response_model=list[LocalOut])
def list_locals(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_locals(db)


@router.post("/locals", response_model=LocalOut, status_code=201)
def create_local(data: LocalCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.create_local(db, data)


@router.patch("/locals/{local_id}", response_model=LocalOut)
def update_local(local_id: int, data: LocalUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_local(db, local_id)
    if not obj:
        raise HTTPException(404, "Local no encontrado")
    return crud.update_local(db, obj, data)


@router.delete("/locals/{local_id}", status_code=204)
def delete_local(local_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_local(db, local_id)
    if not obj:
        raise HTTPException(404, "Local no encontrado")
    crud.delete_local(db, obj)


# ── PRODUCTS ──────────────────────────────────────
@router.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_products(db)


@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.create_product(db, data)


@router.patch("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_product(db, product_id)
    if not obj:
        raise HTTPException(404, "Producto no encontrado")
    return crud.update_product(db, obj, data)


@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_product(db, product_id)
    if not obj:
        raise HTTPException(404, "Producto no encontrado")
    crud.delete_product(db, obj)