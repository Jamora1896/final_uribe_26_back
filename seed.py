import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal, Base
from app.models import User, Advisor, Local, Product  # noqa: F401
from app.auth import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_users():
    users = [
        {"username": "admin", "password": "admin12345", "phone": "3001000001"},
        {"username": "demo",  "password": "demo12345",  "phone": "3001000002"},
    ]
    for u in users:
        if not db.query(User).filter(User.username == u["username"]).first():
            db.add(User(
                username=u["username"],
                hashed_password=hash_password(u["password"]),
                phone=u["phone"],
            ))
    db.commit()
    print("✅ Usuarios creados")


def seed_advisors():
    names = ["Carlos Rodríguez", "Ana Martínez", "Luis García", "María López"]
    for name in names:
        if not db.query(Advisor).filter(Advisor.name == name).first():
            db.add(Advisor(name=name))
    db.commit()
    print("✅ Asesores creados")


def seed_locals():
    locals_ = [
        {"name": "Local Centro",    "address": "Calle 10 #5-20, Medellín"},
        {"name": "Local El Poblado","address": "Av. El Poblado #15-30"},
        {"name": "Local Envigado",  "address": "Calle 40 Sur #45-10"},
    ]
    for l in locals_:
        if not db.query(Local).filter(Local.name == l["name"]).first():
            db.add(Local(name=l["name"], address=l["address"]))
    db.commit()
    print("✅ Locales creados")


def seed_products():
    products = [
        {"name": "Camiseta Básica",   "price": 45000,  "stock": 100},
        {"name": "Jean Slim Fit",     "price": 120000, "stock": 50},
        {"name": "Chaqueta de Cuero", "price": 250000, "stock": 20},
        {"name": "Vestido Floral",    "price": 89000,  "stock": 35},
        {"name": "Pantalón Casual",   "price": 75000,  "stock": 60},
        {"name": "Blusa Elegante",    "price": 65000,  "stock": 45},
        {"name": "Short Deportivo",   "price": 40000,  "stock": 80},
        {"name": "Sudadera Premium",  "price": 110000, "stock": 30},
    ]
    for p in products:
        if not db.query(Product).filter(Product.name == p["name"]).first():
            db.add(Product(name=p["name"], price=p["price"], stock=p["stock"]))
    db.commit()
    print("✅ Productos creados")


if __name__ == "__main__":
    seed_users()
    seed_advisors()
    seed_locals()
    seed_products()
    db.close()
    print("\n🎉 Seed completado. Ejecuta: uvicorn app.main:app --reload")