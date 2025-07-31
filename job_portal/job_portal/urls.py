from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Redirect root URL
@login_required
def home_redirect(request):
    """
    Redirect users to their respective dashboards based on their role.
    If unauthenticated, this will automatically redirect to the login page because of @login_required.
    """
    if request.user.role == 'employer':
        return redirect('employer_dashboard')
    elif request.user.role == 'applicant':
        return redirect('applicant_dashboard')
    else:
        return redirect('login')  # Fallback

urlpatterns = [
    path('', home_redirect, name='home'),  # Add this as the root URL
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include the users app URLs
    path('jobs/', include('jobs.urls')),    # Include the jobs app URLs
]