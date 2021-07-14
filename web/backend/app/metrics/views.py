import json

from metrics.models import Metric
from metrics.serializers import MetricsSerializer, RadarChartSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class RadarMetricsListEndpoint(generics.ListAPIView):
    queryset = Metric.objects.filter(metric_type="radar")
    serializer_class = MetricsSerializer


class RadarChartEndpoint(APIView):
    def get(self, request) -> Response:
        query_params = request.GET
        serializer = RadarChartSerializer(
            data={
                "player_id": int(query_params["player_id"]),
                "metrics_ids": query_params.getlist("metrics_ids"),
            }
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        player_id = validated_data["player_id"]
        metrics = validated_data["metrics_ids"]

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
