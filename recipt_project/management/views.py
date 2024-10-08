# from django.contrib.auth import authenticate, login, logout 
# from django import forms
# from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
# from datetime import datetime
# import random
# import string
# from . import models
# #Full name, CNIC, phone number, email, address,
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib import messages

# class NewDataForm(forms.Form):
#     def for_edit_user(self, full_name, cnic, phone_number, email, address, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['full_name'].initial = full_name
#         self.fields['cnic'].initial = cnic
#         self.fields['phone_number'].initial = phone_number
#         self.fields['email'].initial = email
#         self.fields['address'].initial = address

#     full_name = forms.CharField(
#         max_length=100,  # Adjust the max_length as needed
#         widget=forms.TextInput(attrs={
#             'id': 'id_full_name',
#             'placeholder': 'Enter Full Name',
#             'class': 'form-control',
#             'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
#         })
#     )

#     cnic = forms.CharField(
#         max_length=15,  # Adjust max_length according to CNIC format
#         widget=forms.TextInput(attrs={
#             'id': 'id_cnic',
#             'placeholder': 'Enter CNIC',
#             'class': 'form-control',
#             'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
#         })
#     )

#     phone_number = forms.CharField(
#         max_length=15,  # Adjust max_length according to phone number format
#         widget=forms.TextInput(attrs={
#             'id': 'id_phone_number',
#             'placeholder': 'Enter Phone Number',
#             'class': 'form-control',
#             'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
#         })
#     )

#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'id': 'id_email',
#             'placeholder': 'Enter Email',
#             'class': 'form-control',
#             'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
#         })
#     )

#     address = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'id': 'id_address',
#             'placeholder': 'Enter Address',
#             'class': 'form-control',
#             'style': 'width: 100%; padding: 10px; margin-bottom: 10px; height: 100px;'  # Adjust height as needed
#         })
#     )

# def index(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("inventry:login"))

#     # Retrieve all users from the database
#     users = User.objects.all()

#     return render(request, 'inventry/index.html', {
#         "users": users,
#         'length_users': len(users)  # Pass the count of users to the template
#     })


# def add_user(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("inventry:login"))

#     # Ensure the session key 'users' is initialized
#     if "users" not in request.session:
#         request.session["users"] = []

#     if request.method == 'POST':
#         form = NewDataForm(request.POST)
#         if form.is_valid():
#             full_name = form.cleaned_data['full_name']
#             cnic = form.cleaned_data['cnic']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             address = form.cleaned_data['address']

#             # Create the new user
#             try:
#                 # Split full name into first name and last name
#                 first_name, last_name = full_name.split(' ', 1)
#                 # Create the User object
#                 user = User.objects.create_user(
#                     username=email,  # Use email as the username
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     password='defaultpassword123'  # Set a default password or implement a password field
#                 )
#                 user.save()
                
#                 messages.success(request, 'User created successfully!')
                
#                 # You can also call your existing inventory models here if needed
#                 user_description = "User created: " + full_name
#                 updated_datetime = datetime.now()

#             except Exception as e:
#                 messages.error(request, f'Error creating user: {str(e)}')
#                 return render(request, 'inventry/add.html', {'form': form})

#             return redirect(reverse("inventry:index"))  # Redirect to the index or any other page
#         else:
#             return render(request, 'inventry/add.html', {'form': form})

#     return render(request, 'inventry/add.html', {"form": NewDataForm()})

# #'''
# # def search_view(request):
# #     search_column = request.GET.get('section', ')  # Default search column
# #     search_value = request.GET.get('q', '')  # Retrieved search value
    
# #     # Convert search_value to string (if not already a string)
# #     search_value = str(search_value)
    
# #     print(f"line 77 search value :: {search_value} , search column :: {search_column}")

# #     results = []  # Initialize results list

# #     # Check if search_value is not empty
# #     if search_value:
# #         # If searching for quantity, check if it's a valid integer
# #         if search_column == 'user_quant':
# #             try:
# #                 # Validate if search_value is a valid integer
# #                 int(search_value)
# #             except ValueError:
# #                 return render(request, 'inventry/index.html', {
# #                     "users": [],
# #                     'length_users': range(0),
# #                     'error_message': "Search value for quantity must be a valid integer."
# #                 })
        
# #         # Call the model method to perform the search based on column and value
# #         results = models.search_users(search_column, search_value)

# #     # Render the template with search results
# #     return render(request, 'inventry/index.html', {
# #         "users": results,
# #         'length_users': range(len(results))
# #     })
# #'''
# #'''
# # def remove_user(request, user_index,:
# #     if not request.user.is_authenticated:
# #         return HttpResponseRedirect(reverse("inventry:login"))

# #     models.delete_item(
# #     print("line 138 deleted the user")
# #     return redirect('inventry:index')
# # def edit_user(request, user_index,:
# #     if not request.user.is_authenticated:
# #         return HttpResponseRedirect(reverse("inventry:login"))

# #     try:
# #         # Fetch the user details from the session
# #         user = models.get_user(
# #         # user=user[0]
# #         # print(f"before edit user is :: {user}")
# #          user_description, user_quantity, user_sale_price, quantity_price_sale, updated_datetime,username = user

# #     except IndexError:
# #         return redirect('inventry:index')  # Redirect if invalid index

# #     if request.method == 'POST':
# #         form = NewDataForm(request.POST)
# #         if form.is_valid():
# #             # Retrieve updated data from the form
# #             new_user_description = form.cleaned_data['user_description']
# #             new_user_sale_price = form.cleaned_data['user_sale_price']
# #             new_user_quantity = form.cleaned_data['user_quantity']
# #             new_quantity_price_sale = new_user_sale_price * new_user_quantity
# #             new_updated_datetime = datetime.now()
# #             # print("after edit user is ::", new_user_description, new_user_quantity, new_user_sale_price, new_quantity_price_sale, new_updated_datetime,f"{request.user.firstname} {request.user.lastname} ({request.user.username})")
# #             if request.user.first_name and request.user.last_name:
# #                 models.add_each_item( new_user_description, new_user_quantity, new_user_sale_price, new_quantity_price_sale, new_updated_datetime,f"{request.user.first_name} {request.user.last_name} ({request.user.username})")
# #             else :
# #                 models.add_each_item( new_user_description, new_user_quantity, new_user_sale_price, new_quantity_price_sale, new_updated_datetime,f" - - ({request.user.username})")
# #             return redirect('inventry:index')
# #         else:
# #             print(f"line 171 Form is invalid: {form.errors}")

# #     else:
# #         # If GET request, prepopulate the form with existing user details
# #         form = NewDataForm(initial={
# #             'user_description': user_description,
# #             'user_quantity': user_quantity,
# #             'user_sale_price': user_sale_price
# #         })

# #     return render(request, 'inventry/add.html', {
# #         "form": form,
# #         'is_editing': True,
# #         'user_index': user_index,
# #         ':  # Add this line
# #     })
# #'''

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("inventry:add"))
#         else:
#             return render(request, "inventry/login.html", {
#                 "message": "Invalid credentials.",
#                 "username": username  # Retain the entered username
#             })
#     return render(request, "inventry/login.html") 
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("inventry:login"))
