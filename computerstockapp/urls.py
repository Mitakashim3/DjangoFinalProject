from django.urls import path
from . import views

urlpatterns = [
    path('', views.computer_list, name='computer_list'),
    path('add/', views.add_computer, name='add_computer'),
    path('edit/<int:computer_id>/', views.edit_computer, name='edit_computer'),
    path('delete/<int:computer_id>/', views.delete_computer, name='delete_computer'),
    path('restore/<int:computer_id>/', views.restore_computer, name='restore_computer'),
    path('archived/', views.archived_computers, name='archived_computers'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('import-csv/', views.import_csv, name='import_csv'),
]
