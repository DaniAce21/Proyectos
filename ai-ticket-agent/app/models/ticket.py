from sqlalchemy import Column, Integer, String

from app.database import Base


# Modelo Ticket
class Ticket(Base):

    # Nombre tabla
    __tablename__ = "tickets"


    # Columnas
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    description = Column(String)

    status = Column(String)

    ai_analysis = Column(String)