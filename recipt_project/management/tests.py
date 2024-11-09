import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Django

import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.db import connection
import pandas as pd
from matplotlib.ticker import FuncFormatter

def get_sales_data(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT total_price, date_time 
            FROM customers 
            WHERE date_time BETWEEN %s AND %s 
            ORDER BY date_time ASC
        """, [start_date, end_date])
        return cursor.fetchall()

def plot_sales_data(dates, total_prices, frequency):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, total_prices, marker='o')
    plt.title(f'Sales Report ({frequency.capitalize()})')
    plt.xlabel('Date')
    plt.ylabel('Total Price')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v/1_000_000:.2f}M' if v >= 1_000_000 else f'{v/1_000:.2f}K' if v >= 1000 else f'{v:.0f}'))

    # Save and encode the plot as a base64 string
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_url = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return chart_url

def generate_report(frequency, start_date, end_date):
    sales_data = get_sales_data(start_date, end_date)
    chart_url = None

    if sales_data:
        df = pd.DataFrame(sales_data, columns=['total_price', 'date_time'])
        df['date_time'] = pd.to_datetime(df['date_time'])
        df.set_index('date_time', inplace=True)

        # Resample data based on frequency (daily, monthly, yearly)
        if frequency == 'daily':
            resampled_data = df.resample('D').sum()
        elif frequency == 'monthly':
            resampled_data = df.resample('M').sum()
        elif frequency == 'yearly':
            resampled_data = df.resample('Y').sum()

        dates = resampled_data.index
        total_prices = resampled_data['total_price']

        chart_url = plot_sales_data(dates, total_prices, frequency)

    return chart_url

def sales_report_view(request):
    chart_url = None

    if request.method == "POST":
        frequency = request.POST.get('frequency')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if frequency and start_date and end_date:
            # Convert date strings to actual date objects
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Generate report based on the form inputs
            chart_url = generate_report(frequency, start_date, end_date)

    return render(request, 'management/tests.html', {'chart_url': chart_url})
