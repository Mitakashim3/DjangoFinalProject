from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

class ComputerStock(models.Model):
    computer_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=20)   
    storage = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_archived = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.computer_name} - {self.brand} {self.model}"
    
    @property
    def local_date_added(self):
        return localtime(self.date_added)
    
    @property
    def local_date_modified(self):
        return localtime(self.date_modified)
    
    class Meta:
        ordering = ['-date_added']
