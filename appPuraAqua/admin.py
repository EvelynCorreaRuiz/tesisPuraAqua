from django.contrib import admin
from .models import User, Comuna

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff']

admin.site.register(User, UserAdmin)
admin.site.register(Comuna)



