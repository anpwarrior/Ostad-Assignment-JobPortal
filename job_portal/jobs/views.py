from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobForm, ApplicationForm
from django.contrib import messages
from jobs.models import Job, Application
from django.db.models import Q

@login_required
def post_job(request):
    if request.user.role != 'employer':  # Only employers can post jobs
        return redirect('dashboard')

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # Assign the current employer as the poster
            job.save()
            messages.success(request, "Job successfully posted!")
            return redirect('employer_dashboard')  # Redirect back to the dashboard after posting
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def edit_job(request, job_id):
    if request.user.role != 'employer':  # Only employers can edit jobs
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id, posted_by=request.user)  # Ensure the job belongs to the logged-in employer

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job successfully updated!")
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, job_id):
    if request.user.role != 'employer':  # Only employers can delete jobs
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id, posted_by=request.user)  # Ensure the job belongs to the logged-in employer
    job.delete()
    messages.success(request, "Job successfully deleted!")
    return redirect('employer_dashboard')

@login_required
def job_listings(request):
    if request.user.role != 'applicant':  # Ensure only applicants can access this functionality
        return redirect('dashboard')

    query = request.GET.get('q', '')  # Get search input from the GET parameter `?q=...`
    jobs = Job.objects.filter(
        Q(title__icontains=query) | 
        Q(company_name__icontains=query) | 
        Q(location__icontains=query)
    ).order_by('-created_at')  # Search across multiple fields and sort by most recent

    return render(request, 'jobs/job_listings.html', {
        'jobs': jobs,
        'query': query,  # Pass the search query back to the template
    })
 
@login_required
def apply_job(request, job_id):
    if request.user.role != 'applicant':  # Only applicants can apply
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id)  # Fetch the job or raise 404 if it doesn't exist

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)  # Include both POST data and FILES for resume upload
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job  # Link the application to the job
            application.applicant = request.user  # Link the application to the logged-in user
            application.save()
            messages.success(request, "You have successfully applied for the job!")
            return redirect('job_listings')
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_job.html', {
        'form': form,
        'job': job,
    })

@login_required
def job_detail(request, job_id):
    # Fetch the requested job or return 404 if not found
    job = get_object_or_404(Job, id=job_id)

    # Check if the logged-in user has already applied for this job
    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    # Handle apply action (via POST)
    if request.method == "POST" and not already_applied:
        # Create the application record
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, f"You have successfully applied for the job: {job.title}.")
        
        # Redirect to refresh the page and include back_url in the query string
        back_url = request.GET.get('back_url', '/users/dashboard/applicant/')  # Ensure back_url persists
        return redirect(f'{request.path}?back_url={back_url}')

    # Extract back_url from GET parameters or default to the Applicant Dashboard
    back_url = request.GET.get('back_url', '/users/dashboard/applicant/')

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'back_url': back_url,  # Pass the back URL to the template
    })

@login_required
def cancel_application(request, application_id):
    # Get the application, ensuring it belongs to the logged-in user
    application = get_object_or_404(Application, id=application_id, applicant=request.user)

    # Delete the application record
    application.delete()
    messages.success(request, f"Your application for '{application.job.title}' has been successfully canceled.")
    
    # Redirect back to the Applicant Dashboard
    return redirect('applicant_dashboard')

@login_required
def update_application_status(request, application_id):
    if request.method == 'POST':
        # Get the application object
        application = get_object_or_404(Application, id=application_id)

        # Get the status from the POST data
        status = request.POST.get('status')
        if status in ['accepted', 'rejected']:
            application.status = status
            application.save()
            messages.success(request, f"Application from {application.applicant.username} has been {status}.")
        else:
            messages.error(request, "Invalid status.")

    # Redirect back to the employer dashboard
    return redirect('employer_dashboard')