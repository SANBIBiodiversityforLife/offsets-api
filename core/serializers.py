from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from core import models
from rest_framework.metadata import SimpleMetadata

from collections import OrderedDict
from django.utils.encoding import force_text
from rest_framework import serializers
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework_gis.fields import GeometryField


class PermitNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PermitName
        fields = ('id', 'url', 'name', 'authority')


class BiodiversityLossSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BiodiversityLoss
        fields = ('id', 'url', 'type','name', 'size', 'development')


class BiodiversityGainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BiodiversityGain
        fields = ('id', 'url', 'type','name', 'size', 'offset')


class PermitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Permit
        fields = ('id', 'url', 'permit_name','development', 'case_officer', 'date_issued', 'reference_no')


class GeoMetadata(SimpleMetadata):
    """Overriding the SimpleMetadata DRF to add geometryfield for metadata options"""
    label_lookup = ClassLookupDict({
        serializers.Field: 'field',
        serializers.BooleanField: 'boolean',
        serializers.NullBooleanField: 'boolean',
        serializers.CharField: 'string',
        serializers.URLField: 'url',
        serializers.EmailField: 'email',
        serializers.RegexField: 'regex',
        serializers.SlugField: 'slug',
        serializers.IntegerField: 'integer',
        serializers.FloatField: 'float',
        serializers.DecimalField: 'decimal',
        serializers.DateField: 'date',
        serializers.DateTimeField: 'datetime',
        serializers.TimeField: 'time',
        serializers.ChoiceField: 'choice',
        serializers.MultipleChoiceField: 'multiple choice',
        serializers.FileField: 'file upload',
        serializers.ImageField: 'image upload',
        serializers.ListField: 'list',
        serializers.DictField: 'nested object',
        serializers.Serializer: 'nested object',
        GeometryField: 'geojson',
        serializers.ManyRelatedField: 'foreign key - multi',
        serializers.JSONField: 'json',
        PermitSerializer: 'foreign key - multi'
    })

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = super(GeoMetadata, self).get_field_info(field)
        field_info['field'] = str(field)

        # Override the DRF standard metadata with some additional stuff for FKs
        #if 'child' in field_info:
        #    label = field_info['label']
        #    field_info = field_info['child']
        #    field_info['label'] = label
        #    field_info['endpoint'] = str(label).lower()
        if field_info['type'] == 'foreign key - multi':
            field_info['endpoint'] = str(field_info['label']).lower().replace(' ', '-')
        #    import pdb; pdb.set_trace()
            # Note that we must make sure the url prefixes put into the router in urls.py follow this convention
            #field_info['endpoint'] = str(field.child_relation.queryset.model.__name__).lower() + 's'

        return field_info


class DevelopmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Development
        fields = ('id', 'url',  'use', 'get_use_display', 'location_description', 'code')


class DevelopmentGeoSerializer(GeoFeatureModelSerializer):
    #geo_info = serializers.JSONField()

    class Meta:
        model = models.Development
        geo_field = 'footprint'
        fields = ('id', 'url',  'use', 'get_use_display', 'location_description', 'code')


class ImplementationTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.OffsetImplementationTime
        fields = ('id', 'name', 'url')


class OffsetGeoSerializer(GeoFeatureModelSerializer):
    info = serializers.JSONField()

    class Meta:
        model = models.Offset
        geo_field = 'polygon'
        fields = ('id', 'url', 'permit', 'type', 'get_type_display', 'duration', 'implementation_times', 'info')


class OffsetSerializer(serializers.HyperlinkedModelSerializer):
    info = serializers.JSONField()

    class Meta:
        model = models.Offset
        fields = ('id', 'url', 'permit', 'type', 'get_type_display', 'duration', 'implementation_times', 'info')
