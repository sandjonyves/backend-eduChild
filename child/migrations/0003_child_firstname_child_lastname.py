# Generated by Django 5.0.4 on 2024-08-13 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0002_alter_child_dateofbirth'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='firstName',
            field=models.CharField(default='fistr', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='child',
            name='lastName',
            field=models.CharField(default='last', max_length=255),
            preserve_default=False,
        ),
    ]
