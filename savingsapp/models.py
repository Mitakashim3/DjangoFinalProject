from django.db import models
import string
import random

def account_number_generator():
    prefix = '000'
    random_number = ''.join(random.choices(string.digits, k=10))
    return prefix + random_number
# Create your models here.
class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    savings_account_number = models.CharField(max_length=20, unique=True, editable=False,default=account_number_generator)
    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ledgers(models.Model):
    id= models.BigAutoField(primary_key=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    holding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def total_balance(self):
        return self.current_balance - self.holding_balance
