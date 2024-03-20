from django.urls import path
from . import views

urlpatterns = [
    path('buff163/', views.collectBuff163, name='Update Buff 163'),
    path('skinout/', views.collectSkinout, name='Update Skinout'),
    path('skinport/', views.collectSkinport, name='Update Skinport'),
    path('steam/', views.collectSteam, name='Update Steam'),
]
