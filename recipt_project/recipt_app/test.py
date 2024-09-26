# def create_table_recipt(recipt_code, products):
#     """
#     Creates a receipt-specific table and inserts product data.
#     """
#     try:
#         with connection.cursor() as cursor:
#             # Drop the table if it exists
#             cursor.execute(f"""
#                 IF OBJECT_ID(N'{recipt_code}', 'U') IS NOT NULL
#                 DROP TABLE [{recipt_code}]
#             """)
            
#             # Create the new table
#             cursor.execute(f"""
#                 CREATE TABLE [{recipt_code}] (
#                     id INT PRIMARY KEY IDENTITY,
#                     prod_code NVARCHAR(100),
#                     prod_discreption NVARCHAR(1000),
#                     quantity INT,
#                     price FLOAT,
#                     price_quantity FLOAT
#                 )
#             """)
        
#         # Insert data into the new table
#         insert_data(recipt_code, products)
#     except Exception as e:
#         print(f"Error creating receipt table: {e}")
