from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "rut", "last_name", "last_name2", "email", "phone", "address", "city", "numberAddress", "birthdate", "password1", "password2", "is_staff", "comuna"]
        

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
