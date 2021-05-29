import json

from metrics.fields import DEFAULT_RADAR_METRICS
from metrics.serializers import RadarChartSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view(["GET"])
def get_radar_metrics(_):
    return Response([{"value": met, "label": met} for met in DEFAULT_RADAR_METRICS])


class RadarChartEndpoint(APIView):
    def get(self, request) -> Response:
        serializer = RadarChartSerializer(
            data={
                "player_id": int(request.GET["player_id"]),
                "metrics": request.GET.getlist("metrics", []),
            }
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        player_id = validated_data["player_id"]
        metrics = validated_data["metrics"]

        with open("app/metrics/fixtures/radar_chelsea.json", "r") as f:
            data = json.loads(f.read())

        try:
            player_data = data[player_id]
        except IndexError:
            return Response(status_code=404, detail="Player not found")

        player_name = player_data["Player"].split("\\")[0]
        try:
            player_metrics = [player_data[column] for column in metrics]
        except KeyError:
            return Response(status_code=404, detail="Invalid metric requested")

        return Response(
            {"metrics": player_metrics, "name": player_name, "labels": metrics}
        )
