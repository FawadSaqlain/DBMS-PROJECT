from django.urls import path
from . import views

app_name = 'recipt'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('new/<int:return_product>', views.new_receipt, name='new_receipt'),
    path('delete/<int:id>/', views.dele, name='dele'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('edit_customer/<str:customer_name>/<str:customer_email>/', views.edit_customer, name='edit_customer'),
    path('sendmail/<int:new_recipt>', views.sendmail, name='sendmail'),
    path('sendmail_return/<int:new_recipt>', views.sendmail_return, name='sendmail_return'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('save-customer/<int:new_recipt>/', views.save_customer_recipt, name='save_customer'),
    path('return-product/', views.return_product, name='return_product'),
    path('save_customer_return/<int:new_recipt>/',views.save_customer_recipt_return,name='save_customer_return')
]