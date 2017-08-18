from rest_framework import viewsets
from geospatialbiodiversity import models
from geospatialbiodiversity import serializers


class AreaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = models.Area.objects.all()
    serializer_class = serializers.AreaSerializer


