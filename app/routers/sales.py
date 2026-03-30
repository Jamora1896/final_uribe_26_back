from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import DashboardMetrics, SaleCreate, SaleOut, SaleUpdate

router = APIRouter(tags=["Sales"])


@router.get("/dashboard", response_model=DashboardMetrics)
def dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return crud.get_dashboard_metrics(db)


@router.get("/sales", response_model=list[SaleOut])
def list_sales(
    skip: int = 0,
    limit: int = 50,
    date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return crud.get_sales(db, skip=skip, limit=limit, date_filter=date)


@router.post("/sales", response_model=SaleOut, status_code=201)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return crud.create_sale(db, data, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/sales/{sale_id}", response_model=SaleOut)
def get_sale(sale_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_sale(db, sale_id)
    if not obj:
        raise HTTPException(404, "Venta no encontrada")
    return obj


@router.patch("/sales/{sale_id}", response_model=SaleOut)
def update_sale(
    sale_id: int,
    data: SaleUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = crud.get_sale(db, sale_id)
    if not obj:
        raise HTTPException(404, "Venta no encontrada")
    return crud.update_sale(db, obj, data)


@router.delete("/sales/{sale_id}", status_code=204)
def delete_sale(sale_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = crud.get_sale(db, sale_id)
    if not obj:
        raise HTTPException(404, "Venta no encontrada")
    crud.delete_sale(db, obj)