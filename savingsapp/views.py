from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Account, Ledgers
from decimal import Decimal

def Home(request):
    data = {
        'ledgers': Ledgers.objects.select_related('account_number').all()
    }
    return render(request, 'savingsapp/balay.html', data)

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        account = Account(username=username, fullname=fullname, email=email, password=password)
        account.save()
        ledger = Ledgers(account_number=account, amount=0,
            current_balance=0,
            holding_balance=0)
        ledger.save()
        return redirect('home')
    return render(request, 'savingsapp/register.html')

def Cashin(request):
    if request.method == 'POST':
        accountnumber = request.POST.get('account_number')
        amount = Decimal(request.POST.get('amount'))
        account = get_object_or_404(Account, savings_account_number=accountnumber)
        ledger = get_object_or_404(Ledgers, account_number=account)
        ledger.current_balance += amount
        ledger.save()
        return redirect('balay')
    
    context = {
        'account_number': request.GET.get('account_number')
    }
    return render(request, 'savingsapp/cashin.html', context)

def Cashout(request):
    if request.method == 'POST':
        accountnumber = request.POST.get('account_number')
        holding = Decimal(request.POST.get('hold'))
        account = get_object_or_404(Account, savings_account_number=accountnumber)
        ledger = get_object_or_404(Ledgers, account_number=account)
        if ledger.current_balance >= holding:
            ledger.holding_balance += holding
            ledger.save()
            return redirect('balay')
        else:
            return HttpResponse("Insufficient funds")
    
    context = {
        'account_number': request.GET.get('account_number')
    }
    return render(request, 'savingsapp/cashout.html', context)


