import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Django

import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.db import connection, DatabaseError
from matplotlib.ticker import FuncFormatter
from datetime import datetime
import pandas as pd

def get_sales_data(start_date, end_date):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT total_price, date_time 
                FROM customers 
                WHERE date_time BETWEEN %s AND %s 
                ORDER BY date_time ASC
            """, [start_date, end_date])
            return cursor.fetchall()
    except DatabaseError as e:
        print(f"Database error: {e}")
        return []

def plot_sales_data(dates, total_prices, frequency, start_date, end_date):
    try:
        plt.figure(figsize=(10, 5))
        print(dates)
        plt.plot(dates, total_prices, marker='o', color=(165/255, 42/255, 42/255))
        
        plt.title(f'Sales Report ({frequency.capitalize()} :: {start_date} to {end_date})')
        plt.xlabel('Date')
        plt.ylabel('Total Price')
        plt.xticks(rotation=45)
        plt.gca().yaxis.set_major_formatter(
            FuncFormatter(lambda v, _: f'{v/1_000_000:.2f}M' if v >= 1_000_000 else f'{v/1_000:.2f}K' if v >= 1000 else f'{v:.0f}')
        )

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_url = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()
        return chart_url
    except Exception as e:
        print(f"Error in plotting data: {e}")
        return None

def generate_report(frequency, start_date, end_date):
    try:
        sales_data = get_sales_data(start_date, end_date)
        if not sales_data:
            print("No data found for the provided date range.")
            return None

        df = pd.DataFrame(sales_data, columns=['total_price', 'date_time'])
        df['date_time'] = pd.to_datetime(df['date_time'])
        df.set_index('date_time', inplace=True)

        if frequency == 'daily':
            resampled_data = df.resample('D').sum()
        elif frequency == 'monthly':
            resampled_data = df.resample('M').sum()
        elif frequency == 'yearly':
            resampled_data = df.resample('Y').sum()
        else:
            print("Invalid frequency provided.")
            return None

        dates = resampled_data.index
        total_prices = resampled_data['total_price']
        return plot_sales_data(dates, total_prices, frequency, start_date, end_date)

    except Exception as e:
        print(f"Error in generating report: {e}")
        return None

