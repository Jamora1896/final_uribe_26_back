from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator


# ── TOKEN ──────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str


# ── USER ───────────────────────────────────────────
class UserCreate(BaseModel):
    username: str
    password: str
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Mínimo 8 caracteres")
        return v


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    username: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}


# ── ADVISOR ────────────────────────────────────────
class AdvisorCreate(BaseModel):
    name: str


class AdvisorUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class AdvisorOut(BaseModel):
    id: int
    name: str
    is_active: bool
    model_config = {"from_attributes": True}


# ── LOCAL ──────────────────────────────────────────
class LocalCreate(BaseModel):
    name: str
    address: Optional[str] = None


class LocalUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class LocalOut(BaseModel):
    id: int
    name: str
    address: Optional[str]
    is_active: bool
    model_config = {"from_attributes": True}


# ── PRODUCT ────────────────────────────────────────
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0

    @field_validator("price")
    @classmethod
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    is_active: bool
    model_config = {"from_attributes": True}


# ── SALE ───────────────────────────────────────────
class SaleCreate(BaseModel):
    date: date
    advisor_id: int
    local_id: int
    product_id: int
    qty: int

    @field_validator("qty")
    @classmethod
    def qty_positive(cls, v):
        if v < 1:
            raise ValueError("La cantidad debe ser al menos 1")
        return v


class SaleUpdate(BaseModel):
    date: Optional[date] = None
    advisor_id: Optional[int] = None
    local_id: Optional[int] = None
    product_id: Optional[int] = None
    qty: Optional[int] = None


class SaleOut(BaseModel):
    id: int
    date: date
    qty: int
    total: float
    created_at: datetime
    user_id: int
    advisor: AdvisorOut
    local: LocalOut
    product: ProductOut
    model_config = {"from_attributes": True}


# ── DASHBOARD ──────────────────────────────────────
class DashboardMetrics(BaseModel):
    today_total: float
    today_count: int
    top_product: Optional[str]