from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from .sendmail import sendmail_py
from .sendmail_return import sendmail_return_py
import random
import string
from django.views.decorators.csrf import csrf_exempt
from . import models  # Assuming this function saves customer data to DB
from . import models_return  # Assuming this function saves customer data to DB
from django.contrib import messages

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
class returnProduct(forms.Form):
    def for_edit_return_product(self, prod_code, quantity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_code'].initial = prod_code
        self.fields['quantity'].initial = quantity

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
class return_product_recipt_code(forms.Form):
    recipt_code_buy = forms.CharField(
        required=False,  # Make it not required because it will only be asked once
        widget=forms.TextInput(attrs={
            'placeholder': 'Receipt Code',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )

    def for_edit_recipt_code(self, recipt_code_buy, *args, **kwargs):
        """Set the receipt code if it's being edited or provided in the session."""
        super().__init__(*args, **kwargs)
        self.fields['recipt_code_buy'].initial = recipt_code_buy
def return_product(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))

    # Get the receipt code from session or None
    recipt_code_buy = request.session.get("recipt_code_buy", None)

    if request.method == 'POST':
        form_return_product = returnProduct(request.POST)
        
        # If there's no receipt code in the session, process the receipt code form
        if not recipt_code_buy:
            form_return_product_recipt_code = return_product_recipt_code(request.POST)
        else:
            # Otherwise, use the receipt code from session and don't show the form
            form_return_product_recipt_code = return_product_recipt_code()

        # Validate both forms
        if form_return_product.is_valid() and (form_return_product_recipt_code.is_valid() or recipt_code_buy):
            # Get product code and quantity
            prod_code = form_return_product.cleaned_data['prod_code']
            quantity = form_return_product.cleaned_data['quantity']

            # Get or save the receipt code
            if not recipt_code_buy:
                recipt_code_buy = form_return_product_recipt_code.cleaned_data['recipt_code_buy']
                request.session["recipt_code_buy"] = recipt_code_buy
                customer=models.get_customer_recipt(request.session["recipt_code_buy"])
                request.session["customer_name"]=customer[1]
                request.session["customer_email"]=customer[2]


            # Fetch product receipt details based on receipt code and product code
            product_recipt = models.get_recipt_product(recipt_code_buy, prod_code)
            if product_recipt:
                if product_recipt[3] >= quantity:
                    quantity_price = product_recipt[4] * quantity
                    product_found = False

                    # Check if the product already exists in the session products list
                    for product in request.session["products"]:
                        if product[0] == prod_code:
                            product[1] += quantity  # Update quantity
                            product[3] += quantity_price  # Update total price
                            product_found = True
                            break

                    if not product_found:
                        # Add the new product to the session list
                        request.session["products"].append([prod_code, quantity, product_recipt[4], quantity_price, product_recipt[2]])
                    
                    # Update total price
                    request.session['total_price'] += quantity_price

            # If the receipt code is present (from POST or session), save it in the session
            if recipt_code_buy:
                request.session["recipt_code_buy"] = recipt_code_buy
                customer=models.get_customer_recipt(request.session["recipt_code_buy"])
                request.session["customer_name"]=customer[1]
                request.session["customer_email"]=customer[2]
        else:
            # Render the form again with errors
            return render(request, 'recipt/return_product.html', {
                'form_product': form_return_product,
                'form_recipt': form_return_product_recipt_code,
                'error': 'Please provide valid product and receipt code.'
            })

    # Render the form for GET requests
    return render(request, 'recipt/return_product.html', {
        "form_product": returnProduct(),
        'form_recipt': return_product_recipt_code(),
        'recipt_code_buy': request.session.get("recipt_code_buy", None)  # Pass the receipt code if present
    })
# Main view for displaying receipt details
def index(request):
    if not request.user.is_authenticated:
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
    if not request.user.is_authenticated:
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
    if not user_data['products'] or not user_data['customer_name'] or not user_data['customer_email']:
        return HttpResponse("Required session data is missing.", status=400)

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
# View to send email and handle success/error scenarios
def sendmail_return(request, new_recipt):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))

    # Retrieve user and session data
    user_data = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'products': request.session.get("products"),
        'total_price': request.session.get("total_price"),
        'total_price_bought': models.get_customer_recipt(request.session["recipt_code_buy"])[5],
        'customer_name': request.session.get("customer_name"),
        'customer_email': request.session.get("customer_email"),
        'recipt_code': request.session.get("recipt_code"),
        'recipt_code_buy':request.session.get("recipt_code_buy"),
        'bought_product':models.get_table(request.session["recipt_code_buy"])
    }
    
    print(f"270 recipt buy :: {request.session["recipt_code_buy"]} model bought :: {models.get_table(request.session["recipt_code_buy"])}")
    print(f"271 product return :: {user_data['products']}")
    print(f"272 product bought :: {user_data['bought_product']}")

    # Ensure session data exists
    if not user_data['products'] or not user_data['customer_name'] or not user_data['customer_email']:
        return HttpResponse("Required session data is missing.", status=400)

    # Send email and handle response from sendmail_py
    result = sendmail_return_py(user_data)
    print(f"line 228 Result from sendmail_py: {result}")  # Log the result for debugging

    if result.startswith("Error"):
        # Redirect to edit_customer with the customer's name and email as URL parameters
        return redirect('recipt:edit_customer', customer_name=user_data['customer_name'], customer_email=user_data['customer_email'])

    elif result == "Success":
        # Save customer data before sending email
        return save_customer_recipt_return(request, new_recipt)

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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))
    
    if request.method == 'POST':
        form_product = ProductForm(request.POST)
        form_customer = CustomerForm(request.POST)
        if form_product.is_valid() and form_customer.is_valid():
            prod_code = form_product.cleaned_data['prod_code']
            quantity = form_product.cleaned_data['quantity']
            product_inventry = models.get_product(prod_code)
            print(f"line 261 product inventry = {product_inventry}")
            if product_inventry[2] >= quantity:
                quantity_price = product_inventry[3] * quantity
                product_found = False

                for product in request.session["products"]:
                    if product[0] == prod_code:
                        product[1] += quantity
                        product[3] += quantity_price
                        product_found = True
                        break

                if not product_found:
                    request.session["products"].append([prod_code, quantity, product_inventry[3], quantity_price,product_inventry[1]])
                request.session['total_price'] += quantity_price

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
    if not request.user.is_authenticated:
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))

    try:
        product = request.session["products"].pop(id)
        request.session['total_price'] -= product[3]  # Subtract the quantity_price
    except IndexError:
        pass  # Handle index errors if necessary

    return redirect('recipt:index')
