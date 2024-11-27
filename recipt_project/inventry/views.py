from django.contrib.auth import authenticate, login, logout 
from . import views_forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
import random
import string
from . import models
from django.contrib.auth.hashers import check_password
import pandas as pd
from io import BytesIO

# Helper function to generate a random receipt number
def generate_random_key(length=5):
    characters = string.ascii_letters + string.digits
    random_key = ''.join(random.choices(characters, k=length))
    return random_key

def index(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))
    return render(request, 'inventry/index.html', {
        "products": models.view_inventory(request),
        # 'length_products':range(len(models.view_inventory(request)))
    })
def inventry_sort(request,asc_decs,sort_by):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))
    # print(f"asc_decs,sortby :: {asc_decs},{sort_by}")
    return render(request, 'inventry/index.html', {
        "products": models.view_sorted_inventory(request,asc_decs,sort_by),
        'length_products':range(len(models.view_inventory(request))),
        'sorted_as':f"{asc_decs}{sort_by}"
    })
def search_view(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))
    search_column = request.GET.get('section', 'product_code')  # Default search column
    search_value = request.GET.get('q', '')  # Retrieved search value
    
    # Convert search_value to string (if not already a string)
    search_value = str(search_value)
    
    print(f"line 77 search value :: {search_value} , search column :: {search_column}")

    results = []  # Initialize results list

    # Check if search_value is not empty
    if search_value:
        # If searching for quantity, check if it's a valid integer
        if search_column == 'prod_quant':
            try:
                # Validate if search_value is a valid integer
                int(search_value)
            except ValueError:
                # return render(request, 'inventry/index.html', {
                #     "products": [],
                #     'length_products': range(0),
                #     'error_message': "Search value for quantity must be a valid integer."
                # })
                return render(request, 'inventry/error.html', {
                        "error": "Search value for quantity must be a valid integer."
                        })
        
        # Call the model method to perform the search based on column and value
        results = models.search_products(search_column, search_value)

    # Render the template with search results
    return render(request, 'inventry/index.html', {
        "products": results,
        'length_products': range(len(results))
    })
def add(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))
    
    # Ensure the session key 'products' is initialized
    if "products" not in request.session:
        request.session["products"] = []

    if request.method == 'POST':
        form = views_forms.NewDataForm(request.POST)
        if form.is_valid():
            prod_code = generate_random_key()
            prod_description = form.cleaned_data['prod_description']
            prod_sale_price = form.cleaned_data['prod_sale_price']
            prod_quantity = form.cleaned_data['prod_quantity']
            quantity_price_sale = prod_sale_price * prod_quantity
            updated_datetime = datetime.now()
            # models.add_each_item(prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime,request.user.username)
            if request.user.first_name and request.user.last_name:
                models.add_each_item(prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime,f"{request.user.first_name} {request.user.last_name} ({request.user.username})")
            else :
                models.add_each_item(prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime,f" - - ({request.user.username})")

        else:
            return render(request, 'inventry/add.html', {'form': form})
    
    return render(request, 'inventry/add.html', {"form": views_forms.NewDataForm()})
def delet(request, prod_index,prod_code):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))

    models.delete_item(prod_code)
    print("line 138 deleted the product")
    return redirect('inventry:index')
