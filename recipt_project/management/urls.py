from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_user/', views.add_user, name='add_user'),
    path('remove_user/<int:user_index>/<str:username>/', views.remove_user, name='remove_user'),  # Remove user URL
    path('edit_user/<int:user_index>/<str:username>/', views.edit_user, name='edit_user'),  # Edit user URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search_view/', views.search_view, name='search_view'),
    ]