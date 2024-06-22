from django.urls import path
from . import views

urlpatterns = [
    path('profit-summary/', views.getProfitSummary, name='Profit Summary'),
]
