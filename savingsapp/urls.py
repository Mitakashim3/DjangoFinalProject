from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name='balay'),
    path('register/', views.Register, name='register'),
    path('cashin/', views.Cashin, name='cashin'),
    path('cashout/', views.Cashout, name='cashout'),
]