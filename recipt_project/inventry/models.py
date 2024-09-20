from django.db import connection
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_each_item(prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime, username):
    """Inserts or updates product data in the product table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM dbo.product WHERE prod_code = %s", [prod_code])
            exists = cursor.fetchone()[0]

            if exists:
                # Update the existing record
                product=get_product(prod_code)
                if product[1] != prod_description or product[4] != quantity_price_sale or product[6] != username:
                    cursor.execute("""
                        UPDATE dbo.product
                        SET product_description = %s,
                            prod_quant = %s,
                            prod_sale_price = %s,
                            quantity_price_sale = %s,
                            updated_datetime = %s,
                            added_by_employ = %s
                        WHERE prod_code = %s
                    """, [prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime, username, prod_code])
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO dbo.product (prod_code, product_description, prod_quant, prod_sale_price, quantity_price_sale, updated_datetime, added_by_employ)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime, username])
    except IntegrityError as e:
        print(f"Error inserting/updating record: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@csrf_exempt
def get_product(prod_code):
    """Retrieves product data from the product table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dbo.product WHERE prod_code = %s", [prod_code])
            products = cursor.fetchall()
            return [list(product) for product in products]
    except Exception as e:
        print(f"Error fetching product data: {e}")
        return []

@csrf_exempt
def view_inventory(request):
    """Returns a list of products in the inventory."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dbo.product")
            products = cursor.fetchall()
            return [list(product) for product in products]
    except Exception as e:
        print(f"Error fetching product data: {e}")
        return []

def delete_item(prod_code):
    """Deletes a product from the product table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM dbo.product WHERE prod_code = %s", [prod_code])
        connection.commit()
    except Exception as e:
        print(f"Error while deleting product: {e}")
        connection.rollback()
