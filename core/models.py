from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from core import services


class PermitName(models.Model):
    """
    Local or national authorities issue permits of different types. The Department of Mineral Resources, for example
    issues 3 diferent types of permits.
    Other egs: 'Environmental Impact Assessment', 'Department of Agriculture, Forestry and Fisheries Permit',
    'Water Use License Application', 'Department of Mineral Resources'
    """
    name = models.CharField(max_length=100, help_text="E.g. Department of Water Affairs.")
    authority = models.CharField(max_length=100, help_text="E.g. Water Use License (WULA).")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'authority')


class Development(models.Model):
    """
    Developments are buildings or groups of buildings/constructions which are undertaken somewhere in South Africa.
    The permits are already obtained and the building is completed.
    """
    permits = models.ManyToManyField(PermitName, through='Permit', help_text="May be one of several, linked to the Permit model. Do not select any options if there is no information about the permit.")

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
    use = models.CharField(max_length=2, choices=TYPE_CHOICES, help_text="Choose all types of development that form part of the application.")

    footprint = models.PolygonField(help_text="Should be a .geojson file.")

    geo_info = JSONField() # What the heck is this??

    # Info from the data capture sheets. I don't know how much of this is going to get used, possibly it should just be stored in json.
    applicant = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the development company who applied for the permit?")
    application_title = models.CharField(max_length=500, null=True, blank=True, help_text="Should describe what the development is, e.g. 'Establishment of the Northern Golf Course Estate, Johannesburg Gauteng'.")
    activity_description = models.TextField(null=True, blank=True, help_text="Provides more detail on what the development will entail, e.g. 'The development proposal will comprise of the following: Residential, internal roads, and access control.'")
    case_officer = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the case officer dealing with the application.")
    environmental_consultancy = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the consultancy who performed the EIA")
    environmental_assessment_practitioner = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the staff member in the above consultancy.")
    location_description = models.TextField(null=True, blank=True, help_text="A description of the locality of the development.")
    unique_id = models.CharField(max_length=200, null=True, blank=True, help_text="This is SANBI's ID number for this development.")

    def __str__(self):
        name = self.application_title
        if 'province' in self.geo_info:
            name += ' ' + self.geo_info['province']
        return name


class Permit(models.Model):
    """
    Developments can have several types of permits associated with different areas and issued on different dates.
    """
    permit_name = models.ForeignKey(PermitName, on_delete=models.CASCADE)
    development = models.ForeignKey(Development, on_delete=models.CASCADE)
    area_hectares = models.IntegerField(null=True, blank=True, help_text="The area in hectares associated with this permit.")
    date_issued = models.DateField(null=True, blank=True, help_text="The date this permit was issued.")
    reference_no = models.CharField(max_length=200, null=True, blank=True, help_text="The reference number for the permit.")


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
