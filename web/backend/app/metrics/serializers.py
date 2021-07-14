from metrics.fields import DEFAULT_RADAR_METRICS
from metrics.models import Metric
from rest_framework import serializers
from teams.models import Player


class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ["id", "display_name"]


class RadarChartSerializer(serializers.Serializer):

    player_id = serializers.IntegerField()
    metrics_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_null=True
    )

    def validate_player_id(self, player_id):
        if not Player.objects.filter(id=player_id).exists():
            raise serializers.ValidationError(
                f"Player with id={player_id} does not exist"
            )
        return player_id

    def validate_metrics_ids(self, metrics_ids):
        qs = Metric.objects.filter(metric_type="radar")
        if metrics_ids:
            qs.filter(id__in=metrics_ids)

        return qs.values_list("internal_name", flat=True)
