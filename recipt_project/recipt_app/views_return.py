from . import views_return_forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from .sendmail_return import sendmail_return_py
from . import models  # Assuming this function saves customer data to DB
from . import models_return  # Assuming this function saves customer data to DB
from . import views_forms


def save_customer_recipt_return(request, new_recipt):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))
    customer_name = request.session.get("customer_name")
    customer_email = request.session.get("customer_email")
    recipt_code = request.session.get("recipt_code")
    recipt_code_buy=request.session.get("recipt_code_buy")
    date_time = datetime.now()
    total_price = request.session.get("total_price")
    products = request.session.get("products")

    if request.user.first_name and request.user.last_name:
        Employ_name = f"{request.user.first_name} {request.user.last_name} ({request.user.last_name})"
    else:
        Employ_name = request.user.username

    try:
        models_return.save_customer_recipt_return_to_db(customer_name,customer_email,Employ_name, recipt_code_buy,recipt_code, date_time, total_price, products)
    except Exception as e:
        return render(request, 'recipt/error.html', {
                        "error": f"Error saving receipt: {e}"
                        })
        
    # Redirect or return a valid response
    if new_recipt == 1:
        return redirect("recipt:new_receipt", return_product=1)
    else:
        # return HttpResponse("Customer data saved successfully.")
        return redirect("recipt:index")
# View to send email and handle success/error scenarios
def sendmail_return(request, new_recipt):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
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
    # Ensure session data exists
    if not user_data['products'] or not user_data['customer_name'] or not user_data['customer_email']:
        return HttpResponse("Required session data is missing.", status=400)

    # Send email and handle response from sendmail_py
    result = sendmail_return_py(user_data)
    if result.startswith("Error"):
        # Redirect to edit_customer with the customer's name and email as URL parameters
        return redirect('recipt:edit_customer', customer_name=user_data['customer_name'], customer_email=user_data['customer_email'])

    elif result == "Success":
        # Save customer data before sending email
        return save_customer_recipt_return(request, new_recipt)

    else:
        # Handle unexpected issues during email sending
        return render(request, 'recipt/error.html', {
                        "error": f"An unexpected issue occurred while sending the email. to {user_data['customer_name']} on {user_data['customer_email']}."
                        })

    # Catch-all return, ensuring we never return None
    return HttpResponse("Unexpected error.", status=500)

def return_product(request):
    try:
        # Ensure user is authenticated and has the correct role
        if not request.user.is_authenticated or (
            models.select_userdata(request.user.username)[1] not in ["counter manager", "administration manager"]
        ):
            return HttpResponseRedirect(reverse("recipt:login"))

        # Retrieve receipt code from session, if available
        recipt_code_buy = request.session.get("recipt_code_buy", None)

        if request.method == 'POST':
            form_return_product = views_return_forms.returnProduct(request.POST)

            if not recipt_code_buy:
                form_return_product_recipt_code = views_return_forms.return_product_recipt_code(request.POST)
            else:
                form_return_product_recipt_code = views_return_forms.return_product_recipt_code()

            # Validate both forms
            if form_return_product.is_valid() and (form_return_product_recipt_code.is_valid() or recipt_code_buy):
                prod_code = form_return_product.cleaned_data['prod_code']
                quantity = form_return_product.cleaned_data['quantity']

                if not recipt_code_buy:
                    recipt_code_buy = form_return_product_recipt_code.cleaned_data['recipt_code_buy']
                    if not models.table_exists(recipt_code_buy):
                        return render(request, 'recipt/error.html', {"error": "Buy receipt does not exist."})

                    request.session["recipt_code_buy"] = recipt_code_buy

                    # Fetch customer details
                    customer = models.get_customer_recipt(recipt_code_buy)
                    
                    request.session["customer_name"] = customer[1] if customer else ""
                    request.session["customer_email"] = customer[2] if customer else ""

                # Fetch product receipt details
                product_recipt = models.get_recipt_product(recipt_code_buy, prod_code)
                if not product_recipt:
                    return render(request, 'recipt/error.html', {"error": "Product does not exist."})

                # Check if quantity is valid
                if product_recipt[3] < quantity:
                    return render(request, 'recipt/error.html', {"error": "Insufficient quantity in receipt."})

                # Calculate quantity price
                quantity_price = product_recipt[4] * quantity
                product_found = False

                # Update session data for the product
                for product in request.session.get("products", []):
                    if product[0] == prod_code:
                        product[1] += quantity
                        product[3] += quantity_price
                        product_found = True
                        break

                if not product_found:
                    request.session.setdefault("products", []).append(
                        [prod_code, quantity, product_recipt[4], quantity_price, product_recipt[2]]
                    )

                # Update total price
                request.session["total_price"] = request.session.get("total_price", 0) + quantity_price

            else:
                return render(request, 'recipt/return_product.html', {
                    'form_product': form_return_product,
                    'form_recipt': form_return_product_recipt_code,
                    'error': 'Please provide valid product and receipt code.',
                })

        # Render the form for GET requests
        return render(request, 'recipt/return_product.html', {
            "form_product": views_return_forms.returnProduct(),
            'form_recipt': views_return_forms.return_product_recipt_code(),
            'recipt_code_buy': recipt_code_buy,
        })

    except models.DoesNotExist:
        return render(request, 'recipt/error.html', {"error": "Database operation failed."})
    except KeyError:
        return render(request, 'recipt/error.html', {"error": "Session data missing or corrupted."})
    except ValueError:
        return render(request, 'recipt/error.html', {"error": "Invalid input provided."})
    except Exception:
        return render(request, 'recipt/error.html', {"error": "An unexpected error occurred. Please try again later."})



# View to edit product details
def edit_product_return(request, id,recipt_code_buy):
    if not request.user.is_authenticated or ((models.select_userdata(request.user.username)[1] != "counter manager" and models.select_userdata(request.user.username)[1] != "administration manager")):
        return HttpResponseRedirect(reverse("recipt:login"))

    try:
        product = request.session["products"][id]
        prod_code, quantity, price, quantity_price,pro_descript = product
    except IndexError:
        return redirect('recipt:index')  # Redirect if invalid ID

    if request.method == 'POST':
        form_product = views_forms.ProductForm(request.POST)
        if form_product.is_valid():
            # Update session data
            new_prod_code = form_product.cleaned_data['prod_code']
            new_quantity = form_product.cleaned_data['quantity']
            
            product_recipt=models.get_recipt_product(recipt_code_buy,new_prod_code)
            if product_recipt:
                if new_quantity<= product_recipt[3]:
                    new_quantity_price = price * new_quantity
                    # Update the product
                    request.session["products"][id] = [new_prod_code, new_quantity, price, new_quantity_price,pro_descript ]
                    # Recalculate total price
                    request.session['total_price'] = sum(p[3] for p in request.session["products"])
                    return redirect('recipt:index')
                else:
                    return render(request, 'recipt/error.html', {
                        "error": f"product quantity not available ({product_recipt[3]})"
                        })
            else:
                return render(request, 'recipt/error.html', {
                    "error": f"product code ({prod_code}) is not available"
                    })
    else:
        form_product = views_forms.ProductForm(initial={'prod_code': prod_code, 'quantity': quantity})
    return render(request, 'recipt/add.html', {"form_product": form_product, 'is_editing_return': True, 'id': id ,'recipt_code_buy': recipt_code_buy})