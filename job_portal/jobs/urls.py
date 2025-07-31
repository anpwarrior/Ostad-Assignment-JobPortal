from django.urls import path
from .views import post_job, edit_job, delete_job, job_listings, apply_job, job_detail, cancel_application

urlpatterns = [
    path('post/', post_job, name='post_job'),
    path('<int:job_id>/edit/', edit_job, name='edit_job'),
    path('<int:job_id>/delete/', delete_job, name='delete_job'),
    path('listings/', job_listings, name='job_listings'),  # Add this for browsing available jobs
    path('<int:job_id>/apply/', apply_job, name='apply_job'),
    path('<int:job_id>/detail/', job_detail, name='job_detail'),
    path('application/<int:application_id>/cancel/', cancel_application, name='cancel_application'),
]