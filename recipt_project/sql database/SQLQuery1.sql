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

-- CREATE TABLE customers_return (
--     id INT PRIMARY KEY IDENTITY,
--     name NVARCHAR(100),
--     email NVARCHAR(100),
--     Employ_name NVARCHAR(100),
--     recipt_code_buy NVARCHAR(100) NOT NULL,
--     recipt_code_return NVARCHAR(100) NOT NULL UNIQUE,
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

-- DROP TABLE customers;
-- DROP TABLE customers_return;
-- DROP TABLE _gvmm0
-- DROP TABLE _RmnrO

-- SELECT * FROM information_schema.tables WHERE table_name = 'product';
-- SELECT * FROM information_schema.tables WHERE table_name = 'customers';

-- SELECT * FROM Product
-- ORDER BY prod_code ASC;  -- Sorts the products by price in ascending order
-- SELECT * FROM product
SELECT * FROM customers
SELECT * FROM customers_return
SELECT * FROM _gvmm0
SELECT * FROM _mjn2P
SELECT * FROM _lbkVh
-- drop table _4AWX0
-- update _XCLsB set quantity=20 where prod_code='iQz22'
-- SELECT * FROM customers WHERE recipt_code = '_d407j'
-- SELECT * FROM Product
-- WHERE LOWER(prod_code) LIKE LOWER('%mp%')
--    OR LOWER(product_description) LIKE LOWER('%mp%')
--    OR LOWER(CAST(prod_quant AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(prod_sale_price AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(quantity_price_sale AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(updated_datetime  AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(added_by_employ AS VARCHAR(50))) LIKE LOWER('%mp%')

-- SELECT * FROM Product
-- WHERE LOWER(%s) LIKE LOWER('%s')