from django.urls import path
from .views import ToDoList, ToDoDetail, ToDoCreate, ToDoDelete, ToDoUpdate

urlpatterns = [
    path('list/', ToDoList.as_view(), name='list'),
    path('detail/<int:pk>', ToDoDetail.as_view(), name='detail'),
    path('create/', ToDoCreate.as_view(), name='create'),
    path('delete/<int:pk>', ToDoDelete.as_view(), name='delete'),
    path('update/<int:pk>', ToDoUpdate.as_view(), name='update'),
]
