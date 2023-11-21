from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "rut", "last_name", "last_name2", "email", "phone", "address", "city", "numberAddress", "birthdate", "password1", "password2", "is_staff"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.is_staff = False
        if commit:
            user.save()
        return user