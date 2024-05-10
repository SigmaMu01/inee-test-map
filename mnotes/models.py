from django.contrib.gis.db import models

from mnotes.app_defaults import *


class User(models.Model):
    """A table of users with a list of their map pins"""
    token = models.CharField(max_length=64)  # PASS
    first_name = models.CharField(max_length=32, null=True)
    second_name = models.CharField(max_length=64, null=True)
    avatar = models.ImageField(default=default_avatar_path())
    map_pins = models.ManyToManyField("MapPinCoordinate", blank=True)  # Replace with a list of foreign keys

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class UserMapNote(models.Model):
    """A table of notes related to map pin IDs"""
    title = models.CharField(max_length=64, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    date_published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Published")

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ["-date_published"]


class MapPinCoordinate(models.Model):
    """A table of map pins"""
    map_pin_point = models.PointField()
    note = models.OneToOneField("UserMapNote", on_delete=models.CASCADE)  # Delete pins to remove notes