# View to edit customer details
def edit_customer(request, customer_name, customer_email):
    if not request.user.is_authenticated:
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
    if not request.user.is_authenticated:
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
            new_quantity_price = price * new_quantity

            # Update the product
            request.session["products"][id] = [new_prod_code, new_quantity, price, new_quantity_price,pro_descript ]

            # Recalculate total price
            request.session['total_price'] = sum(p[3] for p in request.session["products"])

            return redirect('recipt:index')
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
        return HttpResponse("Customer data not provided.", status=400)

    if request.user.first_name and request.user.last_name:
        Employ_name = f"{request.user.first_name} {request.user.last_name} ({request.user.last_name})"
    else:
        Employ_name = request.user.username

    try:
        models.save_customer_recipt_to_db(customer_name, customer_email, Employ_name, recipt_code, date_time, total_price, products)
    except Exception as e:
        print(f"line 387 Error saving receipt: {e}")
        return HttpResponse("Error saving data to the database.", status=500)
        
    # Redirect or return a valid response
    if new_recipt == 1:
        print('line 392 Going to new receipt after saving data')
        return HttpResponseRedirect(reverse("recipt:new_receipt", kwargs={'return_product': 0}))
        # return new_receipt(request,0)
    else:
        # return HttpResponse("Customer data saved successfully.")
        return redirect("recipt:index")
def save_customer_recipt_return(request, new_recipt):
    customer_name = request.session.get("customer_name")
    customer_email = request.session.get("customer_email")
    recipt_code = request.session.get("recipt_code")
    recipt_code_buy=request.session.get("recipt_code_buy")
    date_time = datetime.now()
    total_price = request.session.get("total_price")
    products = request.session.get("products")

    # if not customer_name or not customer_email or not recipt_code:
    #     return HttpResponse("Customer data not provided.", status=400)

    if request.user.first_name and request.user.last_name:
        Employ_name = f"{request.user.first_name} {request.user.last_name} ({request.user.last_name})"
    else:
        Employ_name = request.user.username

    try:
        models_return.save_customer_recipt_return_to_db(customer_name,customer_email,Employ_name, recipt_code_buy,recipt_code, date_time, total_price, products)
    except Exception as e:
        print(f"line 421 Error saving receipt: {e}")
        return HttpResponse("Error saving data to the database.", status=500)
        
    # Redirect or return a valid response
    if new_recipt == 1:
        print('line 426 Going to new receipt after saving data')
        return redirect("recipt:new_receipt", return_product=1)
    else:
        # return HttpResponse("Customer data saved successfully.")
        return redirect("recipt:index")
# Login and logout views
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(f"line 437 user name :: {username}")
        # , password :: {password}")
        user = authenticate(request, username=username, password=password)
        if (user is not None) and (models.select_userdata(username) == "counter manager" or models.select_userdata(username) == "administration manager"):
            login(request, user)
            messages.success(request, 'This is a success TEST message!')
            return HttpResponseRedirect(reverse("recipt:new_receipt", kwargs={'return_product': 0}))
        else:
            return render(request, "recipt/login.html", {
                "message": "Invalid credentials.",
                "username": username  # Retain the entered username
            })
    return render(request, "recipt/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("recipt:login"))

