from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from geospatialbiodiversity import models

class AreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Area
        geo_field = 'polygon'
        fields = ('date', 'name', 'type', 'identifier', 'polygon', 'url')