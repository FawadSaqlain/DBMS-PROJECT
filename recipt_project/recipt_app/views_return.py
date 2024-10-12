from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from .sendmail_return import sendmail_return_py
from . import models  # Assuming this function saves customer data to DB
from . import models_return  # Assuming this function saves customer data to DB

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

def save_customer_recipt_return(request, new_recipt):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("recipt:login"))
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
