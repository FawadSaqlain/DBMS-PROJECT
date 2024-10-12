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
            print(f"## line 42 models.py product :: {product}")
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
            print(f"line 69 update_quantity {quantity},{update_quantity_price},{prod_code}")
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
            print(f"line 85 inventry_product :: {inventry_product}")
            if not inventry_product:
                print(f"line 86 Product with code {prod_code} not found.")
                continue  # Skip if product not found
            
            # inventry_product = inventry_product[0]
            current_quantity = inventry_product[2]  # Assuming this is prod_quant
            print(f"line 91 current quantity  {current_quantity}")
            updated_quantity = current_quantity - quantity
            print(f"line 93 updated quantity  {updated_quantity}")

            update_quantity_price = inventry_product[4] - price_quantity
            print(f"line 96 updated quantity price ::  {update_quantity_price}")

            # Update the product quantity in the inventory
            print(f"line 99 inventry before updated {updated_quantity} , {prod_code}")
            update_quantity(updated_quantity,update_quantity_price, prod_code)
            print(f"line 101 inventry after updated {updated_quantity} , {prod_code}")
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO [{recipt_code}] (prod_code, prod_discreption, quantity, price, price_quantity) 
                    VALUES (%s, %s, %s, %s, %s)
                """, [prod_code, inventry_product[1], quantity, price, price_quantity])
    except Exception as e:
        print(f"line 108 Error inserting data into receipt table: {e}")
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

            print(f"line 122 Updated total_price to {total_price} for recipt_code {recipt_code_buy}")

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
            print(f"line 193 product :: {product}")
            prod_code = product[1]
            quantity = product[3]
            quanitiy_price=product[5]
            # Fetch current inventory quantity
            inventry_product = get_product(prod_code)
            print(f"line 200 inventry_product :: {inventry_product}")
            if inventry_product:
                current_quantity = inventry_product[2]
                updated_quantity = current_quantity + quantity
                updated_quantity_price=inventry_product[4]+quanitiy_price
                # Update the product quantity in the inventory
                update_quantity(updated_quantity,updated_quantity_price, prod_code)
                print(f"line 207 get updated inventry {get_product(prod_code)}")
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
                print(f"line 333 Updated quantity for product {prod_code} to {prod_quant} in receipt {recipt_code}")
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

# '''
# def insert_quantity_inventry_subtract_recipt_quantity_return(recipt_code, products, recipt_code_buy):
#     """
#     Inserts product quantity into the inventory table and updates product quantities.
#     """
#     try:
#         for product in products:
#             prod_code = product['prod_code'] if isinstance(product, dict) else product[0]
#             quantity = product['quantity'] if isinstance(product, dict) else product[1]
#             price = product['price'] if isinstance(product, dict) else product[2]
#             price_quantity = product['price_quantity'] if isinstance(product, dict) else product[3]
            
#             # Get inventory details for the product
#             inventry_product = get_product(prod_code)
#             print(f"line 139 inventry_product :: {inventry_product}")
#             if not inventry_product:
#                 print(f"line 141 Product with code {prod_code} not found in inventory.")
#                 continue
            
#             current_quantity = inventry_product[2]  # Assuming index 2 is prod_quant in the inventory
#             updated_quantity = current_quantity + quantity
#             update_quantity_price=price_quantity + inventry_product[4]
#             print(f"line 147 updated quantity * price  {update_quantity_price}")
#             print(f"line 148 Updating inventory for product {prod_code}: current {current_quantity}, updated {updated_quantity}")
#             update_quantity(updated_quantity,update_quantity_price, prod_code)

#             # Get receipt details for the product (the one they bought from originally)
#             inventry_product_recipt = get_recipt_product(recipt_code_buy, prod_code)
#             print(f"line 153 inventry_product_recipt :: {inventry_product_recipt}|| recipt_code_buy,:: {recipt_code_buy},|| prod_code :: {prod_code},")
#             if not inventry_product_recipt:
#                 print(f"line 155 Product with code {prod_code} not found in receipt.")
#                 continue
            
