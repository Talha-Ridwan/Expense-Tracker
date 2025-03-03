from django.shortcuts import render,redirect
from django.http import HttpResponse
from . forms import CreateUserForm,LoginForm

# Authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Create your views here.
def homepage(request):
    return render(request, 'index/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')
    context = {'registerform':form}
    return render(request, 'registration/register.html',context)

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect("dashboard")
    context = {'loginform':form}
    return render(request, 'login/login.html',context)

def user_logout(request):
    auth.logout(request)
    return redirect("")

 
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
