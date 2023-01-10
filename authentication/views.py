from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() == False:
            messages.error(request, 'That user does not exist')
            return redirect('login_view')
        elif authenticate(request, username = username, password = password) == None:
            messages.error(request, 'Incorrect password')
            return redirect('login_view')
        else:
            user = authenticate(request, username = username, password = password)
            login(request, user)
            return redirect('home')

    else:
        context = {
            'form' : AuthenticationForm()
        }
        return render(request, 'authentication/login.html', context)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists() == True:
            messages.error(request, 'That username already exists')
            return redirect('register')
        elif User.objects.filter(email__iexact=email).exists == True:
            messages.error(request, 'That email already exists')
            return redirect('register')
        elif password1 != password2:
            messages.error(request, 'Passwords did not match')
            return redirect('register')
        else:
            if form.is_valid():
                form.save()
                user = authenticate(username = username, password = password1)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('register')

    else:
        context = {
            'form' : UserRegisterForm
        }
        return render (request, 'authentication/register.html', context)



class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'authentication/login.html'
    extra_context = {
        'form' : AuthenticationForm()
    }