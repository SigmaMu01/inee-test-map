# Generated by Django 5.0.6 on 2024-05-16 15:51

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mnotes", "0005_alter_usermapnote_map_pin_point"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usermapnote",
            name="map_pin_point",
            field=django.contrib.gis.db.models.fields.PointField(
                srid=4326, verbose_name="Coordinates"
            ),
        ),
    ]
