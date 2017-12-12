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
    name = models.CharField(max_length=100, help_text="Name of the permit - e.g. Water Use License (WULA).")
    authority = models.CharField(max_length=100, help_text="Name of the authority who issues the permit - e.g. Department of Water Affairs.")

    def __str__(self):
        return self.name + ' - ' + self.authority

    class Meta:
        unique_together = ('name', 'authority')


class Development(models.Model):
    """
    Developments are buildings or groups of buildings/constructions which are undertaken somewhere in South Africa.
    The permits are already obtained and the building is completed.
    """
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

    footprint = models.MultiPolygonField(help_text="Should be a .geojson file.", null=True, blank=True)
    location_description = models.TextField(null=True, blank=True, help_text="A description of the locality of the development.")
    geo_info = JSONField(null=True, blank=True) # What the heck is this??

    # Info from the data capture sheets. I don't know how much of this is going to get used, possibly it should just be stored in json.
    developer= models.CharField(max_length=100, null=True, blank=True, help_text="The name of the development company who applied for the permit?")

    code = models.CharField(max_length=200, null=True, blank=True, help_text="This is SANBI's ID number for this development.")

    def __str__(self):
        name = self.application_title
        #if 'province' in self.geo_info:
        #    name += ' ' + self.geo_info['province']
        return self.unique_id


class Permit(models.Model):
    """
    Developments can have several types of permits associated with different areas and issued on different dates.
    """
    permit_name = models.ForeignKey(PermitName, on_delete=models.CASCADE)
    development = models.ForeignKey(Development, on_delete=models.CASCADE)
    reference_no = models.CharField(max_length=200, null=True, blank=True, help_text="The reference number for the permit.")
    date_issued = models.DateField(null=True, blank=True, help_text="The date this permit was issued.")

    area_hectares = models.IntegerField(null=True, blank=True, help_text="The area in hectares associated with this permit.")
    case_officer = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the case officer dealing with the permit.")
    application_title = models.CharField(max_length=500, null=True, blank=True, help_text="Should describe what the development is, e.g. 'Establishment of the Northern Golf Course Estate, Johannesburg Gauteng'.")
    activity_description = models.TextField(null=True, blank=True, help_text="Provides more detail on what the development will entail, e.g. 'The development proposal will comprise of the following: Residential, internal roads, and access control.'")
    environmental_consultancy = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the consultancy who performed the EIA")
    environmental_assessment_practitioner = models.CharField(max_length=100, null=True, blank=True, help_text="The name of the staff member in the above consultancy.")

    OFFSET_REQUIREMENT_STIPULATED = 'Y'
    OFFSET_REQUIREMENT_NOT_DETERMINED = 'D'
    OFFSET_REQUIREMENT_NOT_PUBLICISED = 'P'
    OFFSET_REQUIREMENT_STIPULATED_CHOICES = (
        (OFFSET_REQUIREMENT_STIPULATED, 'Yes'),
        (OFFSET_REQUIREMENT_NOT_DETERMINED, 'No, the offset hasn\'t been determined'),
        (OFFSET_REQUIREMENT_NOT_PUBLICISED, 'No, not publicised')
    )
    offset_requirement_stipulated = models.CharField(max_length=2, choices=OFFSET_REQUIREMENT_STIPULATED_CHOICES, help_text="Choose all types of development that form part of the application.")


class OffsetImplementationTime(models.Model):
    """
    The offsets required by a development can be implemented over multiple time frames:
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
    permit = models.ForeignKey(Permit, null=True, blank=True,)
    polygon = models.MultiPolygonField(null=True, blank=True)

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


class OffsetTrigger(models.Model):
    ECOSYSTEM = 'E'
    THREATENED_SP = 'T'
    TYPE_OF_TRIGGER_CHOICES = (
        (ECOSYSTEM, 'Ecosystem'),
        (THREATENED_SP, 'Threatened or protected species')
    )
    type_of_trigger = models.CharField(max_length=1, choices=TYPE_OF_TRIGGER_CHOICES)
    name = models.CharField(max_length=200, null=True, blank=True, help_text="The name of the ecosystem or protected species.")

    # Optional fields sometimes not displayed (only for ecosystems)
    size = models.IntegerField(null=True, blank=True, help_text="This is the actual amount of space the development is taking up of this ecosystem.")
    required_offset_size = models.IntegerField(null=True, blank=True, help_text="The condition of the authorisation, specified in hectares.")

    MET = 'ME'
    NOT_MET_LAPSED = 'LA'
    NOT_MET_IN_PROGRESS = 'IP'
    NOT_MET_UNKNOWN = 'NU'
    OFFSET_MET_CHOICES = (
        (MET, 'Yes, this offset has been met'),
        (NOT_MET_LAPSED, 'No, this offset has not been met and the time has lapsed, it is outstanding.'),
        (NOT_MET_IN_PROGRESS, 'No, this offset has not yet been met but the development is still in progress.'),
        (NOT_MET_UNKNOWN, 'No, this offset has not been met for reasons unknown.'),
    )
    offset_met = models.CharField(max_length=1, choices=OFFSET_MET_CHOICES, null=True, blank=True,)



