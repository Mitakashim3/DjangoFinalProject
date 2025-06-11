from django.contrib import admin
from .models import ComputerStock

@admin.register(ComputerStock)
class ComputerStockAdmin(admin.ModelAdmin):
    list_display = ['computer_name', 'brand', 'model', 'price', 'quantity', 'is_archived', 'date_added']
    list_filter = ['brand', 'date_added']
    search_fields = ['computer_name', 'brand', 'model']
    list_per_page = 20
