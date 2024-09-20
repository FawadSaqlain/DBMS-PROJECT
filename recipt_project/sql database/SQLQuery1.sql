-- Check if the table exists and drop it
IF OBJECT_ID('customers', 'U') IS NOT NULL
BEGIN
    DROP TABLE customers;
END

-- Create the table
CREATE TABLE customers (
    id INT PRIMARY KEY IDENTITY,
    name NVARCHAR(100),
    email NVARCHAR(100),
    Employ_name NVARCHAR(100),
    recipt_no NVARCHAR(100) NOT NULL UNIQUE,
);
USE reciptapp
SELECT * FROM customers
SELECT * FROM information_schema.tables WHERE table_name = 'customers';


CREATE TABLE product(
    prod_code NVARCHAR(100) PRIMARY KEY,
    product_description NVARCHAR(1000),
    prod_quant INT,
    prod_sale_price FLOAT,
    quantity_price_sale FLOAT,
    updated_datetime DATE,
    added_by_employ NVARCHAR(100),
)
SELECT * FROM product
SELECT * FROM information_schema.tables WHERE table_name = 'product';
