from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('addproduct/', views.AddProduct, name='product'),
    path('edit/<int:uid>', views.UpdateProduct, name='edit'),
]