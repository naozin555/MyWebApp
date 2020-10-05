from django.urls import path
from .views import hello_func, sign_up_func, log_in_func, detail_func, create_post_func, FoodHabitDelete,\
    list_func, log_out_func, good_func, read_func
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', hello_func, name='hello_func'),
    path('signup/', sign_up_func, name="signup"),
    path('login/', log_in_func, name="login"),
    path('list/', list_func, name="list"),
    path('detail/<int:pk>', detail_func, name="detail"),
    path('create/', create_post_func, name="create"),
    path('delete/<int:pk>', FoodHabitDelete.as_view(), name="delete"),
    path('logout', log_out_func, name="logout"),
    path('good/<int:pk>', good_func, name='good'),
    path('read/<int:pk>', read_func, name='read'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
