from fastapi import APIRouter

from app.schemas.ticket_schema import TicketCreate

from app.services.ai_service import analyze_ticket

from app.database import SessionLocal

from app.models.ticket import Ticket


# Router FastAPI
router = APIRouter()


# =========================================
# GET /tickets
# Obtener todos los tickets
# =========================================
@router.get("/tickets")
def get_tickets():

    # Crear conexión DB
    db = SessionLocal()

    # Obtener tickets
    tickets = db.query(Ticket).all()

    # Retornar tickets
    return tickets


# =========================================
# POST /tickets
# Crear nuevo ticket
# =========================================
@router.post("/tickets")
def create_ticket(ticket: TicketCreate):

    # =====================================
    # Analizar ticket usando IA
    # =====================================
    ai_analysis = analyze_ticket(

        ticket.title,

        ticket.description
    )


    # =====================================
    # Crear conexión DB
    # =====================================
    db = SessionLocal()


    # =====================================
    # Crear nuevo ticket
    # =====================================
    new_ticket = Ticket(

        title=ticket.title,

        description=ticket.description,

        status="open",

        # Convertimos dict IA → texto
        ai_analysis=str(ai_analysis)
    )


    # =====================================
    # Guardar ticket en PostgreSQL
    # =====================================
    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)


    # =====================================
    # Respuesta API
    # =====================================
    return {

        "message": "Ticket created successfully",

        "ticket": {

            "id": new_ticket.id,

            "title": new_ticket.title,

            "description": new_ticket.description,

            "status": new_ticket.status,

            "ai_analysis": new_ticket.ai_analysis
        }
    }