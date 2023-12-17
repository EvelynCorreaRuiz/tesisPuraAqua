from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, VerificationForm
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem, Product, Sale, SoldProduct
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Sum
from django.db.models import F
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Sale
from django.contrib import messages
from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                user = User.objects.get(verification_code=code)
                user.is_active = True  # Activa el usuario
                user.verification_code = None  # Borra el código de verificación
                user.save()

                # Autentica y haz login al usuario
                login(request, user)

                return redirect('home')  # Redirect to home page
            except ObjectDoesNotExist:
                form.add_error('code', 'El código de verificación es incorrecto. Por favor, inténtalo de nuevo.')
    else:
        form = VerificationForm()
    return render(request, 'registration/verify.html', {'form': form})

def purchase_history(request):
    # Asegúrate de que el usuario esté autenticado
    if not request.user.is_authenticated:
        return redirect('login')  # redirige al usuario a la página de inicio de sesión si no está autenticado

    # Obtiene todas las ventas para el usuario actual
    sales = Sale.objects.filter(user=request.user)

    # Para cada venta, obtén los productos vendidos y añádelos a la venta como un atributo
    for sale in sales:
        sale.products = sale.items.all()

    # Renderiza la plantilla con las ventas como contexto
    return render(request, 'aquaPura/purchase_history.html', {'sales': sales})

@login_required
def profile(request):
    form = ProfileUpdateForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})


def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión para que no se invalide después de cambiar la contraseña
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

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

    # Calcula el total de la venta
    total = sum([p.product.price * p.quantity for p in sold_products])

    # Renderiza la vista
    return render(request, 'aquaPura/sale_detail.html', {'sale': sale, 'sold_products': sold_products, 'total': total})



@login_required
def checkout(request):
  # Obtén el carrito del usuario
  cart = Cart.objects.get(user=request.user)

  # Comprueba si el total del carrito es 0
  if cart.total == 0:
    messages.error(request, 'No puedes realizar el checkout con un carrito vacío.')
    return redirect('carrito')

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
    # Resta el precio del artículo del total del carrito
    cart_item.cart.total -= cart_item.product.price * cart_item.quantity
    cart_item.cart.save()
    cart_item.delete()
    return redirect('carrito')

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    # Aumenta el total del carrito
    cart_item.cart.total += cart_item.product.price
    cart_item.cart.save()
    return redirect('carrito')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        # Disminuye el total del carrito
        cart_item.cart.total -= cart_item.product.price
        cart_item.cart.save()
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
    

from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # No guardes el usuario todavía
            user.is_active = False  # Haz que el usuario esté inactivo
            user.save()  # Ahora guarda el usuario

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # Genera un código de verificación y guárdalo en el usuario
            verification_code = User.objects.make_random_password()  # Genera un código aleatorio
            user.verification_code = verification_code
            user.save()

            # Envía un correo electrónico con el código de verificación
            send_mail(
                'Código de verificación',
                f'Tu código de verificación es {verification_code}.',
                'from@example.com',  # Reemplaza con tu dirección de correo electrónico
                [user.email],
                fail_silently=False,
            )

            return redirect('verify')  # Redirect to verification page
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

#mensajes de error