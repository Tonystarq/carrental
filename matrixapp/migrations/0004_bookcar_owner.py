# Generated by Django 4.0.2 on 2022-03-22 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrixapp', '0003_rename_mobile_no_bookcar_rentperday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcar',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]