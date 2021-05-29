from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from teams.models import Player
from teams.serializers import PlayerSerializer


@api_view(["GET"])
def get_players(_):

    players: QuerySet = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(
        [
            {"value": p["id"], "label": f"{p['first_name']} {p['last_name']}"}
            for p in serializer.data
        ]
    )


@api_view(["GET"])
def get_player_by_id(_, player_id):

    try:
        player: Player = Player.objects.get(id=player_id)
    except ObjectDoesNotExist:
        return Response(
            {"player_id": [{f"Cannot find player with id {player_id}"}]},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "score": player.score,
            "age": player.age,
            "team_name": player.team.name,
        }
    )
