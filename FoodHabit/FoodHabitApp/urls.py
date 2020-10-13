from django.urls import path
from .views import sign_up_func, log_in_func, detail_func, create_post_func, delete_func,\
    list_func, log_out_func, good_func, read_func

urlpatterns = [
    path('signup/', sign_up_func, name="signup"),
    path('', log_in_func, name="login"),
    path('list/', list_func, name="list"),
    path('detail/<int:pk>', detail_func, name="detail"),
    path('create/', create_post_func, name="create"),
    path('delete/<int:pk>', delete_func, name="delete"),
    path('logout', log_out_func, name="logout"),
    path('good/<int:pk>', good_func, name='good'),
    path('read/<int:pk>', read_func, name='read'),
]
