from django.db import models


class Metric(models.base.Model):

    METRIC_TYPES = [("radar", "Radar Chart Metrics")]

    internal_name = models.CharField(max_length=256)
    display_name = models.CharField(max_length=256)
    metric_type = models.CharField(max_length=256, choices=METRIC_TYPES)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.display_name} [{self.metric_type}]"
