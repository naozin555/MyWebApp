from django.contrib import admin

from .models import Board, FoodHabitModel

# Register your models here.

admin.site.register(FoodHabitModel)
admin.site.register(Board)
