# Generated by Django 5.0.6 on 2024-05-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mnotes', '0005_alter_usermapnote_options_user_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='map_pins',
            field=models.ManyToManyField(blank=True, to='mnotes.mappincoordinate'),
        ),
    ]
