from django.shortcuts import render
from django.contrib.auth.models import User
from . import models

def sorted_user_list(request, sort_by, order):
    valid_fields_in_django = ['username', 'email', 'first_name', 'last_name']
    
    if sort_by not in valid_fields_in_django:
        user_names_list = models.view_sorted_user(request, order, sort_by)
        # Flatten the list if necessary (if user_names_list is a list of lists)
        user_names = [username for sublist in user_names_list for username in sublist]
    else:
        sort_order = f'-{sort_by}' if order == 'desc' else sort_by
        user_names = User.objects.all().order_by(sort_order).values_list('username', flat=True)

    completedata_database = []
    completedata_django = []

    for username in user_names:
        username = username.strip("[]'")  # Ensure we're dealing with a string, remove extra characters if needed
        print(f"Processing username: {username}")  # Debugging line
        try:
            completedata_database.append(models.select_userdata(username))
            user=User.objects.get(username=username)
            user_info = [user.username,user.first_name, user.last_name, user.email,]
            completedata_django.append(user_info)
            print(f"User.objects.get(username=username) :: {User.objects.get(username=username)}")
        except User.DoesNotExist:
            print(f"User with username '{username}' does not exist.")  # Debugging line
        except Exception as e:
            print(f"Error selecting data: {e}")  # Print any other error messages
    print(f"user_database :: {completedata_database}")
    print(f"user_django :: {completedata_django}")
    return render(request, 'management/tests.html', {
        'database': completedata_database,
        'django': completedata_django,
        'sorted_as': sort_by.lstrip('-'),  # UI reference
        'current_order': order  # UI toggle reference
    })
