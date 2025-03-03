from django.shortcuts import render,redirect
from django.http import HttpResponse
from . forms import CreateUserForm,LoginForm

# Authentication models and functions
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



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

def check_username(request):
    username = request.GET.get('username', '')
    
    # Check if the username is already taken
    username_taken = User.objects.filter(username=username).exists()
    
    # Generate suggestions if username is taken
    suggestions = []
    if username_taken:
        # Generate some similar suggestions (this is just a simple example, you could use more sophisticated logic)
        suggestions = [
            f"{username}{i}" for i in range(1, 6) if not User.objects.filter(username=f"{username}{i}").exists()
        ]
    
    return JsonResponse({
        'username_taken': username_taken,
        'suggestions': suggestions
    })

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=username)
                username = user.username  # Get the corresponding username
            except User.DoesNotExist:
                username = username

            user = authenticate(request,username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'loginform':form}
    return render(request, 'login/login.html',context)

def user_logout(request):
    auth.logout(request)
    return redirect("")

 
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
