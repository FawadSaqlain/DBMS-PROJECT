from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django import forms

class NewDataForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_first_name',
            'placeholder': 'Enter first name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_last_name',
            'placeholder': 'Enter last name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    cnic = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'id': 'id_cnic',
            'placeholder': 'Enter CNIC',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'id': 'id_phone_number',
            'placeholder': 'Enter Phone Number',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'id_email',
            'placeholder': 'Enter Email',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_username',
            'placeholder': 'Enter username',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'id_address',
            'placeholder': 'Enter Address',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px; height: 100px;'  
        })
    )

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))

    users = User.objects.all()

    return render(request, 'management/index.html', {
        "users": users,
        'length_users': len(users)
    })

def add_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))

    if request.method == 'POST':
        form = NewDataForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            cnic = form.cleaned_data['cnic']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']

            try:
                # Create the user
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password='defaultpassword123'  # For demo; ideally generate/send password securely
                )
                user.save()

                messages.success(request, 'User created successfully!')

                # Redirect to the index page
                return redirect(reverse("management:index"))
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
                return render(request, 'management/add.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'management/add.html', {'form': form})

    return render(request, 'management/add.html', {"form": NewDataForm()})

def edit_user(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('management:index')

    if request.method == 'POST':
        form = NewDataForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            # Other fields to update can be added here
            user.save()

            messages.success(request, 'User updated successfully!')
            return redirect('management:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewDataForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            # Fetch other fields as needed
        })

    return render(request, 'management/edit.html', {
        "form": form,
        'is_editing': True
    })

def remove_user(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))

    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, f"User '{username}' has been deleted.")
    except User.DoesNotExist:
        messages.error(request, f"User '{username}' not found.")
    
    return redirect('management:index')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("management:index"))
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, "management/login.html", {
                "username": username
            })
    return render(request, "management/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("management:login"))

def search_view():
    pass