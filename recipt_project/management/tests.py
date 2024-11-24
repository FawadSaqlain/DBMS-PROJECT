from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django import forms
from . import models
from django.contrib.auth.hashers import check_password
import pandas as pd
from .sales_report import generate_report
def customer_sort(request,asc_decs,sort_by):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    customer_buy, customer_return = models.get_customer_data()
    customer_buy=models.view_customer_sort(asc_decs,sort_by)
    return render(request,"management/customer_table.html",{"customer_buy":customer_buy,'sorted_as':f"{asc_decs}{sort_by}","customer_return":customer_return})


def customer_search(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    search_column = request.GET.get('section')  # Default search column
    search_value = request.GET.get('q', '')  # Retrieved search value
    
    # Convert search_value to string (if not already a string)
    search_value = str(search_value)
    
    print(f"line 399 search value :: {search_value} , search column :: {search_column}")

    customer_buy = []  # Initialize customer_buy list
    customer_return = []  # Initialize customer_return list

    # Check if search_value is not empty
    if search_value:
        customer_buy_code = models.get_customer_buy_buy_recipt_code_search(search_column, search_value)
        customer_return_code = models.get_customer_return_buy_recipt_code_search(search_column, search_value)
        customer_buy , customer_return=models.get_customer_data_by_recipt(customer_buy_code,customer_return_code)
        

    return render(request, 'management/customer_table.html',
                {'customer_buy': customer_buy,'customer_return': customer_return})


def customerdata(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    customer_buy , customer_return = models.get_customer_data()
    return render(request, 'management/customer_table.html',
                {'customer_buy': customer_buy,'customer_return': customer_return})
