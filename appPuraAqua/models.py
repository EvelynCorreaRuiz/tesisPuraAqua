import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError(_("La contraseña debe tener al menos 12 caracteres"))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("La contraseña debe contener al menos un número"))
        if not any(char.isupper() for char in password):
            raise ValidationError(_("La contraseña debe contener al menos una letra mayúscula"))
        if not any(char in '!@#$%^&*()_+.' for char in password):  # Agregado el punto '.' aquí
            raise ValidationError(_("La contraseña debe contener al menos un carácter especial (!, @, #, $, %, ^, &, *, (, ), _, +, .)"))  # Agregado el punto '.' aquí

    def get_help_text(self):
        return _("""Tu contraseña debe contener al menos 12 caracteres, un número, una letra mayúscula y un carácter especial (!, @, #, $, %, ^, &, *, (, ), _, +, .)""")  # Agregado el punto '.' aquí

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
class City(models.Model):
    name_city = models.CharField(max_length=200)

    def __str__(self):
        return self.name_city
    
class Comuna(models.Model):
    name_comuna = models.CharField(max_length=50)

    def __str__(self):
        return self.name_comuna

class User(AbstractUser):
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message="El nombre y apellido solo deben contener letras"
    )
        
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # username is not required
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', "rut"]

    objects = CustomUserManager()  # use the custom manager

    email = models.EmailField(unique=True)  # ensure email is unique
    first_name = models.CharField(validators=[name_validator], max_length=30)
    last_name = models.CharField(validators=[name_validator], max_length=30)
    last_name2 = models.CharField(validators=[name_validator], max_length=20)

    
    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dKk]$',
        message="El RUT debe tener el formato: 12345678-9 o 12345678-K"
    )
    rut = models.CharField(validators=[rut_validator], unique=True, max_length=10)

    phone_validator = RegexValidator(
        regex=r'^\+56\d{9}$',
        message="El número de teléfono debe tener el formato: +56912345678"
    )
    phone = models.CharField(validators=[phone_validator], max_length=12)
    address = models.CharField(max_length=50) 

    number_validator = RegexValidator(
        regex=r'^\d+$',
        message="El número de dirección debe contener solo dígitos"
    )
    numberAddress = models.CharField(validators=[number_validator], max_length=10)
    birthdate = models.DateField(default=date.today)

    class Meta:
        db_table = 'Usuario'

    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    verification_code = models.CharField(default=uuid.uuid4, unique=True, max_length=20)

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    imagen = models.ImageField(upload_to='products', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Product, through='SoldProduct')

class SoldProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



