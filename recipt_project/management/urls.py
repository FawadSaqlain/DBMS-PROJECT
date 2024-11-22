from django.urls import path
from . import views
from.import tests
app_name = 'management'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_user/', views.add_user, name='add_user'),
    path('remove_user/<int:user_index>/<str:username>/', views.remove_user, name='remove_user'),  # Remove user URL
    path('edit_user/<int:user_index>/<str:username>/', views.edit_user, name='edit_user'),  # Edit user URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search_user/', views.search_user, name='search_user'),
    path('profile/', views.profile, name='profile'),
    path('user_sort/<int:asc_decs>/<str:sort_by>/', views.user_sort, name='user_sort'),
    path('sales_report/',tests.sales_report_view,name='sales_report'),
    path('customer_sort/<int:asc_decs>/<str:sort_by>/',tests.customer_sort,name='customer_sort')
    ]