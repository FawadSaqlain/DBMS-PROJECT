# models.py

from django.db import connection
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
        print(f"Error inserting/updating record: {e}")

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
        print(f"Error fetching product data: {e}")
        return None
from django.db import connection

def table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = %s;
        """, [table_name])
        exists = cursor.fetchone()[0]
        return exists == 1  # Returns True if the table exists, False otherwise
def update_quantity(quantity, prod_code):
    """
    Updates the quantity of a product in the inventory.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE product
                SET prod_quant = %s
                WHERE prod_code = %s
            """, [quantity, prod_code])
            print(f"update_quantity {quantity},{prod_code}")
    except Exception as e:
        print(f"Error updating product quantity: {e}")
# def return_product(recipt_code,prod_code,prod_quant):
    
def insert_data(recipt_code, products):
    """
    Inserts product data into the receipt-specific table and updates product quantities.
    """
    try:
        # Assuming `products` is a list of dictionaries or lists with necessary product details
        for product in products:
            prod_code = product['prod_code'] if isinstance(product, dict) else product[0]
            quantity = product['quantity'] if isinstance(product, dict) else product[1]
            price = product['price'] if isinstance(product, dict) else product[2]
            price_quantity = product['price_quantity'] if isinstance(product, dict) else product[3]
            
            inventry_product = get_product(prod_code)
            if not inventry_product:
                print(f"Product with code {prod_code} not found.")
                continue  # Skip if product not found
            
            # inventry_product = inventry_product[0]
            current_quantity = inventry_product[2]  # Assuming this is `prod_quant`
            print(f"current quantity  {current_quantity}")
            updated_quantity = current_quantity - quantity
            print(f"updated quantity  {updated_quantity}")

            # Update the product quantity in the inventory
            print(f"inventry before updated {updated_quantity} , {prod_code}")
            update_quantity(updated_quantity, prod_code)
            print(f"inventry after updated {updated_quantity} , {prod_code}")
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO [{recipt_code}] (prod_code, prod_discreption, quantity, price, price_quantity) 
                    VALUES (%s, %s, %s, %s, %s)
                """, [prod_code, inventry_product[1], quantity, price, price_quantity])
    except Exception as e:
        print(f"Error inserting data into receipt table: {e}")
def table_exists(table_name):
    """
    Checks if a table exists in the database.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = %s;
        """, [table_name])
        exists = cursor.fetchone()[0]
        return exists == 1  # Returns True if the table exists, False otherwise

def restore_inventory_from_receipt(recipt_code):
    """
    Restores the inventory quantities from an existing receipt before dropping the table.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT prod_code, quantity FROM [{recipt_code}]")
        products = cursor.fetchall()
        for product in products:
            prod_code = product[0]
            quantity = product[1]
            # Fetch current inventory quantity
            inventry_product = get_product(prod_code)
            if inventry_product:
                current_quantity = inventry_product[2]
                updated_quantity = current_quantity + quantity
                # Update the product quantity in the inventory
                update_quantity(updated_quantity, prod_code)

def create_table_recipt(recipt_code, products):
    """
    Creates a receipt-specific table and inserts product data.
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
        print(f"Error creating receipt table: {e}")

def get_recipt_product(recipt_code, prod_code):
    """
    Get a receipt-specific product data as a single-dimensional list.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the table exists
            if table_exists(recipt_code):
                # Retrieve product data from the existing receipt table
                cursor.execute(f"""
                    SELECT * FROM [{recipt_code}]
                    WHERE prod_code = %s
                """, (prod_code,))
                result = cursor.fetchone()  # Use fetchone() to get a single record
                if result:
                    return list(result)  # Convert tuple to list and return it
                else:
                    return None  # Return None if no result is found
    except Exception as e:
        print(f"Error fetching product data: {e}")
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
        print(f"Error fetching customer data: {e}")
        return None

def insert_customer_return(name, email, employ_name, recipt_code_buy, recipt_code_return, total_price, date_time, products):
    """
    Insert a new customer return record into the customers_return table or update it if it exists.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the record already exists in customers_return
            cursor.execute("SELECT COUNT(*) FROM customers_return WHERE recipt_code_return = %s", [recipt_code_return])
            exists = cursor.fetchone()[0]

            if exists:
                # Update the existing record in customers_return
                cursor.execute("""
                    UPDATE customers_return
                    SET name = %s, email = %s, Employ_name = %s, recipt_code_buy = %s, total_price = %s, date_time = %s
                    WHERE recipt_code_return = %s
                """, [name, email, employ_name, recipt_code_buy, total_price, date_time, recipt_code_return])
            else:
                # Insert a new record into customers_return
                cursor.execute("""
                    INSERT INTO customers_return (name, email, Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, email, employ_name, recipt_code_buy, recipt_code_return, total_price, date_time))

            # Create a new receipt table for the returned products
            create_table_recipt(recipt_code_return, products)

    except Exception as e:
        print(f"Error inserting customer return data: {e}")

def save_customer_recipt_return_to_db(Employ_name, recipt_code_buy,recipt_code_return, date_time, total_price, products):
    customer= get_customer_recipt(recipt_code_buy)
    print(f"Employ_name::{Employ_name}, recipt_code_buy::{recipt_code_buy},recipt_code_return::{recipt_code_return}, date_time::{date_time}, total_price::{total_price}, products::{products}")
    print(f"customer :: {customer}")
    insert_customer_return(customer[1], customer[2], Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time,products)