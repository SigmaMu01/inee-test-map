# Generated by Django 5.0.6 on 2024-05-09 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mnotes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserMapNotes',
            new_name='UserMapNote',
        ),
    ]