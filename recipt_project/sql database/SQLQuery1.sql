-- CREATE DATABASE GENERALSTORE_MS

-- DROP DATABASE GENERALSTORE_MS

USE GENERALSTORE_MS;

INSERT INTO Employ (username, user_type, cnic, phone_number, updated_datetime, address) 
VALUES ('fawad', 'administration manager', '36603-0269853-9', '+9230228730277', '2020-04-12', 'mumtazgarden');

INSERT INTO Employ (username, user_type, cnic, phone_number, updated_datetime, address) 
VALUES ('tyui', 'administration manager', '36601-8596363-0', '+923254246836', '2019-04-12', 'every where');

SELECT * from employ

-- Declare the scalar variable @sql
-- DECLARE @sql NVARCHAR(MAX) = '';

-- -- Build the DROP TABLE statements for tables starting with '_'
-- SELECT @sql = @sql + 'DROP TABLE ' + QUOTENAME(TABLE_NAME) + ';' + CHAR(13)
-- FROM INFORMATION_SCHEMA.TABLES
-- WHERE TABLE_NAME LIKE '_%' AND TABLE_SCHEMA = 'dbo';

-- -- Print the generated SQL for verification (optional)
-- PRINT @sql;

-- -- Execute the dynamic SQL to drop the tables
-- IF @sql <> ''
--     EXEC sp_executesql @sql;
-- ELSE
--     PRINT 'No tables to drop.';


-- DROP TABLE django_content_type;
-- DROP TABLE django_migrations;
-- DROP TABLE auth_user;

-- Drop other tables as necessary
-- IF OBJECT_ID('customers', 'U') IS NOT NULL
-- BEGIN
    -- DROP TABLE customers;
-- END
-- DROP TABLE product;

-- DROP TABLE customers;
-- DROP TABLE customers_return;

-- DROP TABLE _ZzCPB


-- CREATE TABLE customers (
--     id INT PRIMARY KEY IDENTITY(1,1),
--     name NVARCHAR(100),
--     email NVARCHAR(100),
--     Employ_name NVARCHAR(100),
--     recipt_code NVARCHAR(6) NOT NULL UNIQUE,
--     total_price FLOAT CHECK (total_price >= 0.0),
--     date_time DATETIME
-- );

-- CREATE TABLE customers_return (
--     id INT,
--     name NVARCHAR(100),
--     email NVARCHAR(100),
--     Employ_name NVARCHAR(100),
--     recipt_code_buy NVARCHAR(6) NOT NULL,
--     recipt_code_return NVARCHAR(6) NOT NULL UNIQUE,
--     total_price FLOAT CHECK (total_price >= 0.0),
--     date_time DATETIME
-- );


-- CREATE TABLE product (
--     prod_code NVARCHAR(5) PRIMARY KEY,
--     product_description NVARCHAR(255) NOT NULL UNIQUE,  -- Change TEXT to NVARCHAR(255) for efficiency
--     prod_quant INT CHECK (prod_quant >= 0),  -- Ensures quantity is at least 1
--     prod_sale_price FLOAT CHECK (prod_sale_price >= 0.0),  -- Ensures sale price is at least 0.0
--     quantity_price_sale FLOAT CHECK (quantity_price_sale >= 0.0),  -- Ensures quantity price sale is at least 0.0
--     updated_datetime DATETIME,
--     added_by_employ TEXT
-- );

-- CREATE TABLE Employ (
--     username NVARCHAR(100) PRIMARY KEY NOT NULL,
--     user_type NVARCHAR(50) NOT NULL, -- Reduced size for user_type
--     cnic NVARCHAR(15) NOT NULL UNIQUE,
--     phone_number NVARCHAR(15) NOT NULL, -- Increased size to handle '+923...' format
--     updated_datetime DATETIME NOT NULL,
--     address NVARCHAR(MAX) NOT NULL -- Use NVARCHAR(MAX) instead of TEXT for compatibility
-- );


