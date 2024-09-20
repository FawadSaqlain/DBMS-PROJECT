from django.db import connection

from django.db import IntegrityError

def save_customer_to_db(customer_name, customer_email, Employ_name, recipt_no):
    """Inserts or updates customer data in the customers table."""
    try:
        with connection.cursor() as cursor:
            # Check if the record already exists
            cursor.execute("SELECT COUNT(*) FROM customers WHERE recipt_no = %s", [recipt_no])
            exists = cursor.fetchone()[0]

            if exists:
                # Optionally update the existing record
                cursor.execute("""
                    UPDATE customers
                    SET name = %s, email = %s, Employ_name = %s
                    WHERE recipt_no = %s
                """, [customer_name, customer_email, Employ_name, recipt_no])
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO customers (name, email, Employ_name, recipt_no) 
                    VALUES (%s, %s, %s, %s)
                """, [customer_name, customer_email, Employ_name, recipt_no])

    except IntegrityError as e:
        # Handle any other potential integrity errors
        print(f"Error inserting/updating record: {e}")
