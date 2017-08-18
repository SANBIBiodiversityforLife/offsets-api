from rest_framework import viewsets
from rest_framework.decorators import detail_route
from core import models
from core import serializers


class DevelopmentViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.Development.objects.all()
    serializer_class = serializers.DevelopmentSerializer


class PermitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.Permit.objects.all()
    serializer_class = serializers.PermitSerializer


class OffsetImplementationTimeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = models.OffsetImplementationTime.objects.all()
    serializer_class = serializers.OffsetImplementationTimeSerializer


class OffsetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = models.Offset.objects.all()
    serializer_class = serializers.OffsetSerializer
