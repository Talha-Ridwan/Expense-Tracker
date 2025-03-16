from django.shortcuts import render,redirect
from django.http import HttpResponse
from . forms import CreateUserForm,LoginForm

# Authentication models and functions
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.core.mail import send_mail
from ExpenseTracker.settings import EMAIL_HOST_USER
import random
from django.views.decorators.csrf import  csrf_exempt

# Create your views here.
def homepage(request):
    return render(request, 'index/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        form = CreateUserForm(request.POST)
        if form.is_valid():
            otp = random.randint(100000,999999)
            send_mail("User Data: ",f"Verify your ExpenseTracker account using this OTP: {otp}", EMAIL_HOST_USER,[email],fail_silently=True)
            return render(request, 'registration/otp.html',{'otp':otp,'first_name':first_name,'last_name':last_name,'email':email,'username':username,"password1":password1,'password2':password2})

    context = {'registerform':form}
    return render(request, 'registration/register.html',context)


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username
            )
            user.set_password(password1)  # Encrypt the password
            user.save()

            send_mail(
                "User Data: ",
                "Your account has been created successfully",
                EMAIL_HOST_USER,
                [email],
                fail_silently=True
            )

            return JsonResponse({'message': 'User created successfully'}, status=200)
    
    return JsonResponse({'error': 'Password mismatch'}, status=400)



def check_username(request):
    username = request.GET.get('username', '')
    
    # Check if the username is already taken
    username_taken = User.objects.filter(username=username).exists()
    
    # Generate suggestions if username is taken
    suggestions = []
    if username_taken:
        suggestions = [
            f"{username}{i}" for i in range(1, 6) if not User.objects.filter(username=f"{username}{i}").exists()
        ]
    
    return JsonResponse({
        'username_taken': username_taken,
        'suggestions': suggestions
    })


# def my_login(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         print('asdf')
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             print('hi')

#             user = authenticate(request,username=username, password=password)
            
#             if user is not None:
#                 auth.login(request, user)
#                 return redirect("dashboard")
#     context = {'loginform':form}
#     return render(request, 'login/login.html',context)


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('asdf')
        users = User.objects.values('email', 'username')  # Get both email and username
        for user_data in users:
            if username == user_data['email']:
                username = user_data['username']
                break
        print(username)
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
