# models.py

from django.db import connection , DatabaseError
from django.db import IntegrityError

def save_customer_recipt_to_db(customer_name, customer_email, employ_name, recipt_code, date_time, total_price, products):
    """
    Inserts or updates customer data in the customers table.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the record already exists
            cursor.execute("SELECT COUNT(*) FROM customers WHERE recipt_code = %s", [recipt_code])
            exists = cursor.fetchone()[0]

            if exists:
                # Update the existing record
                cursor.execute("""
                    UPDATE customers
                    SET name = %s, email = %s, Employ_name = %s, date_time = %s, total_price = %s
                    WHERE recipt_code = %s
                """, [customer_name, customer_email, employ_name, date_time, total_price, recipt_code])
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO customers (name, email, Employ_name, recipt_code, date_time, total_price) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [customer_name, customer_email, employ_name, recipt_code, date_time, total_price])
            
            create_table_recipt(recipt_code, products)
    
    except IntegrityError as e:
        # Handle any integrity errors
        print(f"line 34 Error inserting/updating record: {e}")
def get_product(prod_code):
    """Retrieves product data from the product table and returns the first product found."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dbo.product WHERE prod_code = %s", [prod_code])
            product = cursor.fetchone()  # Fetch the first result directly
            if product:
                return list(product)  # Return the product as a list
            else:
                return None  # Return None if no product is found
    except Exception as e:
        print(f"line 46 Error fetching product data: {e}")
        return None
def get_table(table_name):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            table_data = cursor.fetchall()
            if table_data:
                return [list(row) for row in table_data]  
            else:
                return None  
    except Exception as e:
        print(f"line 64 Error fetching table data: {e}")
        return None

def table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = %s;
        """, [table_name])
        exists = cursor.fetchone()[0]
        return exists == 1  # Returns True if the table exists, False otherwise
def update_quantity(quantity,update_quantity_price, prod_code):
    """
    Updates the quantity of a product in the inventory.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE product
                SET prod_quant = %s,
                quantity_price_sale = %s
                WHERE prod_code = %s
            """, [quantity,update_quantity_price, prod_code])
    except Exception as e:
        print(f"line 71 Error updating product quantity: {e}")
def insert_data(recipt_code, products):
    """
    Inserts product data into the receipt-specific table and updates product quantities.
    """
    try:
        # Assuming products is a list of dictionaries or lists with necessary product details
        for product in products:
            prod_code = product['prod_code'] if isinstance(product, dict) else product[0]
            quantity = product['quantity'] if isinstance(product, dict) else product[1]
            price = product['price'] if isinstance(product, dict) else product[2]
            price_quantity = product['price_quantity'] if isinstance(product, dict) else product[3]
            
            inventry_product = get_product(prod_code)
            if not inventry_product:
                continue  # Skip if product not found
            
            # inventry_product = inventry_product[0]
            current_quantity = inventry_product[2]  # Assuming this is prod_quant
            updated_quantity = current_quantity - quantity
            update_quantity_price = inventry_product[4] - price_quantity
            # Update the product quantity in the inventory
            update_quantity(updated_quantity,update_quantity_price, prod_code)
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO [{recipt_code}] (prod_code, prod_discreption, quantity, price, price_quantity) 
                    VALUES (%s, %s, %s, %s, %s)
                """, [prod_code, inventry_product[1], quantity, price, price_quantity])
    except Exception as e:
        print(f"line 101 Error inserting product data: {e}")
def update_recipt_customer(recipt_code_buy, total_price):
    """
    Updates the total_price for a customer based on their recipt_code.
    """
    try:
        with connection.cursor() as cursor:
            # Update the total_price for the customer with the given recipt_code
            cursor.execute("""
                UPDATE customers
                SET total_price = %s
                WHERE recipt_code = %s
            """, [total_price, recipt_code_buy])
    except Exception as e:
        print(f"line 125 Error updating recipt customer: {e}")
def restore_inventory_from_receipt(recipt_code):
    """
    Restores the inventory quantities from an existing receipt before dropping the table.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM [{recipt_code}]")
        products = cursor.fetchall()
        for product in products:
            prod_code = product[1]
            quantity = product[3]
            quanitiy_price=product[5]
            # Fetch current inventory quantity
            inventry_product = get_product(prod_code)
            if inventry_product:
                current_quantity = inventry_product[2]
                updated_quantity = current_quantity + quantity
                updated_quantity_price=inventry_product[4]+quanitiy_price
                # Update the product quantity in the inventory
                update_quantity(updated_quantity,updated_quantity_price, prod_code)
def create_table_recipt(recipt_code, products):
    """
    Creates a receipt-specific table and inserts bought product data.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the table exists
            if table_exists(recipt_code):
                # Restore inventory quantities from the existing receipt table
                restore_inventory_from_receipt(recipt_code)
                
                # Drop the existing receipt table
                cursor.execute(f"DROP TABLE [{recipt_code}]")
            
            # Create the new table
            cursor.execute(f"""
                CREATE TABLE [{recipt_code}] (
                    id INT PRIMARY KEY IDENTITY,
                    prod_code NVARCHAR(100),
                    prod_discreption NVARCHAR(1000),
                    quantity INT,
                    price FLOAT,
                    price_quantity FLOAT
                )
            """)
        
        # Insert data into the new table
        insert_data(recipt_code, products)
    except Exception as e:
        print(f"line 286 Error creating receipt table: {e}")
def update_recipt_product_quantity(recipt_code, prod_code, prod_quant,update_quantity_price_recipt):
    """
    Update the quantity of a specific product in a specific receipt.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the receipt table exists
            if table_exists(recipt_code):
                # Construct the query with the receipt table name directly
                query = f"""
                    UPDATE [{recipt_code}]
                    SET quantity = %s,
                    price_quantity=%s
                    WHERE prod_code = %s
                """
                cursor.execute(query, [prod_quant,update_quantity_price_recipt, prod_code])  # Use placeholders for prod_quant and prod_code
            else:
                print(f"line 335 Receipt table {recipt_code} does not exist.")
    except Exception as e:
        print(f"line 337 Error updating product quantity in receipt {recipt_code}: {e}")
def get_recipt_product(recipt_code, prod_code):
    """
    Get a receipt-specific product data as a single-dimensional list.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the receipt table exists
            if table_exists(recipt_code):
                # Construct the query with the receipt table name directly
                query = f"""
                    SELECT * FROM [{recipt_code}]
                    WHERE prod_code = %s
                """
                cursor.execute(query, [prod_code])  # Use placeholders for prod_code to prevent SQL injection
                result = cursor.fetchone()  # Fetch a single record
                
                if result:
                    return list(result)  # Convert tuple to list and return it
                else:
                    return None  # Return None if no result is found
    except Exception as e:
        print(f"line 359 Error fetching product data: {e}")
        return None
def get_customer_recipt(recipt_code):
    """
    Get a receipt-specific customer data as a single-dimensional list.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the table exists
            cursor.execute("""
                SELECT * FROM customers
                WHERE recipt_code = %s
            """, (recipt_code,))  # Include a comma to create a single-item tuple
            result = cursor.fetchone()  # Use fetchone() to get a single record
            if result:
                return list(result)  # Convert tuple to list and return it
            else:
                return None  # Return None if no result is found
    except Exception as e:
        print(f"line 397 Error fetching customer data: {e}")
        return None
def select_userdata(username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Employ WHERE username = %s"
            cursor.execute(query, [username])
            result = cursor.fetchone()  # Fetch the first row of the result
            if result:
                return result
            else:
                print("No data found for the given username.")
    except DatabaseError as e:
        print(f"Error selecting data: {e}")
