from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.advisor import Advisor
    from app.models.local import Local
    from app.models.product import Product


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(Integer, ForeignKey("advisors.id"), nullable=False)
    local_id: Mapped[int] = mapped_column(Integer, ForeignKey("locals.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sales")
    advisor: Mapped["Advisor"] = relationship("Advisor", back_populates="sales")
    local: Mapped["Local"] = relationship("Local", back_populates="sales")
    product: Mapped["Product"] = relationship("Product", back_populates="sale_items")