from fastapi import FastAPI

from app.database import engine
from app.database import Base

from app.routes.ticket import router as tickets_router


# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)


# App FastAPI
app = FastAPI()


# Registrar rutas
app.include_router(tickets_router)


@app.get("/")
def root():

    return {
        "message": "AI Ticket Agent Running"
    }