# Generated by Django 2.2.16 on 2020-10-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodHabitModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.FloatField()),
                ('food_name', models.CharField(max_length=20)),
                ('food_category', models.CharField(max_length=15)),
            ],
        ),
    ]