from django.db import connection
from django.db import IntegrityError
from . import models
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
                cursor.execute("SELECT COUNT(*) FROM customers_return WHERE recipt_code_buy = %s", [recipt_code_buy])
                id = cursor.fetchone()[0] + 1  # Increment the count to use as the new ID

                # Insert a new record into customers_return
                cursor.execute("""
                    INSERT INTO customers_return (id, name, email, Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [id, name, email, employ_name, recipt_code_buy, recipt_code_return, total_price, date_time])

            # Create a new receipt table for the returned products
            create_table_recipt_return(recipt_code_return, products, recipt_code_buy)

    except Exception as e:
        print(f"line 36 Error inserting customer return data: {e}")

def save_customer_recipt_return_to_db(customer_name,customer_email,Employ_name, recipt_code_buy,recipt_code_return, date_time, total_price, products):

    insert_customer_return(customer_name, customer_email, Employ_name, recipt_code_buy, recipt_code_return, total_price, date_time,products)

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
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM [{recipt_code}]")
        products = cursor.fetchall()
        for product in products:
            prod_code = product[1]
            quantity = product[3]
            quantity_price=product[5]
            # Fetch current inventory quantity
            inventry_product = models.get_product(prod_code)
            if inventry_product:
                current_quantity = inventry_product[2]
                updated_quantity = current_quantity - quantity
                updated_quantity_price=inventry_product[4]-quantity_price
                # Update the product quantity in the inventory
                models.update_quantity(updated_quantity,updated_quantity_price, prod_code)
def restore_buy_recipt_from_receipt_return(recipt_code,recipt_code_buy):
    """
    Restores the inventory quantities from an existing return receipt before dropping the table.
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM [{recipt_code}]")
        products = cursor.fetchall()
        for product in products:
            prod_code = product[1]
            quantity = product[3]
            quantity_price=product[5]
            # Fetch current inventory quantity
            buy_recipt_product = models.get_recipt_product(recipt_code_buy, prod_code)
            if buy_recipt_product:
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
            if not inventry_product:
                continue
            
            current_quantity = inventry_product[2]  # Assuming index 2 is prod_quant in the inventory
            updated_quantity = current_quantity + quantity
            # update_quantity_price=price_quantity + inventry_product[4]
            update_quantity_price=(quantity*inventry_product[3]) + inventry_product[4] # Assuming index 3 is prod_price in the inventory
            models.update_quantity(updated_quantity,update_quantity_price, prod_code)

            # Get receipt details for the product (the one they bought from originally)
            product_recipt_buy = models.get_recipt_product(recipt_code_buy, prod_code)
            if not product_recipt_buy:
                continue
            
            current_quantity_recipt = product_recipt_buy[3]  # Assuming index 3 is prod_quant in the receipt
            updated_quantity_recipt = current_quantity_recipt - quantity
            update_quantity_price_recipt=product_recipt_buy[5] - price_quantity
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
        print(f"{updated_total_price} = {total_price_buy} - {total_return_buy}")
        models.update_recipt_customer(recipt_code_buy, updated_total_price)

    except Exception as e:
        print(f"line 184 Error inserting data into receipt table: {e}")
