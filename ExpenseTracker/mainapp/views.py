from django.shortcuts import render,redirect
from django.http import HttpResponse
from . forms import CreateUserForm,LoginForm
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from mainapp.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSeializer,UserExpenseSerializer, QuickAddExpenseSerializer
from django.contrib.auth import authenticate
from mainapp.renderers import UserRenderer
from mainapp.models import UserExpense
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from datetime import date


# Authentication models and functions
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.core.mail import send_mail
from ExpenseTracker.settings import EMAIL_HOST_USER
import random
from django.views.decorators.csrf import  csrf_exempt




def homepage(request):
    return render(request, 'index/index.html')



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
     renderer_classes = [UserRenderer]
     def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token,"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token":token,"message": "User logged in successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid email & password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serialzer = UserProfileSeializer(request.user)
        return Response(serialzer.data, status=status.HTTP_200_OK)



class UserExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all user expenses"""
        expenses = UserExpense.objects.filter(user=request.user)
        serializer = UserExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new expense with a specified type"""
        serializer = UserExpenseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuickAddExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        data = request.data.copy()  # Make a copy of the request data
        data["expense_type"] = "others"  # Set default expense type to 'Others'
        data["date"] = str(date.today())  # Set today's date

        serializer = UserExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "Quick expense added under 'Others'"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# # # Create your views here.
# # def homepage(request):
# #     return render(request, 'index/index.html')

# # def register(request):
# #     form = CreateUserForm()
# #     if request.method == 'POST':
# #         email = request.POST.get('email')
# #         username = request.POST.get('username')
# #         last_name = request.POST.get('last_name')
# #         first_name = request.POST.get('first_name')
# #         password1 = request.POST.get('password1')
# #         password2 = request.POST.get('password2')
        
# #         form = CreateUserForm(request.POST)
# #         if form.is_valid():
# #             otp = random.randint(100000,999999)
# #             send_mail("User Data: ",f"Verify your ExpenseTracker account using this OTP: {otp}", EMAIL_HOST_USER,[email],fail_silently=True)
# #             return render(request, 'registration/otp.html',{'otp':otp,'first_name':first_name,'last_name':last_name,'email':email,'username':username,"password1":password1,'password2':password2})

# #     context = {'registerform':form}
# #     return render(request, 'registration/register.html',context)


# # @csrf_exempt
# # def verify_otp(request):
# #     if request.method == 'POST':
# #         email = request.POST.get('email')
# #         username = request.POST.get('username')
# #         last_name = request.POST.get('last_name')
# #         first_name = request.POST.get('first_name')
# #         password1 = request.POST.get('password1')
# #         password2 = request.POST.get('password2')

# #         if password1 == password2:
# #             user = User(
# #                 first_name=first_name,
# #                 last_name=last_name,
# #                 email=email,
# #                 username=username
# #             )
# #             user.set_password(password1)  # Encrypt the password
# #             user.save()

# #             send_mail(
# #                 "User Data: ",
# #                 "Your account has been created successfully",
# #                 EMAIL_HOST_USER,
# #                 [email],
# #                 fail_silently=True
# #             )

# #             return JsonResponse({'message': 'User created successfully'}, status=200)
    
# #     return JsonResponse({'error': 'Password mismatch'}, status=400)



# # def check_username(request):
# #     username = request.GET.get('username', '')
    
# #     # Check if the username is already taken
# #     username_taken = User.objects.filter(username=username).exists()
    
# #     # Generate suggestions if username is taken
# #     suggestions = []
# #     if username_taken:
# #         suggestions = [
# #             f"{username}{i}" for i in range(1, 6) if not User.objects.filter(username=f"{username}{i}").exists()
# #         ]
    
# #     return JsonResponse({
# #         'username_taken': username_taken,
# #         'suggestions': suggestions
# #     })


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
