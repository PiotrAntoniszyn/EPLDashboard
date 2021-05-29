from metrics.fields import DEFAULT_RADAR_METRICS
from rest_framework import serializers
from teams.models import Player


class RadarChartSerializer(serializers.Serializer):

    player_id = serializers.IntegerField()
    metrics = serializers.ListField(child=serializers.CharField(), allow_null=True)

    def validate_player_id(self, player_id):
        if not Player.objects.filter(id=player_id).exists():
            raise serializers.ValidationError(
                f"Player with id={player_id} does not exist"
            )
        return player_id

    def validate_metrics(self, metrics):
        if not metrics:
            return DEFAULT_RADAR_METRICS

        for metric in metrics:
            if metric not in DEFAULT_RADAR_METRICS:
                raise serializers.ValidationError(
                    f"{metric} is not a valid metric name"
                )
        return metrics