def edit_product(request, prod_index,prod_code):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))

    try:
        # Fetch the product details from the session
        product = models.get_product(prod_code)
        # product=product[0]
        print(f"before edit product is :: {product}")
        prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime,username = product

    except IndexError:
        return redirect('inventry:index')  # Redirect if invalid index

    if request.method == 'POST':
        form = views_forms.NewDataForm(request.POST)
        if form.is_valid():
            # Retrieve updated data from the form
            new_prod_description = form.cleaned_data['prod_description']
            new_prod_sale_price = form.cleaned_data['prod_sale_price']
            new_prod_quantity = form.cleaned_data['prod_quantity']
            new_quantity_price_sale = new_prod_sale_price * new_prod_quantity
            new_updated_datetime = datetime.now()
            print("after edit product is ::",prod_code, new_prod_description, new_prod_quantity, new_prod_sale_price, new_quantity_price_sale, new_updated_datetime,f"{request.user.first_name} {request.user.last_name} ({request.user.username})")
            if request.user.first_name and request.user.last_name:
                models.add_each_item(prod_code, new_prod_description, new_prod_quantity, new_prod_sale_price, new_quantity_price_sale, new_updated_datetime,f"{request.user.first_name} {request.user.last_name} ({request.user.username})")
            else :
                models.add_each_item(prod_code, new_prod_description, new_prod_quantity, new_prod_sale_price, new_quantity_price_sale, new_updated_datetime,f" - - ({request.user.username})")
            return redirect('inventry:index')
        else:
            print(f"line 171 Form is invalid: {form.errors}")

    else:
        # If GET request, prepopulate the form with existing product details
        form = views_forms.NewDataForm(initial={
            'prod_description': prod_description,
            'prod_quantity': prod_quantity,
            'prod_sale_price': prod_sale_price
        })

    return render(request, 'inventry/add.html', {
        "form": form,
        'is_editing': True,
        'prod_index': prod_index,
        'prod_code': prod_code  # Add this line
    })
def export_excel(request):
    if request.method == "POST":
        # Extract products from the POST data
        raw_products = request.POST.getlist('products')  # List of serialized products
        if not raw_products:
            # return HttpResponse("No products available to export.", status=400)
            return render(request, 'inventry/error.html', {
                        "error": "No products available to export."
                        })

        # Deserialize products
        products = [product.split(',') for product in raw_products]

        # Define column names for the Excel file
        column_names = ['Product Code', 'Description', 'Quantity', 'Price', 'Total', 'Date Time', 'Updated By']

        # Convert products to a DataFrame
        df = pd.DataFrame(products, columns=column_names)

        # Create a BytesIO stream to save the Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')

        # Set up the response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="Inventory Products ({datetime.now().strftime("%Y-%m-%d/%H-%M-%S")}).xlsx"'

        return response
    else:
        return HttpResponse("Invalid request method.", status=405)
def profile(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "inventory manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("inventry:login"))
    user_data=models.select_userdata(request.user.username)
    if request.method == 'POST':
        form = views_forms.changepassword(request.POST)
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
                    return redirect('inventry:logout')
                else:
                    # return render(request, 'inventry/profile.html', {
                    #     "form": form,
                    #     "message": "Passwords do not match",
                    #     "user_data":user_data
                    #     })
                    return render(request, 'inventry/error.html', {
                        "error": "Passwords do not match"
                        })
            else:
                # return render(request, 'inventry/profile.html', {
                #     "form": form,
                #     "message": "Old password is incorrect",
                #     "user_data":user_data
                #     })
                return render(request, 'inventry/error.html', {
                    "error": "Old password is incorrect"
                    })
    return render(request, 'inventry/profile.html', {
                    "message": "",
                    "form": views_forms.changepassword(),
                    "user_data":user_data
                    })
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(f" models.select_userdata(username) :: {models.select_userdata(username)}")
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            if (models.select_userdata(username)[1] == "inventory manager" or models.select_userdata(username)[1] == "administration manager"):
                login(request, user)
                return HttpResponseRedirect(reverse("inventry:add"))
            else:
            #     return render(request, "inventry/login.html", {
            #     "message": "invalid permisions",
            #     "username": username  # Retain the entered username
            # })
                return render(request, 'inventry/error.html', {
                    "error": "invalid permisions"
                    })
        else:
            # return render(request, "inventry/login.html", {
            #     "message": "Invalid credentials.",
            #     "username": username  # Retain the entered username
            # })
            return render(request, 'inventry/error.html', {
                "error": "Invalid credentials."
                })
    return render(request, "inventry/login.html") 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("inventry:login"))