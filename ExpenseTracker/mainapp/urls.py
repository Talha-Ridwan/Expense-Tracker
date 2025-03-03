from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('check_username/', views.check_username, name='check_username'),
    path('verify-otp', views.verify_otp, name="verify_otp"),
]
