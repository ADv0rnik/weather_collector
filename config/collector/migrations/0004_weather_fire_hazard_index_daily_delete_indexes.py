# Generated by Django 4.0.4 on 2022-05-17 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_alter_weather_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='fire_hazard_index_daily',
            field=models.FloatField(blank=True, default=100.0),
        ),
        migrations.DeleteModel(
            name='Indexes',
        ),
    ]
