from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='Login'),
    path('signup/', views.signup, name='Sign Up'),
    path('test_token/', views.test_token, name='test_token'),
]
