# Generated by Django 4.0.4 on 2022-05-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_alter_weather_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]