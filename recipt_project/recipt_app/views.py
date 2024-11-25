from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from .sendmail import sendmail_py
import random
import string
from django.views.decorators.csrf import csrf_exempt
from . import models  # Assuming this function saves customer data to DB
from django.contrib import messages
from django.contrib.auth.hashers import check_password
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
# Helper function to generate a random receipt number
def generate_random_key(length=5):
    characters = string.ascii_letters + string.digits
    random_key = ''.join(random.choices(characters, k=length))
    return "_" + random_key
# Form for adding/editing products
class ProductForm(forms.Form):
    def for_edit_product(self, code, quant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_code'].initial = code
        self.fields['quantity'].initial = quant

    prod_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_prod_code',
            'placeholder': 'Enter product code',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product quantity',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
# Form for adding/editing customer details
class CustomerForm(forms.Form):
    def for_edit_customer(self, customer_name, customer_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].initial = customer_name
        self.fields['customer_email'].initial = customer_email

    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Customer name',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Customer email',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )
def index(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))
    print(f"178 request :: {request}")

    # Initialize session variables if they do not exist
    if "products" not in request.session:
        request.session["products"] = []

    if "total_price" not in request.session:
        request.session["total_price"] = 0
    if "customer_name" not in request.session:
        request.session["customer_name"] = None
    if "customer_email" not in request.session:
        request.session["customer_email"] = None
    if "recipt_code_buy" not in request.session:
        request.session["recipt_code_buy"] = None
    if "recipt_code" not in request.session:
        request.session["recipt_code"] = generate_random_key()

    print(f"line 193 recipt_app/views.py request.session[products] = {request.session["products"]}")
    return render(request, 'recipt/index.html', {
        "products": request.session["products"],
        "total_price": request.session["total_price"],
        "customer_name": request.session["customer_name"],
        "customer_email": request.session["customer_email"],
        'range_5': range(len(request.session["products"])),
        'now': datetime.now(),
        'recipt_code': request.session["recipt_code"],
        'recipt_code_buy':request.session["recipt_code_buy"]
    })
# View to send email and handle success/error scenarios
def sendmail(request, new_recipt):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))

    # Retrieve user and session data
    user_data = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'products': request.session.get("products"),
        'total_price': request.session.get("total_price"),
        'customer_name': request.session.get("customer_name"),
        'customer_email': request.session.get("customer_email"),
        'recipt_code': request.session.get("recipt_code")
    }

    # Ensure session data exists
    if not user_data['products'] :
        # return HttpResponse("Required session data is missing.", status=400)
        return render(request, 'management/error.html', {
                        "error": f"Required session data is missing. product is {user_data['products']}"
                        })
    if not user_data['customer_name'] :
        # return HttpResponse("Required session data is missing.", status=400)
        return render(request, 'management/error.html', {
                        "error": f"Required session data is missing. customer name is {user_data['customer_name']}"
                        })
    if not user_data['customer_email']:
        # return HttpResponse("Required session data is missing.", status=400)
        return render(request, 'management/error.html', {
                        "error": f"Required session data is missing. customer email is {user_data['customer_email']}"
                        })
    # Send email and handle response from sendmail_py
    result = sendmail_py(user_data)
    print(f"line 228 Result from sendmail_py: {result}")  # Log the result for debugging

    if result.startswith("Error"):
        # Redirect to edit_customer with the customer's name and email as URL parameters
        return redirect('recipt:edit_customer', customer_name=user_data['customer_name'], customer_email=user_data['customer_email'])

    elif result == "Success":
        # Save customer data before sending email
        return save_customer_recipt(request, new_recipt)

    else:
        # Handle unexpected issues during email sending
        return render(request, 'recipt/redirect_popup.html', {
            'customer_name': user_data['customer_name'],
            'customer_email': user_data['customer_email'],
            'error': 'An unexpected issue occurred while sending the email.'
        })

    # Catch-all return, ensuring we never return None
    return HttpResponse("Unexpected error.", status=500)
# View to add new product and customer data to session
def add(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))
    
    if request.method == 'POST':
        form_product = ProductForm(request.POST)
        form_customer = CustomerForm(request.POST)
        if form_product.is_valid() and form_customer.is_valid():
            prod_code = form_product.cleaned_data['prod_code']
            quantity = form_product.cleaned_data['quantity']
            product_recipt = models.get_product(prod_code)
            if product_recipt:
                print(f"line 261 product recipt = {product_recipt}")
                if product_recipt[2] >= quantity:
                    quantity_price = product_recipt[3] * quantity
                    product_found = False

                    for product in request.session["products"]:
                        if product[0] == prod_code:
                            product[1] += quantity
                            product[3] += quantity_price
                            product_found = True
                            break

                    if not product_found:
                        request.session["products"].append([prod_code, quantity, product_recipt[3], quantity_price,product_recipt[1]])
                    request.session['total_price'] += quantity_price
                else:
                    return render(request, 'management/error.html', {
                        "error": f"product quantity not available ({product_recipt[2]})"
                        })
            else:
                return render(request, 'management/error.html', {
                        "error": "product code not available"
                        })
            customer_name = form_customer.cleaned_data['customer_name']
            customer_email = form_customer.cleaned_data['customer_email']
            if customer_name:
                request.session["customer_name"] = customer_name
            if customer_email:
                request.session["customer_email"] = customer_email

        else:
            return render(request, 'recipt/add.html', {'form_product': form_product, 'form_customer': form_customer})
    return render(request, 'recipt/add.html', {"form_product": ProductForm(), 'form_customer': CustomerForm()})
