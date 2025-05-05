from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from decimal import Decimal

def Home(request):
    sortBy = request.GET.get('order_by', 'id')
    kword = request.GET.get('kword', '')
    products = Product.objects.order_by(sortBy).filter(name__icontains=kword)
    if kword:
        products = products.filter(name__icontains=kword)
    
    context = {
        'products': products,
        'kword': kword,
    }
    return render(request, 'productapp/home.html', context)

def AddProduct(request):
    if request.method == 'POST':
        name = request.POST.get('product_name')
        amount = Decimal(request.POST.get('amount'))
        price = Decimal(request.POST.get('product_price'))
        product = Product(name=name, amount=amount, price=price)
        product.save()
        return redirect('home')
    return render(request, 'productapp/addproduct.html')

def UpdateProduct(request, uid):
    product = get_object_or_404(Product, id=uid)
    if request.method == 'GET':
        context = {
            'product': product,
        }
        return render(request, 'productapp/edit.html', context)
    if request.method == 'POST':
        product.name = request.POST.get('product_name')
        product.amount = Decimal(request.POST.get('amount'))
        product.price = Decimal(request.POST.get('product_price'))
        product.save()
        return redirect('home')
    context = {
        'product': product,
    }
    return render(request, 'productapp/edit.html', context)
