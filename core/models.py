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

    TYPE_CHOICES = (
        ('AG', 'Agriculture'),
        ('BU', 'Business'),
        ('GO', 'Government'),
        ('GP', 'Government purposes'),
        ('IN', 'Industrial'),
        ('MI', 'Mining'),
        ('MU', 'Multi-use (public, residential, commercial)'),
        ('RC', 'Recreational'),
        ('RE', 'Residential'),
        ('TR', 'Transport'),
        ('UN', 'Unknown'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, help_text="Choose the one which fits best.")

    footprint = models.PolygonField(help_text="Should be a .geojson file.")

    info = JSONField()

    def save(self, *args, **kwargs):
        province = polygon_models.Area.objects.filter(type=polygon_models.Area.PROVINCE,
                                                      polygon__contains=self.footprint).first()
        #info = {'province': province,
        #        }
        geo_info = services.get_area_info(self.footprint)
        import pdb; pdb.set_trace()

        super(Development, self).save(*args, **kwargs)

    def province(self):
        province = polygon_models.Area.objects.filter(type=polygon_models.Area.PROVINCE, polygon__contains=self.footprint).first()
        return str(province)


class OffsetImplementationTime(models.Model):
    """
    The offsets required by a development can be implemented over multiple time frames, such as:
    Before development, During development, After development - 6 months, After development - 12 months,
    After development - 24 months, After development - more than 24 months
    """
    time = models.CharField(max_length=50)

    def is_staggered(self):
        """If there's more than one implementation time, the implementation is considered to be 'staggered'."""
        return False


class Offset(models.Model):
    """
    Developments might occur on a sensitive piece of land - e.g. a protected area. In which case, the development
    should be associated with one or several offsets. There are different types of offsets implemented over different
    periods, lasting for different durations.
    If an offset is of type hectares it should have an associated polygon.
    """
    development = models.ForeignKey(Development)
    polygon = models.PolygonField(null=True, blank=True)  # This is rather messy, perhaps there's a better way to do it?

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

    DURATION_CHOICES = (
        ('PE', 'Perpetuity'),
        ('US', 'Unspecified'),
        ('UN', 'Unknown'),
        ('LT', '< 20 years'),
        ('TF', 'Between 20 and 50 years'),
        ('HC', '> 50 years'),
    )
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES)

    implementation_times = models.ManyToManyField(OffsetImplementationTime)
