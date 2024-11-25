from django.db import models
from django.db import connection, DatabaseError
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q

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
    result = []
    
    # Search in the custom Employ table for usernames
    with connection.cursor() as cursor:
        valid_columns = ['username', 'user_type', 'cnic', 'phone_number', 'updated_datetime', 'address']

        if search_column == 'all':
            sql = """
            SELECT username FROM Employ
            WHERE LOWER(username) LIKE LOWER(%s)
            OR LOWER(user_type) LIKE LOWER(%s)
            OR LOWER(cnic) LIKE LOWER(%s)
            OR LOWER(phone_number) LIKE LOWER(%s)
            OR LOWER(CAST(updated_datetime AS VARCHAR(50))) LIKE LOWER(%s)
            OR LOWER(address) LIKE LOWER(%s)
            """
            like_value = f'%{search_value}%'
            cursor.execute(sql, [like_value] * 6)
        else:
            if search_column not in valid_columns:
                raise ValueError("Invalid search column provided.")
            
            sql = f"SELECT username FROM Employ WHERE LOWER({search_column}) LIKE LOWER(%s)"
            cursor.execute(sql, [f'%{search_value}%'])
        
        # Fetch and add unique usernames from the Employ table
        employ_usernames = [row[0] for row in cursor.fetchall()]
        result.extend([username for username in employ_usernames if username not in result])

    # Search in the Django User model for usernames
    if search_column in ['username', 'first_name', 'last_name', 'email', 'all']:
        if search_column == 'all':
            user_results = User.objects.filter(
                Q(username__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value)
            ).values_list('username', flat=True)
        else:
            filter_kwargs = {f"{search_column}__icontains": search_value}
            user_results = User.objects.filter(**filter_kwargs).values_list('username', flat=True)
        
        # Fetch and add unique usernames from the User model
        user_usernames = list(user_results)
        result.extend([username for username in user_usernames if username not in result])

    # Return the combined unique usernames list
    return result

def view_sorted_user(request, asc_decs, sort_by):
    """Returns a list of sorted Employs in the user."""
    try:
        with connection.cursor() as cursor:
            order = "ASC" if asc_decs == 0 else "DESC"
            query = f"SELECT username FROM Employ ORDER BY {sort_by} {order}"
            cursor.execute(query)
            Employs = cursor.fetchall()
            
            return [list(Employ) for Employ in Employs]
    except Exception as e:
        print(f"line 200 Error fetching Employ data: {e}")
        return []

def get_customer_data():
    """Returns a tuple containing lists of customers and customers_return data."""
    try:
        with connection.cursor() as cursor:
            # Fetch customers
            query = "SELECT * FROM customers"
            cursor.execute(query)
            customers = cursor.fetchall()

        with connection.cursor() as cursor:
            # Fetch customers_return
            query_return = "SELECT * FROM customers_return"
            cursor.execute(query_return)
            customers_return = cursor.fetchall()

        return customers, customers_return
    except Exception as e:
        print(f"Error fetching customer data: {e}")
        return [], []  # Return empty lists if an error occurs


def view_customer_sort(asc_decs,sort_by):
    """Returns a list of sorted customer in the customer buy."""
    try:
        with connection.cursor() as cursor:
            order = "ASC" if asc_decs == 0 else "DESC"
            query = f"SELECT * FROM customers ORDER BY {sort_by} {order}"
            cursor.execute(query)
            customers = cursor.fetchall()
            return [list(customers) for customers in customers]
    except Exception as e:
        print(f"line 143 Error fetching customers data: {e}")
        return []


