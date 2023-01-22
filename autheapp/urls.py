from django.urls import path
from autheapp.views import EmployeeRegistrationView, EmployeeLoginView, EmployeeProfileView, EmployeeChangePasswordView, EmployeePasswordResetView, SendPasswordResetEmailView

urlpatterns = [
    path('register/',EmployeeRegistrationView.as_view(), name='register'),
    path('login/',EmployeeLoginView.as_view(), name='login'),
    path('profile/',EmployeeProfileView.as_view(), name='profile'),
    path('changepassword/', EmployeeChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', EmployeePasswordResetView.as_view(), name='reset-password'),
]