#             current_quantity_recipt = inventry_product_recipt[3]  # Assuming index 3 is prod_quant in the receipt
#             print(f"line 159 current_quantity_recipt :: {current_quantity_recipt}")
#             print(f"line 160 quantity ::{quantity}")
#             updated_quantity_recipt = current_quantity_recipt - quantity
#             print(f"line 162 updated_quantity_recipt ::{updated_quantity_recipt}")
#             update_quantity_price_recipt=inventry_product_recipt[5] - price_quantity
#             print(f"line 164 update_quantity_price_recipt {update_quantity_price_recipt} # inventry_product_recipt[5] {inventry_product_recipt[5]} # price_quantity {price_quantity}")
#             update_recipt_product_quantity(recipt_code_buy, prod_code,updated_quantity_recipt,update_quantity_price_recipt)

#             # Insert into the return receipt table
#             with connection.cursor() as cursor:
#                 cursor.execute(f"""
#                     INSERT INTO [{recipt_code}] (prod_code, prod_discreption, quantity, price, price_quantity) 
#                     VALUES (%s, %s, %s, %s, %s)
#                 """, [prod_code, inventry_product[1], quantity, price, price_quantity])

#         customer_buy_data=get_customer_recipt(recipt_code_buy) 
#         total_price_buy=customer_buy_data[5]
#         customer_return_buy_data=get_customer_return_recipt(recipt_code)
#         total_return_buy=customer_return_buy_data[6]
#         updated_total_price=total_price_buy-total_return_buy
#         print(f"line 179 updated_total_price=total_price_buy + total_return_buy")
#         print(f"{updated_total_price} = {total_price_buy} - {total_return_buy}")
#         update_recipt_customer(recipt_code_buy, updated_total_price)

#     except Exception as e:
#         print(f"line 184 Error inserting data into receipt table: {e}")
# '''
# '''
# def create_table_recipt_return(recipt_code, products,recipt_code_buy):
#     """
#     Creates a receipt-specific table and inserts product data.
#     """
#     try:
#         with connection.cursor() as cursor:
#             # Check if the table exists
#             if table_exists(recipt_code):
#                 # Restore inventory quantities from the existing receipt table
#                 restore_inventory_from_receipt_return(recipt_code)
#                 restore_buy_recipt_from_receipt_return(recipt_code,recipt_code_buy)
#                 # Drop the existing receipt table
#                 cursor.execute(f"DROP TABLE [{recipt_code}]")
            
#             # Create the new table
#             cursor.execute(f"""
#                 CREATE TABLE [{recipt_code}] (
#                     id INT PRIMARY KEY IDENTITY,
#                     prod_code NVARCHAR(100),
#                     prod_discreption NVARCHAR(1000),
#                     quantity INT,
#                     price FLOAT,
#                     price_quantity FLOAT
#                 )
#             """)
        
#         # Insert data into the new table
#         insert_quantity_inventry_subtract_recipt_quantity_return(recipt_code, products,recipt_code_buy)
#     except Exception as e:
#         print(f"line 316 Error creating receipt return table: {e}")
# '''
# '''
# def restore_buy_recipt_from_receipt_return(recipt_code,recipt_code_buy):
#     """
#     Restores the inventory quantities from an existing return receipt before dropping the table.
#     """
#     print("line 230 restore_inventory_from_receipt_return")
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT * FROM [{recipt_code}]")
#         products = cursor.fetchall()
#         print(f"line 234 products ::{products}")
#         for product in products:
#             prod_code = product[1]
#             quantity = product[3]
#             quantity_price=product[5]
#             print(f'line 239 product :: {product}')
#             # Fetch current inventory quantity
#             buy_recipt_product = get_recipt_product(recipt_code_buy, prod_code)
#             if buy_recipt_product:
#                 print(f'line 243 buy_recipt_product :: {buy_recipt_product}')
#                 current_quantity = buy_recipt_product[3]
#                 updated_quantity = current_quantity + quantity
#                 updated_quantity_price=buy_recipt_product[5]+quantity_price
#                 # Update the product quantity in the inventory
#                 update_recipt_product_quantity(recipt_code_buy,prod_code, updated_quantity,updated_quantity_price)