def get_customer_buy_buy_recipt_code_search(search_column, search_value):
    """Search for customer buy data based on a column and value, returning a list of receipt codes as strings."""
    if search_column == 'recipt_code_buy':
        search_column = 'recipt_code'
    if search_column == 'recipt_code_return':
        return []

    customer_buy = []

    with connection.cursor() as cursor:
        valid_columns = ['name', 'email', 'Employ_name', 'recipt_code', 'total_price', 'date_time']
        if search_column == 'all':
            sql = """
            SELECT recipt_code FROM customers
            WHERE LOWER(name) LIKE LOWER(%s)
            OR LOWER(email) LIKE LOWER(%s)
            OR LOWER(Employ_name) LIKE LOWER(%s)
            OR LOWER(recipt_code) LIKE LOWER(%s)
            OR CAST(total_price AS VARCHAR) LIKE LOWER(%s)
            OR FORMAT(date_time, 'yyyy-MM-dd HH:mm:ss') LIKE LOWER(%s)
            """
            like_value = f'%{search_value}%'
            cursor.execute(sql, [like_value] * 6)
        else:
            if search_column not in valid_columns:
                raise ValueError(f"Invalid search column: {search_column}")

            sql = f"SELECT recipt_code FROM customers WHERE LOWER({search_column}) LIKE LOWER(%s)"
            cursor.execute(sql, [f'%{search_value}%'])

        # Fetch results and extract the first column as strings
        customer_buy = [row[0] for row in cursor.fetchall()]

    return customer_buy


def get_customer_return_buy_recipt_code_search(search_column, search_value):
    """Search for customer return data based on a column and value, returning a list of receipt codes as strings."""
    customer_return = []

    with connection.cursor() as cursor:
        valid_columns = ['name', 'email', 'Employ_name', 'recipt_code_buy', 'recipt_code_return', 'total_price', 'date_time']
        if search_column == 'all':
            sql = """
            SELECT recipt_code_buy FROM customers_return
            WHERE LOWER(name) LIKE LOWER(%s)
            OR LOWER(email) LIKE LOWER(%s)
            OR LOWER(Employ_name) LIKE LOWER(%s)
            OR LOWER(recipt_code_buy) LIKE LOWER(%s)
            OR LOWER(recipt_code_return) LIKE LOWER(%s)
            OR CAST(total_price AS VARCHAR) LIKE LOWER(%s)
            OR FORMAT(date_time, 'yyyy-MM-dd HH:mm:ss') LIKE LOWER(%s)
            """
            like_value = f'%{search_value}%'
            cursor.execute(sql, [like_value] * 7)
        else:
            if search_column not in valid_columns:
                raise ValueError(f"Invalid search column: {search_column}")

            sql = f"SELECT recipt_code_buy FROM customers_return WHERE LOWER({search_column}) LIKE LOWER(%s)"
            cursor.execute(sql, [f'%{search_value}%'])

        # Fetch results and extract the first column as strings
        customer_return = [row[0] for row in cursor.fetchall()]

    return customer_return

def get_customer_buy_data(recipt_buy_code):
    """Returns a tuple containing data of customers from the 'customers' table."""
    try:
        with connection.cursor() as cursor:
            # Fetch customers
            query = "SELECT * FROM customers WHERE recipt_code = %s"
            cursor.execute(query, [recipt_buy_code])  # Pass the parameter correctly
            customers = cursor.fetchall()
        return customers
    except Exception as e:
        print(f"Error fetching customer data: {e}")
        return []  # Return an empty list if an error occurs


def get_customer_return_data(recipt_buy_code):
    """Returns a tuple containing data of customers from the 'customers_return' table."""
    try:
        with connection.cursor() as cursor:
            # Fetch customers_return
            query_return = "SELECT * FROM customers_return WHERE recipt_code_buy = %s"
            cursor.execute(query_return, [recipt_buy_code])  # Pass the parameter correctly
            customers_return = cursor.fetchall()
        return customers_return
    except Exception as e:
        print(f"Error fetching customer return data: {e}")
        return []  # Return an empty list if an error occurs


def get_table_recipt(table_name):
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


def get_customer_by_recipt_code(code,table_name):
    try:
        with connection.cursor() as cursor:
            if table_name=='customers_return':
                query = f"SELECT * FROM {table_name} WHERE recipt_code_return = %s"
            else:
                query = f"SELECT * FROM {table_name} WHERE recipt_code = %s"
            cursor.execute(query, [code])  # Pass the parameter correctly
            customer = cursor.fetchone()
            if customer:
                return list(customer)
            else:
                return None
    except Exception as e:
        print(f"Error fetching customer data: {e}")