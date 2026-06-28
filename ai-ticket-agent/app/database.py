from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# URL conexión PostgreSQL
DATABASE_URL = "postgresql://postgres:12345@localhost/ai_ticket_agent"


# Engine conexión
engine = create_engine(DATABASE_URL)


# Sesiones DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base modelos
Base = declarative_base()