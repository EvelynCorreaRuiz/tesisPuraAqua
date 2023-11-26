from django.urls import path
from .views import home, products, exit, register, carrito
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('carrito/', carrito, name='carrito'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('change_quantity/<int:cart_item_id>/<int:quantity>/', views.change_quantity, name='change_quantity'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sale/<int:sale_id>/', views.sale_detail, name='sale_detail'),
    path('sales_overview/', views.sales_overview, name='sales_overview'),
    path('sales_overview/', views.sales_overview, name='sales_overview'),
]


