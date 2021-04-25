from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.crud import get_players
from app.database.connection import get_db

router = APIRouter()


@router.get("/metrics/player")
def get_player(db: Session = Depends(get_db)):
    players = get_players(db)
    return [{"value": player.id, "label": f"{player.first_name} {player.last_name}"} for player in players]
