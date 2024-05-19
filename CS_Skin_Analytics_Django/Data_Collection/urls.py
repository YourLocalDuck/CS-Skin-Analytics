from django.urls import path
from . import views

urlpatterns = [
    path('init_update/', views.collect, name='Update Markets'),
]
