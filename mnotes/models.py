from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models


class User(AbstractUser):
    """Extended user table with an assigned list of notes"""

    map_pins = models.ManyToManyField("UserMapNote", blank=True)


class UserMapNote(models.Model):
    """A table of notes related to map pin IDs"""

    title = models.CharField(max_length=64, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    date_published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Published"
    )
    map_pin_point = models.PointField(verbose_name="Coordinates")

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ["-date_published"]
