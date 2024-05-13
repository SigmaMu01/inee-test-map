from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models

from mnotes.app_defaults import *


class User(AbstractUser):
    map_pins = models.ManyToManyField("UserMapNote", blank=True)


class UserMapNote(models.Model):
    """A table of notes related to map pin IDs"""
    title = models.CharField(max_length=64, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    date_published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Published")
    map_pin_point = models.PointField(default="0101000020E61000000700004002806F3FEC03C83F02E069BF")

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ["-date_published"]


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField("Population 2005")
    fips = models.CharField("FIPS Code", max_length=2, null=True)
    iso2 = models.CharField("2 Digit ISO", max_length=2)
    iso3 = models.CharField("3 Digit ISO", max_length=3)
    un = models.IntegerField("United Nations Code")
    region = models.IntegerField("Region Code")
    subregion = models.IntegerField("Sub-Region Code")
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name


"""
# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class WorldBorder(models.Model):
    fips = models.CharField(max_length=2)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    un = models.IntegerField()
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.BigIntegerField()
    region = models.IntegerField()
    subregion = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for WorldBorder model
worldborder_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'geom': 'MULTIPOLYGON',
}
"""


class City(models.Model):
    name = models.CharField(max_length=100, blank=False)
    geometry = models.PointField()

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        ordering = ('name',)
