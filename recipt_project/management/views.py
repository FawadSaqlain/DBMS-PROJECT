from django.contrib.auth import authenticate, login, logout
from . import views_forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from django.contrib.auth.hashers import check_password
import pandas as pd
from .sales_report import generate_report

def index(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))

    users = User.objects.all()
    databasedata=models.select_alluserdata()
    return render(request, 'management/index.html', {
        "databasedata":databasedata,
        "users": users,
        'length_users': len(users)
    })
def add_user(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))

    if request.method == 'POST':
        form = views_forms.NewDataForm(request.POST)
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
                    # messages.error(request, 'Passwords do not match!')
                    return render(request, 'management/error.html', {
                    "error": "Passwords do not match!"
                    })
                # Redirect to the index page
                # return redirect(reverse("management:index"))
            except Exception as e:
                # messages.error(request, f'Error creating user: {str(e)}')
                return render(request, 'management/error.html', {
                    "error": "Passwords do not match!"
                    })
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'management/add.html', {'form': form})

    return render(request, 'management/add.html', {"form": views_forms.NewDataForm()})
def edit_user(request, user_index, username):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    
    user = User.objects.get(username=username)
    user_data = models.select_userdata(username)  # Assuming this function retrieves user data including cnic, phone_number, user_type, etc.
    if request.method == 'POST':
        form = views_forms.NewDataForm_edit(request.POST)
        try:
            if form.is_valid():
                user.username=username
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                password=form.cleaned_data['password']
                confirm_password=form.cleaned_data['confirm_password']
                cnic = form.cleaned_data['cnic']
                phone_number = form.cleaned_data['phone_number']
                address = form.cleaned_data['address']
                user_type = form.cleaned_data['user_type']
                models.save_userdata(username, cnic, phone_number, address, user_type)  # Update User and custom Employ model
                if ((password or confirm_password) and (password==confirm_password)):
                    user.set_password(password)
                elif ((password or confirm_password) and (password!=confirm_password)):
                    return render(request, 'management/error.html', {
                        "error": "password and confirm password miss matches."
                        })
                user.save()
                messages.success(request, 'User updated successfully!')
                return redirect('management:index')
        except Exception as e:
                # messages.error(request, 'Please correct the errors below.')
                return render(request, 'management/error.html', {
                        "error": f"Please correct the errors . {e}"
                        })
    else:
        if not user_data:
            form = views_forms.NewDataForm_edit(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username
        })
        else:
            form = views_forms.NewDataForm_edit(initial={
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
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))

    try:
        user = User.objects.get(username=username)
        user = User.objects.get(username=username)
        models.delete_userdata(username)
        user.delete()
        messages.success(request, f"User '{username}' has been deleted.")
        
    except User.DoesNotExist:
        # messages.error(request, f"User '{username}' not found.")
        return render(request, 'management/error.html', {
                    "error": f"User '{username}' not found."
                    })
    
    return redirect('management:index')

def profile(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    if request.method == 'POST':
        form = views_forms.ChangePasswordForm(request.POST)
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

    form = views_forms.ChangePasswordForm()
    django_userdata = [request.user.first_name, request.user.last_name, request.user.email]
    return render(request, 'management/profile.html', {
        "form": form,
        "user_data": models.select_userdata(request.user.username),
        "django_userdata": django_userdata,
    })

def search_user(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    search_column = request.GET.get('section', 'username')  # Default search column
    search_value = request.GET.get('q', '')  # Retrieved search value
    
    # Convert search_value to string (if not already a string)
    search_value = str(search_value)
    results = []  # Initialize results list

    # Check if search_value is not empty
    if search_value:
        results = models.search_user(search_column, search_value)
        databasedata , users =arange_user(results)
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

def user_sort(request,asc_decs,sort_by):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))

    # Define valid fields for sorting in Django
    valid_fields_in_django = ['username', 'email', 'first_name', 'last_name']
    
    # Check if sorting is on a valid field
    if sort_by not in valid_fields_in_django:
        # Use custom sorting if the field is not in Django's User model
        user_names_list = models.view_sorted_user(request, asc_decs, sort_by)
        # Flatten the list in case of nested structure
        user_names = [username for sublist in user_names_list for username in sublist]
    else:
        # Define sort asc_decs (ascending or descending)
        sort_order = f'-{sort_by}' if asc_decs == 1 else sort_by
        user_names = User.objects.all().order_by(sort_order).values_list('username', flat=True)

    completedata_database = []
    completedata_django = []

    # Process each username to gather additional information
    for username in user_names:
        username = username.strip("[]'")  # Ensure clean username strings        
        try:
            # Fetch database information
            completedata_database.append(models.select_userdata(username))
            
            # Fetch Django's User model information
            user = User.objects.get(username=username)
            completedata_django.append(user)
        
        except User.DoesNotExist:
            return render(request, 'management/error.html', {
                    "error": f"User with username '{username}' does not exist."
                    })
        except Exception as e:
            print(f"Error selecting data: {e}")
            return render(request, 'management/error.html', {
                    "error": f"Error selecting data: {e}"
                    })

    # Render response with both sets of data
    return render(request, 'management/index.html', {
        "databasedata": completedata_database,
        'users': completedata_django,
        'length_users': range(len(models.select_alluserdata())),
        'sorted_as': f"{asc_decs}{sort_by.lstrip('-')}"
    })
