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
    names = ["Carlos Rodríguez", "Ana Cano", "Luis Correa", "María López","Juan Pérez", "Sofía Gómez", "Andrés Martínez", "Laura Sánchez"]
    for name in names:
        if not db.query(Advisor).filter(Advisor.name == name).first():
            db.add(Advisor(name=name))
    db.commit()
    print("✅ Asesores creados")


def seed_locals():
    locals_ = [
        {"name": "Rifle Centro",    "address": "Calle 10 #5-20, Medellín"},
        {"name": "Rifle El Poblado","address": "Av. El Poblado #15-30"},
        {"name": "Rifle Envigado",  "address": "Calle 40 Sur #45-10"},
        {"name": "Rifle Itagüí",    "address": "Av. Las Vegas #20-50"},
        {"name": "Rifle Bello",     "address": "Calle 50 #30-15"},
        {"name": "Rifle Laureles",  "address": "Av. Nutibara #10-25"},
        {"name": "Rifle Sabaneta",  "address": "Calle 70 Sur #20-40"},
        {"name": "Rifle Guayabal",  "address": "Av. Guayabal #5-60"},
    ]
    for l in locals_:
        if not db.query(Local).filter(Local.name == l["name"]).first():
            db.add(Local(name=l["name"], address=l["address"]))
    db.commit()
    print("✅ Locales creados")


def seed_products():
    products = [
        {"name": "Camiseta texturizada con tejido trenzado","price": 159900,  "stock": 100},
        {"name": "Jean Wide Leg tono claro","price": 199900, "stock": 50},
        {"name": "Chaqueta acolchada de cuello alto","price": 339900, "stock": 20},
        {"name": "Vestido largo manga sisa con abertura","price": 169900,  "stock": 35},
        {"name": "Pantalón en tejido plano con estampado","price": 169900,  "stock": 60},
        {"name": "Camisa manga larga con bordado", "price": 159900,  "stock": 45},
        {"name": "Bermuda tiro medio en denim", "price": 169900,  "stock": 80},
        {"name": "Pantalón Jogger con pretina","price": 119900, "stock": 30},
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