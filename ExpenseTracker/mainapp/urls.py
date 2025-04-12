from django.urls import path,include
from . import views
from mainapp.views import UserRegistrationView,UserLoginView,UserProfileView,homepage,UserExpenseView, QuickAddExpenseView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('expenses/', UserExpenseView.as_view(), name='expenses'),
    path('expenses/quick-add/', QuickAddExpenseView.as_view(), name='quick-add-expense'),
    path('', views.homepage, name=""),
    # path('register', views.register, name="register"),
    # path('my-login', views.my_login, name="my-login"),
    # path('dashboard', views.dashboard, name="dashboard"),
    # path('user_logout/', views.user_logout, name="user_logout"),
    # path('check_username/', views.check_username, name='check_username'),
    # path('verify-otp', views.verify_otp, name="verify_otp"),
]