# View to start a new receipt
def new_receipt(request,return_product=0):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))

    # Reset session data for a new receipt
    request.session["products"] = []
    request.session["total_price"] = 0
    request.session["recipt_code_buy"]=None
    request.session["customer_name"] = None
    request.session["customer_email"] = None
    request.session["recipt_code"] = generate_random_key()
    if return_product:
        return redirect('recipt:return_product')
    else:
        return redirect('recipt:add')
# View to delete a product from the session
def dele(request, id):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))

    try:
        product = request.session["products"].pop(id)
        request.session['total_price'] -= product[3]  # Subtract the quantity_price
    except IndexError:
        return render(request, 'management/error.html', {
                        "error": f"Invalid index :: {IndexError}"
                        })# Handle index errors if necessary

    return redirect('recipt:index')
# View to edit customer details
def edit_customer(request, customer_name=None, customer_email=None):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_name = customer_form.cleaned_data['customer_name']
            customer_email = customer_form.cleaned_data['customer_email']
            request.session['customer_name'] = customer_name
            request.session['customer_email'] = customer_email
            return redirect('recipt:index')
    else:
        customer_form = CustomerForm(initial={'customer_name': customer_name, 'customer_email': customer_email})
    return render(request, 'recipt/edit_customer.html', {"customer_form": customer_form, "customer_name": customer_name, "customer_email": customer_email})

# View to edit product details
def edit_product(request, id):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))

    try:
        product = request.session["products"][id]
        prod_code, quantity, price, quantity_price,pro_descript = product
    except IndexError:
        return redirect('recipt:index')  # Redirect if invalid ID

    if request.method == 'POST':
        form_product = ProductForm(request.POST)
        if form_product.is_valid():
            # Update session data
            new_prod_code = form_product.cleaned_data['prod_code']
            new_quantity = form_product.cleaned_data['quantity']
            
            product_recipt = models.get_product(new_prod_code)
            print(f"** line 285 product_recipt :: {product_recipt} ")
            if product_recipt:
                if new_quantity<= product_recipt[2]:
                    new_quantity_price = price * new_quantity
                    # Update the product
                    request.session["products"][id] = [new_prod_code, new_quantity, price, new_quantity_price,pro_descript ]
                    # Recalculate total price
                    request.session['total_price'] = sum(p[3] for p in request.session["products"])
                    return redirect('recipt:index')
                else:
                    return render(request, 'management/error.html', {
                        "error": f"product quantity not available ({product_recipt[2]})"
                        })
            else:
                return render(request, 'recipt/error.html', {
                    "error": "product code is not available"
                    })
    else:
        form_product = ProductForm(initial={'prod_code': prod_code, 'quantity': quantity})
    return render(request, 'recipt/add.html', {"form_product": form_product, 'is_editing': True, 'id': id})
@csrf_exempt
def save_customer_recipt(request, new_recipt):
    customer_name = request.session.get("customer_name")
    customer_email = request.session.get("customer_email")
    recipt_code = request.session.get("recipt_code")
    date_time = datetime.now()
    total_price = request.session.get("total_price")
    products = request.session.get("products")

    if not customer_name or not customer_email or not recipt_code:
        # return HttpResponse("Customer data not provided.", status=400)
        # return render(request, 'management/error.html', {
        #                 "error": "Customer data not provided."
        #                 })
        pass

    if request.user.first_name and request.user.last_name:
        Employ_name = f"{request.user.first_name} {request.user.last_name} ({request.user.username})"
    else:
        Employ_name = request.user.username

    try:
        models.save_customer_recipt_to_db(customer_name, customer_email, Employ_name, recipt_code, date_time, total_price, products)
    except Exception as e:
        # print(f"line 387 Error saving receipt: {e}")
        # return HttpResponse("Error saving data to the database.", status=500)
        return render(request, 'management/error.html', {
                        "error": "Error saving receipt: {e}"
                        })
        
    # Redirect or return a valid response
    if new_recipt == 1:
        print('line 392 Going to new receipt after saving data')
        return HttpResponseRedirect(reverse("recipt:new_receipt", kwargs={'return_product': 0}))
        # return new_receipt(request,0)
    else:
        # return HttpResponse("Customer data saved successfully.")
        return redirect("recipt:index")
def profile(request):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))
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
                    return redirect('recipt:logout')
                else:
                    # return render(request, 'recipt/profile.html', {
                    #     "form": form,
                    #     "message": "Passwords do not match",
                    #     "user_data":user_data
                    #     })
                    return render(request, 'management/error.html', {
                        "error": "Passwords do not match"
                        })
            else:
                # return render(request, 'recipt/profile.html', {
                #     "form": form,
                #     "message": "Old password is incorrect",
                #     "user_data":user_data
                #     })
                return render(request, 'management/error.html', {
                        "error": "Old password is incorrect"
                        })
    return render(request, 'recipt/profile.html', {
                    "form": changepassword(),
                    "user_data":user_data
                    })
# Login and logout views
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(f"line 437 user name :: {username}")
        # , password :: {password}")
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            if (models.select_userdata(username)[1] == "counter manager" or models.select_userdata(username)[1] == "administration manager"):
                login(request, user)
                messages.success(request, 'This is a success TEST message!')
                return HttpResponseRedirect(reverse("recipt:new_receipt", kwargs={'return_product': 0}))
            else:
            #     return render(request, "recipt/login.html", {
            #     "message": "invalid permissions",
            #     "username": username  # Retain the entered username
            # })
                return render(request, 'management/error.html', {
                        "error": "invalid permissions"
                        })
        else:
            # return render(request, "recipt/login.html", {
            #     "message": "Invalid credentials.",
            #     "username": username  # Retain the entered username
            # })
            return render(request, 'management/error.html', {
                        "error": "invalid credentials"
                        })
    return render(request, "recipt/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("recipt:login"))

