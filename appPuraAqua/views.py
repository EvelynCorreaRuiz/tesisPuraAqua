from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem, Product, Sale, SoldProduct
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Sum
from django.db.models import F

def sales_overview(request):
    if not request.user.is_superuser:
        return redirect('products')

    # Obtén todas las ventas
    sales = Sale.objects.all()

    return render(request, 'aquaPura/sales_overview.html', {'sales': sales})

@login_required
def sale_detail(request, sale_id):
    # Obtén la venta
    sale = get_object_or_404(Sale, id=sale_id)

    # Asegúrate de que el usuario que solicita la vista es el usuario que realizó la venta
    if request.user != sale.user:
        return HttpResponse("No tienes permiso para ver esta venta.")

    # Obtén los productos vendidos en esta venta
    sold_products = SoldProduct.objects.filter(sale=sale)

    # Renderiza la vista
    return render(request, 'aquaPura/sale_detail.html', {'sale': sale, 'sold_products': sold_products})

@login_required
def checkout(request):
  # Obtén el carrito del usuario
  cart = Cart.objects.get(user=request.user)

  # Crea un nuevo objeto de Venta
  sale = Sale.objects.create(user=request.user, total=cart.total, date=timezone.now())

  # Para cada producto en el carrito, crea un nuevo objeto de ProductoVendido y disminuye la cantidad de producto en el inventario
  for item in cart.cartitem_set.all():
    SoldProduct.objects.create(sale=sale, product=item.product, quantity=item.quantity)
    product = item.product
    product.quantity -= item.quantity
    product.save()

  # Vacía el carrito
  cart.cartitem_set.all().delete()

  # Actualiza el total del carrito a 0
  cart.total = 0
  cart.save()

  return redirect('sale_detail', sale_id=sale.id)

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