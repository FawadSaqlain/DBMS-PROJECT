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
from django.contrib.auth.hashers import check_password

class NewDataForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('inventory manager', 'Inventory Manager'),
        ('counter manager', 'Counter Manager'),
        ('administration manager', 'Administration Manager'),
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
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_password',
            'placeholder': 'Enter password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_password',
            'placeholder': 'Enter confirm password',
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
class NewDataForm_edit(forms.Form):
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
        ('inventory manager', 'Inventory Manager'),
        ('counter manager', 'Counter Manager'),
        ('administration manager', 'Administration Manager'),
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
class changepassword(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_old_password',
            'placeholder': 'Enter old password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter confirm new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
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

            password=form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            try:
                # Create the user
                if(password==confirm_password):
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password  # For demo; ideally generate/send password securely
                    )
                    
                    models.save_userdata(username,cnic,phone_number,address,user_type)
                    user.save()

                    messages.success(request, 'User created successfully!')
                else:
                    messages.error(request, 'Passwords do not match!')
                # Redirect to the index page
                # return redirect(reverse("management:index"))
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
                return render(request, 'management/add.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'management/add.html', {'form': form})

    return render(request, 'management/add.html', {"form": NewDataForm()})
def edit_user(request, user_index, username):
    # username = 'hamza'  # For testing
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))
    
    # print(f"line 151 data is coming in edit_user {user_index} , {username}")
    user = User.objects.get(username=username)
    # print(f"line 153 before saving {user}")
    user_data = models.select_userdata(username)  # Assuming this function retrieves user data including cnic, phone_number, user_type, etc.
    if request.method == 'POST':
        form = NewDataForm_edit(request.POST)
        if form.is_valid():
            user.username=username
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
        if not user_data:
            form = NewDataForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username
        })
        else:
            form = NewDataForm_edit(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'cnic': user_data[2],  # Assuming cnic is the 3rd column
                'phone_number': user_data[3],  # Assuming phone_number is the 4th column
                'user_type': user_data[1],  # Assuming user_type is the 2nd column
                'address': user_data[5],  # Assuming address is the 5th column
            })
    print(f"line 196 username :: {username}")
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
        print(f"line 210 data is coming in edit_user {user_index} , {username}")
        user = User.objects.get(username=username)
    
        user = User.objects.get(username=username)
        print(f"line 214 before saving {user}")
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
        if user is not None and models.select_userdata(username)[1] == "administration manager":
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
def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:login"))
    user_data=models.select_userdata(request.user.username)
    if request.method == 'POST':
        form = changepassword(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']
            if check_password(old_password, request.user.password):
                if new_password==confirm_new_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    print("line 214 :: password is changed ")
                    # request.user.save() 
                    return redirect('management:logout')
                else:
                    return render(request, 'management/profile.html', {
                        "form": form,
                        "message": "Passwords do not match",
                        "user_data":user_data
                        })
            else:
                return render(request, 'management/profile.html', {
                    "form": form,
                    "message": "Old password is incorrect",
                    "user_data":user_data
                    })
    return render(request, 'management/profile.html', {
                    "message": "you are not changing the password",
                    "form": changepassword(),
                    "user_data":user_data
                    })
def user_sort(request,asc_decs,sort_by):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("inventry:login"))
    return redirect('management:index')
    # print(f"asc_decs,sortby :: {asc_decs},{sort_by}")
    # return render(request, 'inventry/index.html', {
    #     "products": models.view_sorted_user(request,asc_decs,sort_by),
    #     'length_products':range(len(models.select_alluserdata(request))),
    #     'sorted_as':f"{asc_decs}{sort_by}"
    # })
def search_user(request):
    search_column = request.GET.get('section', 'username')  # Default search column
    search_value = request.GET.get('q', '')  # Retrieved search value
    
    # Convert search_value to string (if not already a string)
    search_value = str(search_value)
    
    print(f"line 399 search value :: {search_value} , search column :: {search_column}")

    results = []  # Initialize results list

    # Check if search_value is not empty
    if search_value:
        results = models.search_user(search_column, search_value)
        databasedata , users =arange_user(results)
        print(f"line 408 ::{databasedata} {users}")
    # Render the template with search results
    return render(request, 'management/index.html', {
        "databasedata":databasedata,
        "users": users,
        'length_user': range(len(results))
    })
def arange_user(results):
    users=[]
    databasedata=[]
    for username in results:
        print(username)
        user_django = User.objects.get(username=username)
        user_database=models.select_userdata(username)
        users.append(user_django)
        databasedata.append(user_database)

    return databasedata, users
