from django.contrib.gis.db import models
from geospatialbiodiversity import models as polygon_models
from django.contrib.postgres.fields import JSONField
from core import services

class Permit(models.Model):
    """
    A development should have one or more permits. These permits are generally issued by local or national authorities.
    E.g.: 'Environmental Impact Assessment', 'Department of Agriculture, Forestry and Fisheries Permit',
    'Water Use License Application', 'Department of Mineral Resources'
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Development(models.Model):
    """
    Developments are buildings or groups of buildings/constructions which are undertaken somewhere in South Africa.
    The permits are already obtained and the building is completed.
    """
    year = models.IntegerField(help_text="The year in which the development was completed.")
    permits = models.ManyToManyField(Permit, help_text="May be one of several, linked to the Permit model.")

    AGRICULTURE = 'AG'
    BUSINESS = 'BU'
    COMMERCIAL = 'CO'
    GOVERNMENT = 'GO'
    GOVERNMENT_PURPOSES = 'GP'
    INDUSTRIAL = 'IN'
    MINING = 'MI'
    MULTI_USE = 'MU'
    RECREATIONAL = 'RC'
    RESIDENTIAL = 'RE'
    TRANSPORT = 'TR'
    UNKNOWN = 'UN'
    TYPE_CHOICES = (
        (AGRICULTURE, 'Agriculture'),
        (BUSINESS, 'Business'),
        (COMMERCIAL, 'Commercial'),
        (GOVERNMENT, 'Government'),
        (GOVERNMENT_PURPOSES, 'Government purposes'),
        (INDUSTRIAL, 'Industrial'),
        (MINING, 'Mining'),
        (MULTI_USE, 'Multi-use (public, residential, commercial)'),
        (RECREATIONAL, 'Recreational'),
        (RESIDENTIAL, 'Residential'),
        (TRANSPORT, 'Transport'),
        (UNKNOWN, 'Unknown'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, help_text="Choose all types of development that form part of the application.")

    footprint = models.PolygonField(help_text="Should be a .geojson file.")

    geo_info = JSONField()
    info = JSONField()

    def get_info_fields(self):
        return ['applicant', 'application_title', 'activity_description', 'authority', 'case_officer', 'date_issued',
                'environmental_consultancy', 'environmental_assessment_practitioner', 'location', 'reference_no']

    def province(self):
        province = polygon_models.Area.objects.filter(type=polygon_models.Area.PROVINCE, polygon__contains=self.footprint).first()
        return str(province)

    def __str__(self):
        name = str(self.year) + ' ' + self.get_type_display()
        if 'province' in self.geo_info:
            name += ' ' + self.geo_info['province']
        return name

class OffsetImplementationTime(models.Model):
    """
    The offsets required by a development can be implemented over multiple time frames, such as:
    Before development, During development, After development - 6 months, After development - 12 months,
    After development - 24 months, After development - more than 24 months
    """
    name = models.CharField(max_length=50)

    def is_staggered(self):
        """If there's more than one implementation time, the implementation is considered to be 'staggered'."""
        return False

    def __str__(self):
        return self.name


class Offset(models.Model):
    """
    Developments might occur on a sensitive piece of land - e.g. a protected area. In which case, the development
    should be associated with one or several offsets. There are different types of offsets implemented over different
    periods, lasting for different durations.
    If an offset is of type hectares it should have an associated polygon.
    """
    development = models.ForeignKey(Development)
    polygon = models.PolygonField(null=True, blank=True)  # TODO change to multipolygon

    HECTARES = 'HE'
    RESEARCH = 'RE'
    REHAB = 'RH'
    FINANCIAL = 'FI'
    TYPE_CHOICES = (
        (HECTARES, 'Hectares'),
        (RESEARCH, 'Research'),
        (REHAB, 'Rehabilitation'),
        (FINANCIAL, 'Financial compensation')
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, null=True, blank=True)

    PERPETUITY = 'PE'
    UNSPECIFIED = 'US'
    UNKNOWN = 'UN'
    LOWER = 'LT'
    MIDRANGE = 'TF'
    LONG = 'HC'
    DURATION_CHOICES = (
        (PERPETUITY, 'Perpetuity'),
        (UNSPECIFIED, 'Unspecified'),
        (UNKNOWN, 'Unknown'),
        (LOWER, '< 20 years'),
        (MIDRANGE, 'Between 20 and 50 years'),
        (LONG, '> 50 years'),
    )
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES)

    info = JSONField()
    implementation_times = models.ManyToManyField(OffsetImplementationTime)
