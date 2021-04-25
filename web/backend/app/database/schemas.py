from pydantic import BaseModel

class PlayerBase(BaseModel):
    first_name: str
    last_name: str

class Player(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    name: str


class Team(TeamBase):
    id: int
    class Config:
        orm_mode = True