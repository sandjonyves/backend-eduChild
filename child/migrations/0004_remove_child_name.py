# Generated by Django 5.0.4 on 2024-08-13 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0003_child_firstname_child_lastname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='name',
        ),
    ]
