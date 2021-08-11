from django.urls import path
from concert import views


urlpatterns = [
    path('', views.index, name='index'),
]