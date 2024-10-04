
# def return_product(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("recipt:login"))
    
#     if request.method == 'POST':
#         form_return_product = returnProduct(request.POST)
#         form_return_product_recipt_code = return_product_recipt_code(request.POST)
        
#         if form_return_product.is_valid() and form_return_product_recipt_code.is_valid():
            
#             prod_code = form_return_product.cleaned_data['prod_code']
#             quantity = form_return_product.cleaned_data['quantity']
#             recipt_code = form_return_product_recipt_code.cleaned_data['recipt_code']
            
#             # Fetch product from the receipt
#             product_recipt = models.get_recipt_product(recipt_code, prod_code)
            
#             # Check if product_recipt is None before accessing it
#             if product_recipt is None:
#                 # Handle the case where no product was found
#                 return render(request, 'recipt/return_product.html', {
#                     'form_product': form_return_product,
#                     'form_recipt': form_return_product_recipt_code,
#                     'error': 'Product not found in the receipt.'
#                 })

#             # Check if the available quantity in the receipt is enough
#             if product_recipt[2] >= quantity:
#                 quantity_price = product_recipt[3] * quantity
#                 product_found = False

#                 # Update session products_return or add a new one
#                 for product in request.session.get("products_return", []):
#                     if product[0] == prod_code:
#                         product[1] += quantity
#                         product[3] += quantity_price
#                         product_found = True
#                         break

#                 if not product_found:
#                     request.session["products_return"].append([prod_code, quantity, product_recipt[3], quantity_price, product_recipt[1]])

#                 # Save receipt code in the session
#                 if recipt_code:
#                     request.session["recipt_code"] = recipt_code
#             else:
#                 # Handle case where the requested quantity is not available
#                 return render(request, 'recipt/return_product.html', {
#                     'form_product': form_return_product,
#                     'form_recipt': form_return_product_recipt_code,
#                     'error': 'Requested quantity exceeds available quantity.'
#                 })

#         else:
#             return render(request, 'recipt/return_product.html', {
#                 'form_product': form_return_product,
#                 'form_recipt': form_return_product_recipt_code
#             })
    
#     return render(request, 'recipt/return_product.html', {
#         "form_product": returnProduct(), 
#         'form_recipt': return_product_recipt_code()
#     })

