from django.db import connection
from django.db import IntegrityError
from . import models
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
                # Generate an ID by counting existing rows
                cursor.execute("SELECT COUNT(*) FROM customers_return")
                id = cursor.fetchone()[0] + 1  # Increment the count to use as the new ID

                # Insert a new record into customers_return
                cursor.execute("""
                    INSERT INTO customers_return (id, name, email, Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [id, name, email, employ_name, recipt_code_buy, recipt_code_return, total_price, date_time])

            # Create a new receipt table for the returned products
            create_table_recipt_return(recipt_code_return, products, recipt_code_buy)

    except Exception as e:
        print(f"Error inserting customer return data: {e}")

def save_customer_recipt_return_to_db(customer_name,customer_email,Employ_name, recipt_code_buy,recipt_code_return, date_time, total_price, products):
    
    print(f"line 430 Employ_name::{Employ_name}, recipt_code_buy::{recipt_code_buy},recipt_code_return::{recipt_code_return}, date_time::{date_time}, total_price::{total_price}, products::{products}")

    insert_customer_return(customer_name, customer_email, Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time,products)

    # customer_buy_data=get_customer_recipt(recipt_code_buy) 
    # total_price_buy=customer_buy_data[5]
    # customer_return_buy_data=get_customer_return_recipt(recipt_code_return)
    # total_return_buy=customer_return_buy_data[6]
    # updated_total_price=total_price_buy+total_return_buy
    # print(f"@ @ updated_total_price=total_price_buy + total_return_buy")
    # print(f"{updated_total_price} = {total_price_buy} + {total_return_buy}")
    # update_recipt_customer(recipt_code_buy, updated_total_price)
def create_table_recipt_return(recipt_code, products,recipt_code_buy):
    """
    Creates a receipt-specific table and inserts product data.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the table exists
            if models.table_exists(recipt_code):
                # Restore inventory quantities from the existing receipt table
                restore_inventory_from_receipt_return(recipt_code)
                restore_buy_recipt_from_receipt_return(recipt_code,recipt_code_buy)
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
        insert_quantity_inventry_subtract_recipt_quantity_return(recipt_code, products,recipt_code_buy)
    except Exception as e:
        print(f"line 316 Error creating receipt return table: {e}")
def get_customer_return_recipt(recipt_code_return):
    """
    Get a receipt-specific customer return data as a single-dimensional list.
    """
    try:
        with connection.cursor() as cursor:
            # Check if the table exists
            cursor.execute("""
                SELECT * FROM customers_return
                WHERE recipt_code_return = %s
            """, (recipt_code_return,))  # Include a comma to create a single-item tuple
            result = cursor.fetchone()  # Use fetchone() to get a single record
            if result:
                return list(result)  # Convert tuple to list and return it
            else:
                return None  # Return None if no result is found
    except Exception as e:
        print(f"line 378 Error fetching customer data: {e}")
        return None
def restore_inventory_from_receipt_return(recipt_code):
    """
    Restores the inventory quantities from an existing return receipt before dropping the table.
    """
    print("line 207 restore_inventory_from_receipt_return")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM [{recipt_code}]")
        products = cursor.fetchall()
        print(f"line 211 products ::{products}")
        for product in products:
            prod_code = product[1]
            quantity = product[3]
            quantity_price=product[5]
            print(f'line 216 product :: {product}')
            # Fetch current inventory quantity
            inventry_product = models.get_product(prod_code)
            if inventry_product:
                print(f'line 220 inventry_product :: {inventry_product}')
                current_quantity = inventry_product[2]
                updated_quantity = current_quantity - quantity
                updated_quantity_price=inventry_product[4]-quantity_price
                # Update the product quantity in the inventory
                models.update_quantity(updated_quantity,updated_quantity_price, prod_code)
def restore_buy_recipt_from_receipt_return(recipt_code,recipt_code_buy):
    """
    Restores the inventory quantities from an existing return receipt before dropping the table.
    """
    print("line 230 restore_inventory_from_receipt_return")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM [{recipt_code}]")
        products = cursor.fetchall()
        print(f"line 234 products ::{products}")
        for product in products:
            prod_code = product[1]
            quantity = product[3]
            quantity_price=product[5]
            print(f'line 239 product :: {product}')
            # Fetch current inventory quantity
            buy_recipt_product = models.get_recipt_product(recipt_code_buy, prod_code)
            if buy_recipt_product:
                print(f'line 243 buy_recipt_product :: {buy_recipt_product}')
                current_quantity = buy_recipt_product[3]
                updated_quantity = current_quantity + quantity
                updated_quantity_price=buy_recipt_product[5]+quantity_price
                # Update the product quantity in the inventory
                models.update_recipt_product_quantity(recipt_code_buy,prod_code, updated_quantity,updated_quantity_price)

        customer_buy_data=models.get_customer_recipt(recipt_code_buy) 
        total_price_buy=customer_buy_data[5]
        customer_return_buy_data=get_customer_return_recipt(recipt_code)
        total_return_buy=customer_return_buy_data[6]
        updated_total_price=total_price_buy+total_return_buy
        print(f"line 254 updated_total_price=total_price_buy + total_return_buy")
        print(f"line 255 {updated_total_price} = {total_price_buy} + {total_return_buy}")
        models.update_recipt_customer(recipt_code_buy, updated_total_price)
def insert_quantity_inventry_subtract_recipt_quantity_return(recipt_code, products, recipt_code_buy):
    """
    Inserts product quantity into the inventory table and updates product quantities.
    """
    try:
        for product in products:
            prod_code = product['prod_code'] if isinstance(product, dict) else product[0]
            quantity = product['quantity'] if isinstance(product, dict) else product[1]
            price = product['price'] if isinstance(product, dict) else product[2]
            price_quantity = product['price_quantity'] if isinstance(product, dict) else product[3]
            
            # Get inventory details for the product
            inventry_product = models.get_product(prod_code)
            print(f"line 139 inventry_product :: {inventry_product}")
            if not inventry_product:
                print(f"line 141 Product with code {prod_code} not found in inventory.")
                continue
            
            current_quantity = inventry_product[2]  # Assuming index 2 is prod_quant in the inventory
            updated_quantity = current_quantity + quantity
            update_quantity_price=price_quantity + inventry_product[4]
            print(f"line 147 updated quantity * price  {update_quantity_price}")
            print(f"line 148 Updating inventory for product {prod_code}: current {current_quantity}, updated {updated_quantity}")
            models.update_quantity(updated_quantity,update_quantity_price, prod_code)

            # Get receipt details for the product (the one they bought from originally)
            inventry_product_recipt = models.get_recipt_product(recipt_code_buy, prod_code)
            print(f"line 153 inventry_product_recipt :: {inventry_product_recipt}|| recipt_code_buy,:: {recipt_code_buy},|| prod_code :: {prod_code},")
            if not inventry_product_recipt:
                print(f"line 155 Product with code {prod_code} not found in receipt.")
                continue
            
            current_quantity_recipt = inventry_product_recipt[3]  # Assuming index 3 is prod_quant in the receipt
            print(f"line 159 current_quantity_recipt :: {current_quantity_recipt}")
            print(f"line 160 quantity ::{quantity}")
            updated_quantity_recipt = current_quantity_recipt - quantity
            print(f"line 162 updated_quantity_recipt ::{updated_quantity_recipt}")
            update_quantity_price_recipt=inventry_product_recipt[5] - price_quantity
            print(f"line 164 update_quantity_price_recipt {update_quantity_price_recipt} # inventry_product_recipt[5] {inventry_product_recipt[5]} # price_quantity {price_quantity}")
            models.update_recipt_product_quantity(recipt_code_buy, prod_code,updated_quantity_recipt,update_quantity_price_recipt)

            # Insert into the return receipt table
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO [{recipt_code}] (prod_code, prod_discreption, quantity, price, price_quantity) 
                    VALUES (%s, %s, %s, %s, %s)
                """, [prod_code, inventry_product[1], quantity, price, price_quantity])

        customer_buy_data=models.get_customer_recipt(recipt_code_buy) 
        total_price_buy=customer_buy_data[5]
        customer_return_buy_data=get_customer_return_recipt(recipt_code)
        total_return_buy=customer_return_buy_data[6]
        updated_total_price=total_price_buy-total_return_buy
        print(f"line 179 updated_total_price=total_price_buy + total_return_buy")
        print(f"{updated_total_price} = {total_price_buy} - {total_return_buy}")
        models.update_recipt_customer(recipt_code_buy, updated_total_price)

    except Exception as e:
        print(f"line 184 Error inserting data into receipt table: {e}")
