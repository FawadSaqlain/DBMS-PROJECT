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

-- SELECT * FROM Product
-- ORDER BY prod_code ASC;  -- Sorts the products by price in ascending order
SELECT * FROM Product
-- SELECT * FROM customers
-- SELECT * FROM _CDKIB

-- SELECT * FROM Product
-- WHERE prod_code LIKE '%9%'
--    OR product_description LIKE '%9%'
--    OR prod_quant LIKE '%9%'
--    OR prod_sale_price LIKE '%9%'
--    OR quantity_price_sale LIKE '%9%'
--    OR updated_datetime LIKE '%9%'
--    OR added_by_employ LIKE '%9%'

-- SELECT * FROM Product
-- WHERE LOWER(prod_code) LIKE LOWER('%00%')
--    OR LOWER(product_description) LIKE LOWER('%00%')
--    OR LOWER(CAST(prod_quant AS VARCHAR(50))) LIKE LOWER('%00%')
--    OR LOWER(CAST(prod_sale_price AS VARCHAR(50))) LIKE LOWER('%00%')
--    OR LOWER(CAST(quantity_price_sale AS VARCHAR(50))) LIKE LOWER('%00%')
--    OR LOWER(CAST(updated_datetime  AS VARCHAR(50))) LIKE LOWER('%00%')
--    OR LOWER(CAST(added_by_employ AS VARCHAR(50))) LIKE LOWER('%00%')

-- DECLARE @searchTerms NVARCHAR(100) = 'am';  -- replace '00' with your search term
-- SELECT * FROM Product
-- WHERE CONTAINS((prod_code, product_description, added_by_employ), @searchTerms)
--    OR CAST(prod_quant AS VARCHAR(50)) LIKE '%' + @searchTerms + '%'
--    OR CAST(prod_sale_price AS VARCHAR(50)) LIKE '%' + @searchTerms + '%'
--    OR CAST(quantity_price_sale AS VARCHAR(50)) LIKE '%' + @searchTerms + '%'
--    OR CAST(updated_datetime AS VARCHAR(50)) LIKE '%' + @searchTerms + '%';

-- Step 2: Create a Full-Text Catalog
CREATE FULLTEXT CATALOG ProductCatalog AS DEFAULT;

-- Step 3: Create a Unique Index on prod_code
CREATE UNIQUE INDEX UQ_Product_Code ON Product(prod_code);

-- Step 4: Create the Full-Text Index
CREATE FULLTEXT INDEX ON Product (prod_code, product_description, added_by_employ)
KEY INDEX UQ_Product_Code
WITH CHANGE_TRACKING AUTO;

DECLARE @searchTerms NVARCHAR(100) = 'am';  -- Replace with your search term
SELECT * FROM Product
WHERE CONTAINS((prod_code, product_description, added_by_employ), @searchTerms)
   OR CAST(prod_quant AS VARCHAR(50)) LIKE '%' + @searchTerms + '%'
   OR CAST(prod_sale_price AS VARCHAR(50)) LIKE '%' + @searchTerms + '%'
   OR CAST(quantity_price_sale AS VARCHAR(50)) LIKE '%' + @searchTerms + '%'
   OR CAST(updated_datetime AS VARCHAR(50)) LIKE '%' + @searchTerms + '%';
