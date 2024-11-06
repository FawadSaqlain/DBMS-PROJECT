from django.shortcuts import render
from django.contrib.auth.models import User
from . import models

def sorted_user_list(request, order, sort_by):
    # Define valid fields for sorting in Django
    valid_fields_in_django = ['username', 'email', 'first_name', 'last_name']
    
    # Check if sorting is on a valid field
    if sort_by not in valid_fields_in_django:
        # Use custom sorting if the field is not in Django's User model
        user_names_list = models.view_sorted_user(request, order, sort_by)
        # Flatten the list in case of nested structure
        user_names = [username for sublist in user_names_list for username in sublist]
    else:
        # Define sort order (ascending or descending)
        sort_order = f'-{sort_by}' if order == 1 else sort_by
        user_names = User.objects.all().order_by(sort_order).values_list('username', flat=True)

    completedata_database = []
    completedata_django = []

    # Process each username to gather additional information
    for username in user_names:
        username = username.strip("[]'")  # Ensure clean username strings
        print(f"Processing username: {username}")  # Debugging output
        
        try:
            # Fetch database information
            completedata_database.append(models.select_userdata(username))
            
            # Fetch Django's User model information
            user = User.objects.get(username=username)
            completedata_django.append(user)
            print(f"User.objects.get(username={username}) :: {user}")
        
        except User.DoesNotExist:
            print(f"User with username '{username}' does not exist.")
        except Exception as e:
            print(f"Error selecting data: {e}")

    # print(f"user_database :: {completedata_database}")
    # print(f"user_django :: {completedata_django}")

    # Render response with both sets of data
    return render(request, 'management/index.html', {
        "databasedata": completedata_database,
        'users': completedata_django,
        'length_users': range(len(models.select_alluserdata())),
        'sorted_as': f"{order}{sort_by.lstrip('-')}"
    })
