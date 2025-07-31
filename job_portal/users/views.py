from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from jobs.models import Job, Application
from django.db.models import Q
from .forms import EmployerSignUpForm, ApplicantSignUpForm

def employer_register(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('employer_dashboard')  # Redirect to employer dashboard
    else:
        form = EmployerSignUpForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Employer'})

def applicant_register(request):
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('applicant_dashboard')  # Redirect to applicant dashboard
    else:
        form = ApplicantSignUpForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Applicant'})

@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':  # Ensure only employers can access this view
        return redirect('dashboard')

    # Fetch all jobs posted by the logged-in employer
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')  # Jobs sorted by most recent

    return render(request, 'users/employer_dashboard.html', {
        'jobs': jobs,  # Pass the jobs and their applications
    })

@login_required
def applicant_dashboard(request):
    if request.user.role != 'applicant':  # Ensure only applicants can access this view
        return redirect('dashboard')

    # Get all applications submitted by the logged-in user
    applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')

    # Fetch all available jobs (with optional search query)
    query = request.GET.get('q', '')  # Get search input from GET parameters
    jobs = Job.objects.filter(
        Q(title__icontains=query) | 
        Q(company_name__icontains=query) | 
        Q(location__icontains=query)
    ).order_by('-created_at')  # Fetch all jobs matching the search query

    # Create a set of job IDs that the user has already applied for
    applied_job_ids = set(applications.values_list('job_id', flat=True))

    return render(request, 'users/applicant_dashboard.html', {
        'applications': applications,  # Jobs the applicant has applied for
        'jobs': jobs,  # All jobs (matching search criteria)
        'applied_job_ids': applied_job_ids,  # IDs of jobs already applied for
        'query': query,  # Preserve search query in the search bar
    })

@login_required
def dashboard(request):
    """
    Redirects the user to their respective dashboard based on their role.
    """
    if request.user.role == 'employer':
        return redirect('employer_dashboard')
    elif request.user.role == 'applicant':
        return redirect('applicant_dashboard')
    else:
        return redirect('login')  # Fallback
    
class CustomLoginView(LoginView):
    """
    Override Django's LoginView to dynamically redirect users after login.
    This uses the LOGIN_REDIRECT_URL ('/') which further redirects users based on their role.
    """
    def get_success_url(self):
        return self.get_redirect_url() or '/'  # Redirect to root

def custom_logout_view(request):
    """
    Handle logout functionality.
    Redirects:
      - Authenticated users to the login screen after logging out.
      - Unauthenticated users trying to access '/users/logout/' to the login page.
    """
    # If the user is authenticated, log them out
    if request.user.is_authenticated:
        logout(request)  # Logs out the current user
        return redirect('login')  # Redirect to login
    
    # If already logged out, simply redirect to login
    return redirect('login')