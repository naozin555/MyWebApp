# Generated by Django 2.2.16 on 2020-10-05 06:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('FoodHabitApp', '0004_auto_20201005_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
