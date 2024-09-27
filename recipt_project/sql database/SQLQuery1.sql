-- Check if the table exists and drop it


-- Create the table
-- CREATE DATABASE GENERALSTORE_MS

-- DROP DATABASE GENERALSTORE_MS

USE GENERALSTORE_MS

-- CREATE TABLE customers (
--     id INT PRIMARY KEY IDENTITY,
--     name NVARCHAR(100),
--     email NVARCHAR(100),
--     Employ_name NVARCHAR(100),
--     recipt_code NVARCHAR(100) NOT NULL UNIQUE,
--     total_price INT,
--     date_time DATETIME
-- );

-- CREATE TABLE product(
--     prod_code NVARCHAR(100) PRIMARY KEY,
--     product_description NVARCHAR(1000),
--     prod_quant INT,
--     prod_sale_price FLOAT,
--     quantity_price_sale FLOAT,
--     updated_datetime DATETIME,
--     added_by_employ NVARCHAR(100),
-- )

-- IF OBJECT_ID('customers', 'U') IS NOT NULL
-- BEGIN
    -- DROP TABLE customers;
-- END
-- DROP TABLE product;

-- SELECT * FROM information_schema.tables WHERE table_name = 'product';
-- SELECT * FROM information_schema.tables WHERE table_name = 'customers';

SELECT * FROM product
SELECT * FROM customers
-- SELECT * FROM _CDKIB