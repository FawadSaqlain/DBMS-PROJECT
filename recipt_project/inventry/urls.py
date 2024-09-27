from django.urls import path
from . import views

app_name = 'inventry'
urlpatterns=[
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    # path('new/', views.new_receipt, name='new_receipt'),
    path('delete/<int:prod_index>/<str:prod_code>/', views.delet, name='dele'),
    path('edit_product/<int:prod_index>/<str:prod_code>/', views.edit_product, name='edit_product'),
    # path('edit_customer/<str:customer_name>/<str:customer_email>/', views.edit_customer, name='edit_customer'),
    path('inventry_sort/<int:asc_decs>/<str:sort_by>/', views.inventry_sort, name='inventry_sort'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),]