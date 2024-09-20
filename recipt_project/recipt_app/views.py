from django.contrib.auth import authenticate, login, logout 
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from .sendmail import viewsdata
import random
import string
from django.views.decorators.csrf import csrf_exempt
from .models import save_customer_to_db  # Assuming this function saves customer data to DB

# Helper function to generate a random receipt number
def generate_random_key(length=5):
    characters = string.ascii_letters + string.digits
    random_key = ''.join(random.choices(characters, k=length))
    return random_key

# Form for adding/editing products
class NewDataForm(forms.Form):
    def for_edit_product(self, nam, pric, quant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = nam
        self.fields['price'].initial = pric
        self.fields['quantity'].initial = quant

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_name',
            'placeholder': 'Enter product name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product price',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product quantity',
            'class': 'form-control',
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
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Customer email',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )

# Main view for displaying receipt details
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))

    # Initialize session variables if they do not exist
    if "products" not in request.session:
        request.session["products"] = []  # 2D list to store [name, quantity, price, quantity_price]
    if "total_price" not in request.session:
        request.session["total_price"] = 0
    if "customer_name" not in request.session:
        request.session["customer_name"] = None
    if "customer_email" not in request.session:
        request.session["customer_email"] = None
    if "recipt_no" not in request.session:
        request.session["recipt_no"] = generate_random_key()

    return render(request, 'recipt/index.html', {
        "products": request.session["products"],
        "total_price": request.session["total_price"],
        "customer_name": request.session["customer_name"],
        "customer_email": request.session["customer_email"],
        'range_5': range(len(request.session["products"])),
        'now': datetime.now(),
        'recipt_no': request.session["recipt_no"]
    })

# View to send email and handle success/error scenarios
def sendmail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))

    user_data = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'products': request.session.get("products"),
        'total_price': request.session.get("total_price"),
        'customer_name': request.session.get("customer_name"),
        'customer_email': request.session.get("customer_email"),
        'recipt_no': request.session["recipt_no"]
    }
    
    # Save customer data before sending email
    save_customer(request,0)
    
    # Send email and handle response
    result = viewsdata(user_data)
    print(f"Result from viewsdata: {result}")  # Log the result for debugging

    if result.startswith("Error"):
        # Redirect to edit_customer with the customer's name and email as URL parameters
        return redirect('recipt:edit_customer', customer_name=user_data['customer_name'], customer_email=user_data['customer_email'])
    elif result == "Success":
        # Render the redirect_popup.html template with customer details
        # return render(request, 'recipt/redirect_popup.html', {
        #     'customer_name': user_data['customer_name'],
        #     'customer_email': user_data['customer_email']
        # })
        return new_receipt(request)
        
    else:
        # Handle unexpected issues during email sending
        return render(request, 'recipt/redirect_popup.html', {
            'customer_name': user_data['customer_name'],
            'customer_email': user_data['customer_email'],
            'error': 'An unexpected issue occurred while sending the email.'
        })

# View to add new product and customer data to session
def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))
    
    if request.method == 'POST':
        form = NewDataForm(request.POST)
        form_customer = CustomerForm(request.POST)
        if form.is_valid() and form_customer.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            quantity_price = price * quantity
            request.session["products"].append([name, quantity, price, quantity_price])
            request.session['total_price'] += quantity_price

            customer_name = form_customer.cleaned_data['customer_name']
            customer_email = form_customer.cleaned_data['customer_email']
            if customer_name:
                request.session["customer_name"] = customer_name
            if customer_email:
                request.session["customer_email"] = customer_email

        else:
            return render(request, 'recipt/add.html', {'form': form, 'form_customer': form_customer})
    return render(request, 'recipt/add.html', {"form": NewDataForm(), 'form_customer': CustomerForm()})

# View to start a new receipt
def new_receipt(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))

    # Reset session data for a new receipt
    request.session["products"] = []
    request.session["total_price"] = 0
    request.session["customer_name"] = None
    request.session["customer_email"] = None
    request.session["recipt_no"] = generate_random_key()
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
        name, quantity, price, quantity_price = product
    except IndexError:
        return redirect('recipt:index')  # Redirect if invalid ID

    if request.method == 'POST':
        form = NewDataForm(request.POST)
        if form.is_valid():
            # Update session data
            new_name = form.cleaned_data['name']
            new_price = form.cleaned_data['price']
            new_quantity = form.cleaned_data['quantity']
            new_quantity_price = new_price * new_quantity

            # Update the product
            request.session["products"][id] = [new_name, new_quantity, new_price, new_quantity_price]

            # Recalculate total price
            request.session['total_price'] = sum(p[3] for p in request.session["products"])

            return redirect('recipt:index')
    else:
        form = NewDataForm(initial={'name': name, 'price': price, 'quantity': quantity})

    return render(request, 'recipt/edit_product.html', {"form": form, 'id': id})


@csrf_exempt
def save_customer(request, new_recipt):
    customer_name = request.session.get("customer_name")
    customer_email = request.session.get("customer_email")
    recipt_no = request.session.get("recipt_no")
    
    if request.user.first_name and request.user.last_name:
        Employ_name = f"{request.user.first_name} {request.user.last_name}"
    else:
        Employ_name = request.user.username

    if recipt_no:
        save_customer_to_db(customer_name, customer_email, Employ_name, recipt_no)
        
        # Redirect or return a valid response
        if new_recipt == 1:
            print('going to new recipt after saving data')
            return redirect("recipt:new_receipt")
        else:
            pass
            # return HttpResponse("Customer data saved successfully.")
    else:
        return HttpResponse("Customer data not provided.", status=400)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("recipt:new_receipt"))
        else:
            return render(request, "recipt/login.html", {
                "message": "Invalid credentials.",
                "username": username  # Retain the entered username
            })
    return render(request, "recipt/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("recipt:login"))