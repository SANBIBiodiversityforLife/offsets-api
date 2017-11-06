from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from core import models
from django.db.models import Count
from core import serializers


class DevelopmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.Development.objects.all()
    serializer_class = serializers.DevelopmentSerializer


class DevelopmentGeoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.Development.objects.all()
    serializer_class = serializers.DevelopmentGeoSerializer


class PermitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.Permit.objects.all()
    serializer_class = serializers.PermitSerializer


class PermitNameViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.PermitName.objects.all()
    serializer_class = serializers.PermitNameSerializer


class ImplementationTimeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = models.OffsetImplementationTime.objects.all()
    serializer_class = serializers.ImplementationTimeSerializer


class OffsetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    metadata_class = serializers.GeoMetadata
    queryset = models.Offset.objects.all()
    serializer_class = serializers.OffsetSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned offsets to a given development
        """
        queryset = models.Offset.objects.filter(type=models.Offset.HECTARES)
        development = self.request.query_params.get('development', None)
        if development is not None:
            queryset = queryset.filter(development__id=development)
        return queryset


class Statistics(viewsets.ViewSet):
    """
    View to get some statistics from the database
    """
    def list(self, request, format=None):
        """
        Return the number of permits each authority has issued
        """
        permits = []
        for permit in models.Permit.objects.all():
            development_count = models.Development.objects.filter(permits=permit).count()
            permits.append({'label': permit.name, 'value': development_count})

        years = models.Permit.objects.all().values('date_issued').annotate(total=Count('date_issued')).order_by('total')
        returned_years = []
        for year in years:
            returned_years.append({'label': year['date_issued'], 'value': year['total']})

        veg_types_dev = models.Development.objects.all().values('geo_info')
        all_vg = {}
        for vgd in veg_types_dev:
            vgd = vgd['geo_info']
            for key, item in vgd.items():
                if key in all_vg:
                    all_vg[key] += 1
                else:
                    all_vg[key] = 1
        # all_vg = sorted(all_vg)
        returned_vg = []

        for key, item in all_vg.items():
            returned_vg.append({'label': key, 'value': item})


        response = {'Number of developments per permit': {'data': sorted(permits, key=lambda k: k['label']),
                                                          'x_axis': 'Permits',
                                                          'y_axis': 'Number of developments',
                                                          'wide_graph': False},
                    'Number of permits per year': {'data': sorted(returned_years, key=lambda k: k['label']),
                                                        'x_axis': 'Years',
                                                        'y_axis': 'Number of developments',
                                                        'wide_graph': False},
                    'Number of vegetation types (developments)': {'data': sorted(returned_vg, key=lambda k: k['label']),
                                                                  'x_axis': 'Vegetation types',
                                                                  'y_axis': 'Number of developments',
                                                                  'wide_graph': True}}
        return Response(response)
