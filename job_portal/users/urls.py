from django.urls import path
from .views import (
    employer_register,
    applicant_register,
    employer_dashboard,
    applicant_dashboard,
    dashboard,
    CustomLoginView,
)
from .views import custom_logout_view

urlpatterns = [
    # Registration URLs
    path('register/employer/', employer_register, name='employer_register'),
    path('register/applicant/', applicant_register, name='applicant_register'),
    
    # Dashboard URLs
    path('dashboard/employer/', employer_dashboard, name='employer_dashboard'),
    path('dashboard/applicant/', applicant_dashboard, name='applicant_dashboard'),
    path('dashboard/', dashboard, name='dashboard'),  # Shared dashboard
    
    # Authentication URLs
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
]