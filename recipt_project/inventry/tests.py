from django.test import TestCase
from django.urls import reverse
from. import views
from django.http import HttpResponseRedirect, HttpResponse
import pandas as pd
# Create your tests here.
from django.http import HttpResponse
import csv
from datetime import datetime
import pandas as pd
from io import BytesIO

def export_excel(request):
    if request.method == "POST":
        # Extract products from the POST data
        raw_products = request.POST.getlist('products')  # List of serialized products
        if not raw_products:
            return HttpResponse("No products available to export.", status=400)

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
