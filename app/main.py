from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import User, Advisor, Local, Product, Sale  # noqa: F401
from app.routers import auth, users, catalog, sales

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RIFLE - API de Gestión de Ventas",
    description="Backend para la tienda de ropa RIFLE.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(catalog.router)
app.include_router(sales.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "RIFLE API",
        "version": "1.0.0",
        "docs": "/docs",
    }