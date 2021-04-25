from sqlalchemy.orm import Session
from app.database import models, schemas

def get_player(db: Session, player_id: int):
    return db.query(models.Player).get(models.Player.id == player_id)

def get_players(db: Session):
    return db.query(models.Player).all()

def create_player(db: Session, player: schemas.PlayerBase):
    player_model = models.Player(first_name=player.first_name, last_name=player.last_name)
    db.add(player_model)
    db.commit()
    db.refresh(player_model)
    return player_model

def get_teams(db: Session, team_id: int):
    return db.query(models.Team).get(models.Team.id == team_id)