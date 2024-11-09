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

def plot_sales_data(dates, total_prices, frequency,start_date, end_date):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, total_prices, marker='o')
    plt.title(f'Sales Report ({frequency.capitalize()} :: {start_date} to {end_date})')
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

        chart_url = plot_sales_data(dates, total_prices, frequency,start_date, end_date)

    return chart_url

def sales_report_view(request):
    chart_url = None

    if request.method == "POST":
        frequency = request.POST.get('frequency')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        print(f"line 72 :: {frequency}  {start_date}  {end_date}")
        if frequency and start_date and end_date:
            # Convert date strings to actual date objects
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Check the frequency and adjust the end date accordingly
            if frequency == 'daily':
                # Keep the time as the last moment of the day (23:59:59)
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            elif frequency == 'monthly':
                # Set to the last day of the month and the last moment of that day
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                # Adjust the date to the last day of the month
                end_date = end_date + pd.offsets.MonthEnd(0)
            elif frequency == 'yearly':
                # Set to December 31st of the year and the last moment of that day
                end_date = end_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

            # Now end_date will reflect the end of the given day, month, or year
                print(f"line 92 :: {frequency}  {start_date}  {end_date}")
                # Generate report based on the form inputs
            chart_url = generate_report(frequency, start_date, end_date)

    return render(request, 'management/tests.html', {'chart_url': chart_url})
