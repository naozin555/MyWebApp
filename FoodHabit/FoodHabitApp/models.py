from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Board(models.Model):
    """投稿記事のモデル"""
    author = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)
    good = models.IntegerField(null=True, blank=True, default=0)
    bad = models.IntegerField(null=True, blank=True, default=0)
    read = models.IntegerField(null=True, blank=True, default=0)
    readtext = models.CharField(max_length=200, null=True, blank=True, default='a')


class FoodHabitModel(models.Model):
    """食習慣のモデル"""
    class Meta:
        db_table = 'food_habit_table'
    date = models.DateField(verbose_name='日付')
    weight = models.FloatField(verbose_name='体重')
    food_name = models.CharField(verbose_name='食品名', max_length=20)
    # 食品のカテゴリは、赤・黄・緑の3種類
    # 赤：血や肉を作る、黄：エネルギー源になる、緑：からだの調子を整える
    food_category = models.CharField(verbose_name='食品のカテゴリ', max_length=15)