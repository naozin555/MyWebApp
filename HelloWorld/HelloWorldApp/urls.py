from django.urls import path
from .views import hello_world_function_app

urlpatterns = [
    path('world3/', hello_world_function_app),
]
