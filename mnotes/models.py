from django.db import models

'''
class Users(models.Model):
    """A table of users with a list of their map pins"""
    token = models.CharField(max_length=64)
    first_name = ''
    second_name = ''
    map_pins = []  # Replace with a list of foreign keys
'''

class UserMapNote(models.Model):
    """A table of notes related to map pin IDs"""
    title = models.CharField(max_length=64)
    description = models.TextField()
    map_pin_id = models.IntegerField()  # Replace with foreign key
    date_published = models.DateTimeField(auto_now_add=True, db_index=True)
#    is_visible = models.BooleanField(default=True)

'''
class MapPinsCoordinates(models.Model):
    """A table of map pins"""
    map_pin_latitude = ''  # Replace with Postgis fields
    map_pin_longitude = ''
'''
