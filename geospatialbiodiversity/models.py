from django.contrib.gis.db import models


class Area(models.Model):
    """
    Developments are buildings or groups of buildings/constructions which are undertaken somewhere in South Africa.
    The permits are already obtained and the building is completed.
    """
    name = models.CharField(max_length=500)
    identifier = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    RAMSAR = 'RA'
    WORLD_HERITAGE = 'WH'
    NATIONAL_PARK = 'NP'
    BOTANICAL_GARDEN = 'BG'
    PROVINCE = 'P'
    TYPE_CHOICES = (
        (RAMSAR, 'Ramsar Site'),
        (WORLD_HERITAGE, 'World Heritage Site'),
        (NATIONAL_PARK, 'National Park'),
        (BOTANICAL_GARDEN, 'Botanical Garden'),
        (BOTANICAL_GARDEN, 'Province'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    polygon = models.PolygonField()

    def __str__(self):
        return self.name
