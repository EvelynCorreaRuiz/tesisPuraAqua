from django.contrib import admin
from .models import User, Comuna, Product, CartItem, Cart

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff']

admin.site.register(User, UserAdmin)
admin.site.register(Comuna)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)