#         customer_buy_data=get_customer_recipt(recipt_code_buy) 
#         total_price_buy=customer_buy_data[5]
#         customer_return_buy_data=get_customer_return_recipt(recipt_code)
#         total_return_buy=customer_return_buy_data[6]
#         updated_total_price=total_price_buy+total_return_buy
#         print(f"line 254 updated_total_price=total_price_buy + total_return_buy")
#         print(f"line 255 {updated_total_price} = {total_price_buy} + {total_return_buy}")
#         update_recipt_customer(recipt_code_buy, updated_total_price)
# '''
# '''
# def insert_customer_return(name, email, employ_name, recipt_code_buy, recipt_code_return, total_price, date_time, products):
#     """
#     Insert a new customer return record into the customers_return table or update it if it exists.
#     """
#     try:
#         with connection.cursor() as cursor:
#             # Check if the record already exists in customers_return
#             cursor.execute("SELECT COUNT(*) FROM customers_return WHERE recipt_code_return = %s", [recipt_code_return])
#             exists = cursor.fetchone()[0]

#             if exists:
#                 # Update the existing record in customers_return
#                 cursor.execute("""
#                     UPDATE customers_return
#                     SET name = %s, email = %s, Employ_name = %s, recipt_code_buy = %s, total_price = %s, date_time = %s
#                     WHERE recipt_code_return = %s
#                 """, [name, email, employ_name, recipt_code_buy, total_price, date_time, recipt_code_return])
#             else:
#                 # Insert a new record into customers_return
#                 cursor.execute("""
#                     INSERT INTO customers_return (name, email, Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 """, (name, email, employ_name, recipt_code_buy, recipt_code_return, total_price, date_time))

#             # Create a new receipt table for the returned products
#             create_table_recipt_return(recipt_code_return, products,recipt_code_buy)

#     except Exception as e:
#         print(f"line 427 Error inserting customer return data: {e}")
# '''
# '''
# def save_customer_recipt_return_to_db(Employ_name, recipt_code_buy,recipt_code_return, date_time, total_price, products):
#     customer= get_customer_recipt(recipt_code_buy)
#     print(f"line 430 Employ_name::{Employ_name}, recipt_code_buy::{recipt_code_buy},recipt_code_return::{recipt_code_return}, date_time::{date_time}, total_price::{total_price}, products::{products}")
#     print(f"line 431 customer :: {customer}")
#     insert_customer_return(customer[1], customer[2], Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time,products)

#     # customer_buy_data=get_customer_recipt(recipt_code_buy) 
#     # total_price_buy=customer_buy_data[5]
#     # customer_return_buy_data=get_customer_return_recipt(recipt_code_return)
#     # total_return_buy=customer_return_buy_data[6]
#     # updated_total_price=total_price_buy+total_return_buy
#     # print(f"@ @ updated_total_price=total_price_buy + total_return_buy")
#     # print(f"{updated_total_price} = {total_price_buy} + {total_return_buy}")
#     # update_recipt_customer(recipt_code_buy, updated_total_price)
# '''
# '''
# def restore_inventory_from_receipt_return(recipt_code):
#     """
#     Restores the inventory quantities from an existing return receipt before dropping the table.
#     """
#     print("line 207 restore_inventory_from_receipt_return")
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT * FROM [{recipt_code}]")
#         products = cursor.fetchall()
#         print(f"line 211 products ::{products}")
#         for product in products:
#             prod_code = product[1]
#             quantity = product[3]
#             quantity_price=product[5]
#             print(f'line 216 product :: {product}')
#             # Fetch current inventory quantity
#             inventry_product = get_product(prod_code)
#             if inventry_product:
#                 print(f'line 220 inventry_product :: {inventry_product}')
#                 current_quantity = inventry_product[2]
#                 updated_quantity = current_quantity - quantity
#                 updated_quantity_price=inventry_product[4]-quantity_price
#                 # Update the product quantity in the inventory
#                 update_quantity(updated_quantity,updated_quantity_price, prod_code)
# '''
# '''
# def get_customer_return_recipt(recipt_code_return):
#     """
#     Get a receipt-specific customer return data as a single-dimensional list.
#     """
#     try:
#         with connection.cursor() as cursor:
#             # Check if the table exists
#             cursor.execute("""
#                 SELECT * FROM customers_return
#                 WHERE recipt_code_return = %s
#             """, (recipt_code_return,))  # Include a comma to create a single-item tuple
#             result = cursor.fetchone()  # Use fetchone() to get a single record
#             if result:
#                 return list(result)  # Convert tuple to list and return it
#             else:
#                 return None  # Return None if no result is found
#     except Exception as e:
#         print(f"line 378 Error fetching customer data: {e}")
#         return None
# '''

