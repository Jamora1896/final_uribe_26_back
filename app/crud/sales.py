from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.sale import Sale
from app.models.product import Product
from app.schemas import SaleCreate, SaleUpdate


def get_sales(db: Session, skip: int = 0, limit: int = 50, date_filter=None):
    q = db.query(Sale).options(
        joinedload(Sale.advisor),
        joinedload(Sale.local),
        joinedload(Sale.product),
    )
    if date_filter:
        q = q.filter(Sale.date == date_filter)
    return q.order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()


def get_sale(db: Session, sale_id: int):
    return (
        db.query(Sale)
        .options(
            joinedload(Sale.advisor),
            joinedload(Sale.local),
            joinedload(Sale.product),
        )
        .filter(Sale.id == sale_id)
        .first()
    )


def create_sale(db: Session, data: SaleCreate, user_id: int):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise ValueError("Producto no encontrado")
    sale = Sale(
        date=data.date,
        qty=data.qty,
        total=product.price * data.qty,
        user_id=user_id,
        advisor_id=data.advisor_id,
        local_id=data.local_id,
        product_id=data.product_id,
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return get_sale(db, sale.id)


def update_sale(db: Session, sale: Sale, data: SaleUpdate):
    for f, v in data.model_dump(exclude_none=True).items():
        setattr(sale, f, v)
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if product:
        sale.total = product.price * sale.qty
    db.commit()
    db.refresh(sale)
    return get_sale(db, sale.id)


def delete_sale(db: Session, sale: Sale):
    db.delete(sale)
    db.commit()


def get_dashboard_metrics(db: Session):
    today = date.today()
    today_sales = db.query(Sale).filter(Sale.date == today).all()
    top = (
        db.query(Sale.product_id, func.sum(Sale.qty).label("total_qty"))
        .group_by(Sale.product_id)
        .order_by(func.sum(Sale.qty).desc())
        .first()
    )
    top_product = None
    if top:
        p = db.query(Product).filter(Product.id == top.product_id).first()
        top_product = p.name if p else None
    return {
        "today_total": sum(s.total for s in today_sales),
        "today_count": len(today_sales),
        "top_product": top_product,
    }