from django.db import models


class NetworkConnectivity(models.Model):

    class Meta:
        db_table = 'network_connectivity'
        unique_together = (('node_from', 'node_to'))
        indexes = [
            models.Index(fields=['node_from']),
            models.Index(fields=['node_to']),
        ]

    node_from = models.IntegerField()
    node_to = models.IntegerField()