def sales_report_view(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    chart_url = None

    if request.method == "POST":
        try:
            frequency = request.POST.get('frequency')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            if frequency and start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)

                if frequency == 'daily':
                    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                elif frequency == 'monthly':
                    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                    end_date = end_date + pd.offsets.MonthEnd(0)
                elif frequency == 'yearly':
                    end_date = end_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

                chart_url = generate_report(frequency, start_date, end_date)
        except ValueError as ve:
            # print(f"Date parsing error: {ve}")
            return render(request, 'management/error.html', {
                        "error": f"Date parsing error: {ve}"
                        })
        except Exception as e:
            print(f"Unexpected error: {e}")
            return render(request, 'management/error.html', {
                        "error": f"Unexpected error: {e}"
                        })
    return render(request, 'management/sales_report.html', {'chart_url': chart_url})
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("management:logout"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None :
            if models.select_userdata(username)[1] == "administration manager":
                login(request, user)
                return HttpResponseRedirect(reverse("management:index"))
            else:
                return render(request, 'management/error.html', {
                        "error": "Invalid Permissions."
                        })
        else:
            # messages.error(request, "Invalid credentials.")
            return render(request, 'management/error.html', {
                        "error": "Invalid credentials."
                        })
    return render(request, "management/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("management:login"))

def customer_sort(request,asc_decs,sort_by):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    customer_buy, customer_return = models.get_customer_data()
    customer_buy=models.view_customer_sort(asc_decs,sort_by)
    return render(request,"management/customer_table.html",{"customer_buy":customer_buy,'sorted_as':f"{asc_decs}{sort_by}","customer_return":customer_return})

def customer_search(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    search_column = request.GET.get('section')  # Default search column
    search_value = request.GET.get('q', '')  # Retrieved search value
    
    # Convert search_value to string (if not already a string)
    search_value = str(search_value)
    
    customer_buy = []  # Initialize customer_buy list
    customer_return = []  # Initialize customer_return list

    # Check if search_value is not empty
    if search_value:
        customer_buy_code = models.get_customer_buy_buy_recipt_code_search(search_column, search_value)
        customer_return_code = models.get_customer_return_buy_recipt_code_search(search_column, search_value)
        
        for code in customer_buy_code:
            customer_buy.append(models.get_customer_buy_data(code))
            
        
        for code in customer_return_code:
            if models.get_customer_return_data(code) not in customer_return:
                customer_return.append(models.get_customer_return_data(code))
            if models.get_customer_buy_data(code) not in customer_buy:
                customer_buy.append(models.get_customer_buy_data(code))

        flattened_customer_buy = [item for sublist in customer_buy for item in sublist]
        # Flatten customer_return
        flattened_customer_return = [item for sublist in customer_return for item in sublist]
        
        

    return render(request, 'management/customer_table.html',
                {'customer_buy': flattened_customer_buy,'customer_return': flattened_customer_return})


def customerdata(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    customer_buy , customer_return = models.get_customer_data()
    return render(request, 'management/customer_table.html',
                {'customer_buy': customer_buy,'customer_return': customer_return})


def get_recipt(request,code,table_name):
    recipt=models.get_table_recipt(code)
    customer=models.get_customer_by_recipt_code(code , table_name)
    customer_return=models.get_customer_return_data(code)
    return render(request,"management/recipt.html",{"recipt":recipt,'customer':customer,'customer_return':customer_return})
