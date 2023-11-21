from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

# Create your views here.
def home(request):
    return render(request, 'aquaPura/home.html')

@login_required
def products(request):
    return render(request, 'aquaPura/products.html')

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

