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
    customer_buy=models.view_customer_sort(asc_decs,sort_by)
    # rendering(request,customer_buy)
    return HttpResponseRedirect(reverse(rendering(request,customer_buy)))


# def customer_search(request):
#     if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
#         return HttpResponseRedirect(reverse("management:login"))
#     search_column = request.GET.get('section', 'username')  # Default search column
#     search_value = request.GET.get('q', '')  # Retrieved search value
    
#     # Convert search_value to string (if not already a string)
#     search_value = str(search_value)
    
#     print(f"line 399 search value :: {search_value} , search column :: {search_column}")

#     results = []  # Initialize results list

#     # Check if search_value is not empty
#     if search_value:
#         results = models.get_customer_search(search_column, search_value)
#     rendering(results)
#     # Render

def customerdata(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    customer_buy , customer_return = models.get_customer_data()
    # rendering(request, customer_buy, customer_return)
    return HttpResponseRedirect(reverse(rendering(request,customer_buy, customer_return)))

def sales_report_view(request):
    if not request.user.is_authenticated or models.select_userdata(request.user.username)[1] != "administration manager":
        return HttpResponseRedirect(reverse("management:login"))
    chart_url = None

    if request.method == "POST":
        try:
            frequency = request.POST.get('frequency')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            print(f"line 72 :: {frequency}  {start_date}  {end_date}")
            
            if frequency and start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)

                if frequency == 'daily':
                    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                elif frequency == 'monthly':
                    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                    end_date = end_date + pd.offsets.MonthEnd(0)
                elif frequency == 'yearly':
                    end_date = end_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

                print(f"line 92 :: {frequency}  {start_date}  {end_date}")
                chart_url = generate_report(frequency, start_date, end_date)
                # rendering(request,chart_url)
                return HttpResponseRedirect(reverse(rendering(request,chart_url)))
        except ValueError as ve:
            # print(f"Date parsing error: {ve}")
            return render(request, 'management/error.html', {
                        "error": f"Date parsing error: {ve}"
                        })
        except Exception as e:
            print(f"Unexpected error: {e}")
            return render(request, 'management/error.html', {
                        "error": f"Unexpected error: {e}"
                        })

def rendering( request, customer_buy=None , customer_return=None , chart_url=None):
    return render(request, 'management/sales_report.html',
                {'chart_url': chart_url,'customer_buy': customer_buy,'customer_return': customer_return})

# def sales_report(request):
#     chart_url=sales_report_view(request)
#     customer_buy , customer_return = customerdata(request)
#     return render(request, 'management/sales_report.html',
#                 {'chart_url': chart_url,'customer_buy': customer_buy,'customer_return': customer_return})
