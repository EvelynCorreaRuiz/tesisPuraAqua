from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "rut", "last_name", "last_name2", "email", "phone", "address", "city", "numberAddress", "birthdate", "password1", "password2", "is_staff", "comuna"]

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 18:
            raise ValidationError('Debes tener al menos 18 años para registrarte.')

        return birthdate

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.is_staff = False
        if commit:
            user.save()

        return user

class ProfileUpdateForm(UserChangeForm):
    password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("email", 'address', "numberAddress", "comuna", "phone", 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()

        # Validación del email
        email = cleaned_data.get('email')
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            self.add_error('email', 'El email no es válido')

        # Validación del número de dirección
        numberAddress = cleaned_data.get('numberAddress')
        if numberAddress and not re.match(r'^\d+$', numberAddress):
            self.add_error('numberAddress', 'El número de dirección solo debe contener dígitos')

        # Validación del teléfono
        phone = cleaned_data.get('phone')
        if phone and not re.match(r'^\+56\d{9}$', phone):
            self.add_error('phone', 'El número de teléfono debe tener el formato: +56912345678')

        # Validación de las contraseñas
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2:
            if len(password1) < 12 or len(password2) < 12:
                self.add_error('password1', 'La contraseña debe tener al menos 12 caracteres')
                self.add_error('password2', 'La contraseña debe tener al menos 12 caracteres')
            if not re.search(r'[A-Z]', password1) or not re.search(r'[A-Z]', password2):
                self.add_error('password1', 'La contraseña debe contener al menos una letra mayúscula')
                self.add_error('password2', 'La contraseña debe contener al menos una letra mayúscula')
            if not re.search(r'\W', password1) or not re.search(r'\W', password2):
                self.add_error('password1', 'La contraseña debe contener al menos un carácter especial')
                self.add_error('password2', 'La contraseña debe contener al menos un carácter especial')
            if '.' not in password1 or '.' not in password2:
                self.add_error('password1', 'La contraseña debe contener el carácter "."')
                self.add_error('password2', 'La contraseña debe contener el carácter "."')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
    
class VerificationForm(forms.Form):
    code = forms.CharField(max_length=100)
