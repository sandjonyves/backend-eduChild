# Generated by Django 5.0.4 on 2024-08-09 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='dateOfBirth',
            field=models.DateField(),
        ),
    ]
