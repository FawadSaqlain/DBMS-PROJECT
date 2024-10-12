from django.db import connection , DatabaseError
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

def search_products(search_column, search_value):
    with connection.cursor() as cursor:
        # Ensure the search column is valid to prevent SQL injection
        valid_columns = ['prod_code', 'product_description', 'prod_quant', 'prod_sale_price', 'quantity_price_sale', 'updated_datetime', 'added_by_employ']
        
        # If search_column is 'all', construct a different query
        if search_column == 'all':
            sql = """
            SELECT * FROM product
            WHERE LOWER(prod_code) LIKE LOWER(%s)
            OR LOWER(product_description) LIKE LOWER(%s)
            OR LOWER(CAST(prod_quant AS VARCHAR(50))) LIKE LOWER(%s)
            OR LOWER(CAST(prod_sale_price AS VARCHAR(50))) LIKE LOWER(%s)
            OR LOWER(CAST(quantity_price_sale AS VARCHAR(50))) LIKE LOWER(%s)
            OR LOWER(CAST(updated_datetime AS VARCHAR(50))) LIKE LOWER(%s)
            OR LOWER(CAST(added_by_employ AS VARCHAR(50))) LIKE LOWER(%s)
            """
            like_value = f'%{search_value}%'
            cursor.execute(sql, [like_value] * 7)  # Repeat the like_value for all 7 placeholders
        else:
            # Validate the search column
            if search_column not in valid_columns:
                raise ValueError("Invalid search column provided.")

            # Prepare the SQL query for a specific column
            if search_column == 'prod_quant':
                # For numeric fields, we need to ensure we convert to int
                try:
                    search_value = int(search_value)  # Convert to int for numeric fields
                except ValueError:
                    raise ValueError("Search value for quantity must be a valid integer.")

            sql = f"SELECT * FROM product WHERE LOWER(CAST({search_column} AS NVARCHAR(50))) LIKE LOWER(%s)"
            
            # Execute the query with the provided search value
            cursor.execute(sql, [f'%{search_value}%'])

        results = cursor.fetchall()
        return results
@csrf_exempt
def add_each_item(prod_code, prod_description, prod_quantity, prod_sale_price, quantity_price_sale, updated_datetime, username):
    # product=get_product(prod_code)
    # product=product[0]
    # print(f"line 51 product {product}")
    # print(f"line 63 condition for updating  if {product[1]} != {prod_description} or {product[4]} != {quantity_price_sale} or {product[6]} != {username}:")
    """Inserts or updates product data in the product table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM dbo.product WHERE prod_code = %s", [prod_code])
            exists = cursor.fetchone()[0]

            if exists:
                # Update the existing record
                product=get_product(prod_code)
                print(f"line 63 models.py product :: {product}")
                # product=product[0]
                print(f"line 64 condition for updating  if {product[1]} != {prod_description} or {product[4]} != {quantity_price_sale} or {product[6]} != {username}:")
                if product[1] != prod_description or product[4] != quantity_price_sale :
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
        print(f"line 81 Error inserting/updating record: {e}")
    except Exception as e:
        print(f"line 83 An unexpected error occurred: {e}")
@csrf_exempt
def get_product(prod_code):
    """Retrieves product data from the product table and returns a 1D list of the first product."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dbo.product WHERE prod_code = %s", [prod_code])
            products = cursor.fetchall()
            if products:
                print(f"live 95 product :: {products}")
                products =products[0]
                return products # Return the 1D list of the first product (index 0)
            else:
                return []  # Return an empty list if no products are found
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
        print(f"line 131 Error fetching product data: {e}")
        return []
def view_sorted_inventory(request, asc_decs, sort_by):
    """Returns a list of sorted products in the inventory."""
    try:
        with connection.cursor() as cursor:
            order = "ASC" if asc_decs == 0 else "DESC"
            query = f"SELECT * FROM Product ORDER BY {sort_by} {order}"
            cursor.execute(query)
            products = cursor.fetchall()
            return [list(product) for product in products]
    except Exception as e:
        print(f"line 143 Error fetching product data: {e}")
        return []
def delete_item(prod_code):
    """Deletes a product from the product table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM dbo.product WHERE prod_code = %s", [prod_code])
        connection.commit()
    except Exception as e:
        print(f"line 153 Error while deleting product: {e}")
        connection.rollback()


def select_userdata(username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT user_type FROM Employ WHERE username = %s"
            cursor.execute(query, [username])
            result = cursor.fetchone()  # Fetch the first row of the result
            if result:
                user_type = result[0]  # Extract the string from the tuple
                print("Data selected successfully:", user_type)
                return user_type
            else:
                print("No data found for the given username.")
                return ""  # Return an empty string if no data is found
    except DatabaseError as e:
        print(f"Error selecting data: {e}")
        return ""
