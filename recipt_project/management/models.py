from django.db import models
from django.db import connection, DatabaseError
from datetime import datetime
# Function to select all user data
def select_alluserdata():
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Employ"
            cursor.execute(query)
            result = cursor.fetchall()  # Fetch all rows of the result
            if result:
                print("Data selected successfully:")
                for row in result:
                    print(row)  # Print each row
            else:
                print("No data found in the Employ table.")
            return result
    except DatabaseError as e:
        print(f"Error selecting data: {e}")
# # Function to save user data
# def save_userdata(username, cnic, phone_number, address, user_type):
#     try:
#         with connection.cursor() as cursor:
#             query = """
#             INSERT INTO Employ (username, user_type, cnic, phone_number, updated_datetime, address)
#             VALUES (%s, %s, %s, %s, %s, %s)
#             """
#             values = (
#                 username,
#                 user_type,
#                 cnic,
#                 phone_number,
#                 datetime.now(),  # Store the current date and time
#                 address
#             )
#             cursor.execute(query, values)
#             connection.commit()  # Commit transaction
#             print("Data inserted successfully.")
#     except DatabaseError as e:
#         print(f"Error inserting data: {e}")
#         connection.rollback()  # Rollback in case of error

# Function to update user data
def update_userdata(username, cnic, phone_number, address, user_type):
    try:
        print(f"before updating {username}, {cnic}, {phone_number}, {address}, {user_type}")
        with connection.cursor() as cursor:
            query = """
            UPDATE Employ
            SET cnic = %s, phone_number = %s, address = %s, user_type = %s, updated_datetime = %s
            WHERE username = %s
            """
            values = (
                cnic,
                phone_number,
                address,
                user_type,
                datetime.now(),  # Update timestamp
                username
            )
            cursor.execute(query, values)
            connection.commit()  # Commit transaction
            print(f"Data updated successfully.{select_userdata(username)}")
    except DatabaseError as e:
        print(f"Error updating data: {e}")
        connection.rollback()  # Rollback in case of error

# Function to delete user data
def delete_userdata(username):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Employ WHERE username = %s"
            cursor.execute(query, [username])
            connection.commit()  # Commit transaction
            print("Data deleted successfully.")
    except DatabaseError as e:
        print(f"Error deleting data: {e}")
        connection.rollback()  # Rollback in case of error

# Function to select user data

def select_userdata(username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Employ WHERE username = %s"
            cursor.execute(query, [username])
            result = cursor.fetchone()  # Fetch the first row of the result
            if result:
                print("Data selected successfully:", result)
            else:
                print("No data found for the given username.")
            return result
    except DatabaseError as e:
        print(f"Error selecting data: {e}")
from django.db import connection, IntegrityError
from datetime import datetime

def save_userdata(username, cnic, phone_number, address, user_type):
    """Inserts or updates user data in the Employ table."""
    try:
        with connection.cursor() as cursor:
            # Check if the user already exists
            cursor.execute("SELECT COUNT(*) FROM dbo.Employ WHERE username = %s", [username])
            exists = cursor.fetchone()[0]

            if exists:
                # Update the existing user data
                user = select_userdata(username)
                print(f"line 64 models.py user :: {user}")
                if user[2] != cnic or user[3] != phone_number or user[4] != address or user[1] != user_type:
                    cursor.execute("""
                        UPDATE dbo.Employ
                        SET cnic = %s,
                            phone_number = %s,
                            address = %s,
                            user_type = %s,
                            updated_datetime = %s
                        WHERE username = %s
                    """, [cnic, phone_number, address, user_type, datetime.now(), username])
                    print(f"line 71: User {username} updated successfully.")
                else:
                    print(f"line 73: No updates needed for user {username}.")
            else:
                # Insert new user record
                cursor.execute("""
                    INSERT INTO dbo.Employ (username, user_type, cnic, phone_number, updated_datetime, address)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [username, user_type, cnic, phone_number, datetime.now(), address])
                print(f"line 79: User {username} added successfully.")
                
    except IntegrityError as e:
        print(f"line 81 Error inserting/updating user: {e}")
    except Exception as e:
        print(f"line 83 An unexpected error occurred: {e}")

def search_user(search_column, search_value):
    with connection.cursor() as cursor:
        # Ensure the search column is valid to prevent SQL injection
        valid_columns = ['prod_code', 'product_description', 'prod_quant', 'prod_sale_price', 'quantity_price_sale', 'updated_datetime', 'added_by_employ']
        
        # If search_column is 'all', construct a different query
        if search_column == 'all':
            sql = """
            SELECT * FROM Employ
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
