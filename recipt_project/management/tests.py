
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .import views_forms
from . import models
from django.http import HttpResponseRedirect
from django.contrib import messages
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class ChangePasswordForm(forms.Form):
    password_validator = RegexValidator(
        regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=+#%^()|}{;:/.>,<`~])[A-Za-z\d@$!%*?&_=+#%^()|}{;:/.>,<`~]{8,16}$',
        message="Password must be 8-16 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character."
    )

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'id_old_password',
            'placeholder': 'Enter old password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[password_validator]
    )

    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'id_new_password',
            'placeholder': 'Enter new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[password_validator]
    )

    confirm_new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_new_password',
            'placeholder': 'Confirm new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[password_validator]
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        return cleaned_data

def profile(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']

            # Validate old password against the user's current password
            if not check_password(old_password, request.user.password):
                return render(request, 'management/error.html', {
                        "error": "Your old password not correct."
                        })
            if confirm_new_password == new_password:
                # Save the new password
                request.user.set_password(new_password)
                request.user.save()
                return redirect('management:logout')
            else:
                return render(request, 'management/error.html', {
                        "error": "New password and confirm password do not match."
                        })
        else:
            return render(request, 'management/profile.html', {
                "form": form,
                "user_data": models.select_userdata(request.user.username),
                "django_userdata": [request.user.first_name, request.user.last_name, request.user.email],
            })

    form = ChangePasswordForm()
    django_userdata = [request.user.first_name, request.user.last_name, request.user.email]
    return render(request, 'management/profile.html', {
        "form": form,
        "user_data": models.select_userdata(request.user.username),
        "django_userdata": django_userdata,
    })
