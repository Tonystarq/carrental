# Generated by Django 4.0.2 on 2022-03-22 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matrixapp', '0004_bookcar_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookcar',
            name='owner',
        ),
    ]
