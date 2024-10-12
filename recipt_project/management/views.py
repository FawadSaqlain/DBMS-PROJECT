from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django import forms
from . import models
class NewDataForm(forms.Form):
    def for_edit_user(self,first_name ,last_name, cnic,phone_number,email,username,user_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = first_name
        self.fields['last_name'].initial = last_name
        self.fields['cnic'].initial = cnic
        self.fields['phone_number'].initial = phone_number
        self.fields['email'].initial = email
        self.fields['username'].initial = username
        self.fields['user_type'].initial = user_type
    USER_TYPE_CHOICES = [
        ('inventory_manager', 'Inventory Manager'),
        ('counter_manager', 'Counter Manager'),
        ('administration_manager', 'Administration Manager'),
    ]
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
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'style': 'margin-right: 10px; margin-bottom: 10px;'
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
    databasedata=models.select_alluserdata()
    return render(request, 'management/index.html', {
        "databasedata":databasedata,
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
            user_type = form.cleaned_data['user_type']

            try:
                # Create the user
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password='defaultpassword123'  # For demo; ideally generate/send password securely
                )
                
                models.save_userdata(username,cnic,phone_number,address,user_type)
                user.save()

                messages.success(request, 'User created successfully!')

                # Redirect to the index page
                # return redirect(reverse("management:index"))
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
                return render(request, 'management/add.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'management/add.html', {'form': form})

    return render(request, 'management/add.html', {"form": NewDataForm()})

# from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib import messages
# from .models import User  # Import your User model

# @csrf_exempt
def edit_user(request, user_index, username):
    # username = 'hamza'  # For testing
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))
    
    print(f"line 151 data is coming in edit_user {user_index} , {username}")
    user = User.objects.get(username=username)
    print(f"line 153 before saving {user}")
    user_data = models.select_userdata(username)  # Assuming this function retrieves user data including cnic, phone_number, user_type, etc.
    
    if request.method == 'POST':
        form = NewDataForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            cnic = form.cleaned_data['cnic']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            user_type = form.cleaned_data['user_type']
            
            print(f"before updating in edit_user models.save_userdata({username}, {cnic}, {phone_number}, {address}, {user_type})")
            models.save_userdata(username, cnic, phone_number, address, user_type)  # Update User and custom Employ model
            
            print(f"line 169 before saving {user}")
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
            'cnic': user_data[2],  # Assuming cnic is the 3rd column
            'phone_number': user_data[3],  # Assuming phone_number is the 4th column
            'user_type': user_data[1],  # Assuming user_type is the 2nd column
            'address': user_data[5],  # Assuming address is the 5th column
        })
    
    return render(request, 'management/add.html', {
        "form": form,
        'is_editing': True,
        'user_index': user_index,
        'username': username  # Fixed typo: 'usename' -> 'username'
    })

def remove_user(request, user_index,username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))

    try:
        user = User.objects.get(username=username)
        models.delete_userdata(username)
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