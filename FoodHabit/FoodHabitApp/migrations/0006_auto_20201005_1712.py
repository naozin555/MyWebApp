# Generated by Django 2.2.16 on 2020-10-05 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodHabitApp', '0005_auto_20201005_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodhabitmodel',
            name='date',
            field=models.DateField(verbose_name='日付'),
        ),
        migrations.AlterField(
            model_name='foodhabitmodel',
            name='food_category',
            field=models.CharField(max_length=15, verbose_name='食品のカテゴリ'),
        ),
        migrations.AlterField(
            model_name='foodhabitmodel',
            name='food_name',
            field=models.CharField(max_length=20, verbose_name='食品名'),
        ),
        migrations.AlterField(
            model_name='foodhabitmodel',
            name='weight',
            field=models.FloatField(verbose_name='体重'),
        ),
        migrations.AlterModelTable(
            name='foodhabitmodel',
            table='food_habit_table',
        ),
    ]