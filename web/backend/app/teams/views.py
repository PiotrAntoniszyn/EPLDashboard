from rest_framework.response import Response
from rest_framework.decorators import api_view

from teams.serializers import PlayerSerializer
from teams.models import Player

@api_view(["GET"])
def get_players(request):

    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(
        [
            {"value": p["id"], "label": f"{p['first_name']} {p['last_name']}"}
            for p in serializer.data
        ]
    )