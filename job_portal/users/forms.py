from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class EmployerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'
        if commit:
            user.save()
        return user

class ApplicantSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'applicant'
        if commit:
            user.save()
        return user