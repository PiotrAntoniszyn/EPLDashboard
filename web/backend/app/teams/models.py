from django.db import models
from django.db.models.deletion import DO_NOTHING


class Team(models.base.Model):
    name = models.CharField(max_length=120)

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return f"{self.name}"


class Player(models.base.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    age = models.IntegerField()
    position = models.CharField(max_length=20)
    nationality = models.CharField(max_length=120)
    team = models.ForeignKey(
        Team, on_delete=DO_NOTHING, null=True, related_name="players"
    )
    score = models.IntegerField(default=0)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} [{self.team}]"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} [{self.team}]"
