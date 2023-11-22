from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem, Product
from django.http import JsonResponse

def empty_cart(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)
        items.delete()
        cart.total = 0
        cart.save()
    return redirect('carrito')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('carrito')

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('carrito')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('carrito')

@login_required
def change_quantity(request, cart_item_id, quantity):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    difference = quantity - cart_item.quantity
    cart_item.quantity = quantity
    cart_item.save()
    cart_item.cart.total += difference * cart_item.product.price
    cart_item.cart.save()
    return redirect('carrito')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'total': 0})
    quantity = request.POST.get('quantity', 1)
    if quantity in [None, '']:
        quantity = 1
    else:
        quantity = int(quantity)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'quantity': quantity})
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    cart.total += product.price * quantity
    cart.save()
    return redirect('products')  # Redirige al usuario a la página de productos

@login_required
def carrito(request):
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'total': 0})
    items = CartItem.objects.filter(cart=cart)
    for item in items:
        item.price = item.product.price * item.quantity
    return render(request, 'aquaPura/carrito.html', {'cart': cart, 'items': items})


def home(request):
    return render(request, 'aquaPura/home.html')

@login_required
def products(request):
    products = Product.objects.all()
    return render(request, 'aquaPura/products.html', {'products': products})

def exit(request):
    logout(request)
    return redirect('home')
    

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})