-- SELECT * FROM Product
-- WHERE LOWER(prod_code) LIKE LOWER('%mp%')
--    OR LOWER(product_description) LIKE LOWER('%mp%')
--    OR LOWER(CAST(prod_quant AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(prod_sale_price AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(quantity_price_sale AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(updated_datetime  AS VARCHAR(50))) LIKE LOWER('%mp%')
--    OR LOWER(CAST(added_by_employ AS VARCHAR(50))) LIKE LOWER('%mp%')

-- SELECT * FROM Product WHERE LOWER(%s) LIKE LOWER('%s')

-- SELECT * FROM Product ORDER BY prod_code ASC;  -- Sorts the products by price in ascending order

-- SELECT * FROM product
-- SELECT * FROM customers WHERE recipt_code = '_08u5n';
-- SELECT * FROM EMPLOY
-- SELECT * FROM customers_return

-- drop table customers_return
-- drop table product
-- drop table customers
-- drop table Employ
-- DROP TABLE _gvmm0


-- UPDATE customers 
-- SET name = 'as', email = 'daasd@sdfdf.com' 
-- WHERE recipt_code = '_08u5n';



-- UPDATE product set prod_quant = 95 where prod_code='p0001';
-- UPDATE product SET quantity_price_sale = prod_quant * prod_sale_price;

-- select * from product where prod_code='p0045'
-- SELECT * FROM dbo.product
-- inserted dummy products and customers 




    -- INSERT INTO customers (name, email, Employ_name, recipt_code, total_price, date_time) VALUES 
    -- ('John Doe', 'john.doe1@example.com', 'Alice Smith', 'RC001', 1200, '2024-3-01 14:30:00'),
    -- ('Jane Smith', 'jane.smith1@example.com', 'Bob Johnson', 'RC002', 250, '2024-5-02 15:45:00'),
    -- ('Michael Brown', 'michael.brown1@example.com', 'Charlie Davis', 'RC003', 300, '2024-5-03 12:00:00'),
    -- ('Emily Johnson', 'emily.johnson1@example.com', 'Diana White', 'RC004', 9000, '2024-6-04 18:20:00'),
    -- ('Chris Lee', 'chris.lee1@example.com', 'Edward Taylor', 'RC005', 150, '2024-6-05 09:15:00'),
    -- ('Sarah Parker', 'sarah.parker1@example.com', 'Frank Miller', 'RC006', 17235, '2024-6-06 14:10:00'),
    -- ('David Clark', 'david.clark1@example.com', 'George Hall', 'RC007', 200, '2024-7-07 17:05:00'),
    -- ('Laura Adams', 'laura.adams1@example.com', 'Hannah Scott', 'RC008', 23230, '2024-8-08 10:40:00'),
    -- ('Tom King', 'tom.king1@example.com', 'Isaac Lewis', 'RC009', 340, '2024-8-09 11:25:00'),
    -- ('Amy Wright', 'amy.wright1@example.com', 'Jack Evans', 'RC010', 27320, '2024-8-10 13:50:00'),
    -- ('Nathan Hill', 'nathan.hill1@example.com', 'Laura Martin', 'RC011', 480, '2024-9-11 16:30:00'),
    -- ('Oliver Green', 'oliver.green1@example.com', 'Mia Robinson', 'RC012', 220, '2024-9-12 14:05:00'),
    -- ('Liam Scott', 'liam.scott1@example.com', 'Noah Walker', 'RC013', 30320, '2024-10-13 12:30:00'),
    -- ('Sophia White', 'sophia.white1@example.com', 'Ella Young', 'RC014', 125, '2024-10-14 09:50:00'),
    -- ('Mason Lewis', 'mason.lewis1@example.com', 'Lucas Baker', 'RC015', 150, '2024-11-15 17:45:00'),
    -- ('Isabella Clark', 'isabella.clark1@example.com', 'Charlotte Adams', 'RC016', 22375, '2024-11-16 14:20:00'),
    -- ('William Harris', 'william.harris1@example.com', 'Sophia King', 'RC017', 390, '2024-11-17 13:15:00'),
    -- ('Ava Perez', 'ava.perez1@example.com', 'Henry Mitchell', 'RC018', 180, '2024-11-18 15:55:00'),
    -- ('James Turner', 'james.turner1@example.com', 'Amelia Carter', 'RC019', 320, '2024-12-19 12:25:00'),
    -- ('Charlotte Evans', 'charlotte.evans1@example.com', 'Oliver Morris', 'RC020', 21320, '2024-12-20 14:40:00'),
    -- ('Lucas Martin', 'lucas.martin1@example.com', 'Ella Peterson', 'RC021', 160, '2024-12-21 10:50:00'),
    -- ('Henry Brooks', 'henry.brooks1@example.com', 'Emma Bell', 'RC022', 260, '2023-2-22 13:30:00'),
    -- ('Emily Reed', 'emily.reed1@example.com', 'Aiden Gray', 'RC023', 300, '2023-2-23 11:00:00'),
    -- ('Ella Stewart', 'ella.stewart1@example.com', 'Jackson Diaz', 'RC024', 175, '2023-4-24 09:15:00'),
    -- ('Aiden Murphy', 'aiden.murphy1@example.com', 'Liam Lopez', 'RC025', 4100, '2023-4-25 16:00:00'),
    -- ('Amelia Fisher', 'amelia.fisher1@example.com', 'James Reed', 'RC026', 320, '2023-6-26 14:10:00'),
    -- ('Oliver Bell', 'oliver.bell1@example.com', 'Mason Perry', 'RC027', 220, '2023-6-27 15:35:00'),
    -- ('Emma King', 'emma.king1@example.com', 'Sophia Sanders', 'RC028', 140, '2023-8-28 12:45:00'),
    -- ('Sophia Carter', 'sophia.carter1@example.com', 'Mia Ross', 'RC029', 3, '2023-8-29 11:25:00'),
    -- ('Jackson Morris', 'jackson.morris1@example.com', 'Henry Kelly', 'RC030', 270, '2023-10-30 16:30:00'),
    -- ('Lucas Mitchell', 'lucas.mitchell1@example.com', 'Charlotte Adams', 'RC100', 20, '2023-11-07 12:10:00');


    -- INSERT INTO product (prod_code, product_description, prod_quant, prod_sale_price, quantity_price_sale, updated_datetime, added_by_employ) VALUES 
    -- ('p0001', 'Apple iPhone 14', 100, 999.99, 999.99, '2024-12-06 10:00:00', 'John Doe'),
    -- ('p0002', 'Samsung Galaxy S21', 150, 799.99, 799.99, '2024-12-06 10:30:00', 'Jane Smith'),
    -- ('p0003', 'Sony WH-1000XM4 Headphones', 75, 349.99, 349.99, '2024-12-06 11:00:00', 'Michael Brown'),
    -- ('p0004', 'Dell XPS 13 Laptop', 50, 1299.99, 1299.99, '2024-12-06 11:30:00', 'Sarah Lee'),
    -- ('p0005', 'HP Spectre x360', 60, 1499.99, 1499.99, '2024-12-06 12:00:00', 'David Miller'),
    -- ('p0006', 'Canon EOS 5D Mark IV', 30, 2499.99, 2499.99, '2024-12-06 12:30:00', 'Emily Davis'),
    -- ('p0007', 'Nikon D850 DSLR', 40, 2899.99, 2899.99, '2024-12-06 13:00:00', 'John Evans'),
    -- ('p0008', 'GoPro HERO11 Black', 100, 399.99, 399.99, '2024-12-06 13:30:00', 'Alice Carter'),
    -- ('p0009', 'Samsung QLED TV', 80, 799.99, 799.99, '2024-12-06 14:00:00', 'Robert Wilson'),
    -- ('p0010', 'LG OLED TV', 120, 1299.99, 1299.99, '2024-12-06 14:30:00', 'Sophia Clark'),
    -- ('p0011', 'Bose SoundLink Revolve', 90, 199.99, 199.99, '2024-12-06 15:00:00', 'Olivia Moore'),
    -- ('p0012', 'Apple AirPods Pro', 150, 249.99, 249.99, '2024-12-06 15:30:00', 'Jacob Harris'),
    -- ('p0013', 'Samsung Galaxy Tab S7', 60, 649.99, 649.99, '2024-12-06 16:00:00', 'Charlotte Lewis'),
    -- ('p0014', 'Microsoft Surface Pro 7', 45, 749.99, 749.99, '2024-12-06 16:30:00', 'James Walker'),
    -- ('p0015', 'Lenovo ThinkPad X1 Carbon', 70, 1399.99, 1399.99, '2024-12-06 17:00:00', 'Benjamin King'),
    -- ('p0016', 'Asus ROG Strix Laptop', 50, 1599.99, 1599.99, '2024-12-06 17:30:00', 'Mia Martinez'),
    -- ('p0017', 'Apple MacBook Air', 80, 999.99, 999.99, '2024-12-06 18:00:00', 'Lucas Garcia'),
    -- ('p0018', 'Google Pixel 6', 100, 599.99, 599.99, '2024-12-06 18:30:00', 'Ella Perez'),
    -- ('p0019', 'Apple Watch Series 7', 120, 399.99, 399.99, '2024-12-06 19:00:00', 'Liam Robinson'),
    -- ('p0020', 'Fitbit Charge 5', 200, 179.99, 179.99, '2024-12-06 19:30:00', 'Ava Carter'),
    -- ('p0021', 'Dell UltraSharp Monitor', 150, 499.99, 499.99, '2024-12-06 20:00:00', 'Zoe Clark'),
    -- ('p0022', 'Epson EcoTank Printer', 70, 449.99, 449.99, '2024-12-06 20:30:00', 'Ella Adams'),
    -- ('p0023', 'Samsung 970 EVO SSD', 180, 129.99, 129.99, '2024-12-06 21:00:00', 'Mason Turner'),
    -- ('p0024', 'Seagate Expansion 1TB', 250, 59.99, 59.99, '2024-12-06 21:30:00', 'Aiden Phillips'),
    -- ('p0025', 'Kingston HyperX RAM', 200, 79.99, 79.99, '2024-12-06 22:00:00', 'Madison Scott'),
    -- ('p0026', 'Logitech MX Master 3', 150, 99.99, 99.99, '2024-12-06 22:30:00', 'Noah Young'),
    -- ('p0027', 'Razer DeathAdder Elite', 100, 59.99, 59.99, '2024-12-06 23:00:00', 'Grace Nelson'),
    -- ('p0028', 'Bose QuietComfort 35 II', 80, 299.99, 299.99, '2024-12-06 23:30:00', 'Jack Carter'),
    -- ('p0029', 'Apple iPad Pro', 120, 799.99, 799.99, '2024-12-07 00:00:00', 'Harper Green'),
    -- ('p0030', 'Sony PlayStation 5', 50, 499.99, 499.99, '2024-12-07 00:30:00', 'Isabella Turner'),
    -- ('p0031', 'Xbox Series X', 70, 499.99, 499.99, '2024-12-07 01:00:00', 'Daniel Harris'),
    -- ('p0032', 'Nintendo Switch OLED', 90, 349.99, 349.99, '2024-12-07 01:30:00', 'Chloe Lewis'),
    -- ('p0033', 'Samsung Galaxy Buds 2', 150, 149.99, 149.99, '2024-12-07 02:00:00', 'Matthew Walker'),
    -- ('p0034', 'JBL Flip 5 Bluetooth Speaker', 100, 119.99, 119.99, '2024-12-07 02:30:00', 'Emily Johnson'),
    -- ('p0035', 'LG 27GL83A-B Monitor', 80, 379.99, 379.99, '2024-12-07 03:00:00', 'Henry Allen'),
    -- ('p0036', 'Apple Mac Mini', 60, 699.99, 699.99, '2024-12-07 03:30:00', 'Eva Lewis'),
    -- ('p0037', 'Corsair Vengeance RAM', 120, 89.99, 89.99, '2024-12-07 04:00:00', 'Matthew Wright'),
    -- ('p0038', 'BenQ ZOWIE Gaming Monitor', 70, 299.99, 299.99, '2024-12-07 04:30:00', 'Amelia Hall'),
    -- ('p0039', 'Acer Predator Helios 300', 50, 1399.99, 1399.99, '2024-12-07 05:00:00', 'Jack Wilson'),
    -- ('p0040', 'Xiaomi Mi Smart Band 6', 200, 49.99, 49.99, '2024-12-07 05:30:00', 'Lily Harris'),
    -- ('p0041', 'Huawei Watch GT 3', 150, 249.99, 249.99, '2024-12-07 06:00:00', 'Oliver Smith'),
    -- ('p0042', 'Logitech G Pro X Headset', 80, 129.99, 129.99, '2024-12-07 06:30:00', 'Sophie Moore'),
    -- ('p0043', 'Microsoft Xbox Wireless Controller', 100, 59.99, 59.99, '2024-12-07 07:00:00', 'William Young'),
    -- ('p0044', 'Apple TV 4K', 70, 179.99, 179.99, '2024-12-07 07:30:00', 'Grace Evans'),
    -- ('p0045', 'Bose Soundbar 700', 60, 799.99, 799.99, '2024-12-07 08:00:00', 'Nathan Perez'),
    -- ('p0046', 'Razer Kraken V3 Headset', 90, 129.99, 129.99, '2024-12-07 08:30:00', 'Ethan Scott'),
    -- ('p0047', 'Samsung Galaxy Watch 4', 80, 249.99, 249.99, '2024-12-07 09:00:00', 'Chloe Martinez'),
    -- ('p0048', 'Logitech G502 Hero Mouse', 120, 49.99, 49.99, '2024-12-07 09:30:00', 'Isaac King'),
    -- ('p0049', 'Corsair K95 RGB Mechanical Keyboard', 100, 199.99, 199.99, '2024-12-07 10:00:00', 'Mason Lee'),
    -- ('p0050', 'Amazon Echo Show 8', 150, 129.99, 129.99, '2024-12-07 10:30:00', 'Aiden Clark');


-- select * from customers
-- select * from customers_return
-- select * from Employ
-- SELECT * from product where prod_code ='p0008'
-- DELETE from product