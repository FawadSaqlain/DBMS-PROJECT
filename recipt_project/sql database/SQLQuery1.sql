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
-- drop table Employ
-- CREATE TABLE Employ (
--     username NVARCHAR(100) PRIMARY KEY,
--     user_type NVARCHAR(1000),
--     cnic NVARCHAR(1000),
--     phone_number NVARCHAR(1000),
--     updated_datetime DATETIME,
--     address NVARCHAR(1000),
-- )

-- INSERT INTO Employ (username, user_type, cnic, phone_number, updated_datetime, address)VALUES ('fawad', 'administration manager', '3660302698539', '03316963802', '2020-04-12', 'mumtazgarden');
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
-- SELECT * FROM _gvmm0
-- SELECT * FROM _mjn2P
-- SELECT * FROM _lbkVh
SELECT * FROM _fLIIa
-- SELECT * FROM EMPLOY
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
-- drop table customers

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
-- ('Henry Brooks', 'henry.brooks1@example.com', 'Emma Bell', 'RC022', 260, '2025-2-22 13:30:00'),
-- ('Emily Reed', 'emily.reed1@example.com', 'Aiden Gray', 'RC023', 300, '2025-2-23 11:00:00'),
-- ('Ella Stewart', 'ella.stewart1@example.com', 'Jackson Diaz', 'RC024', 175, '2025-4-24 09:15:00'),
-- ('Aiden Murphy', 'aiden.murphy1@example.com', 'Liam Lopez', 'RC025', 4100, '2025-4-25 16:00:00'),
-- ('Amelia Fisher', 'amelia.fisher1@example.com', 'James Reed', 'RC026', 320, '2025-6-26 14:10:00'),
-- ('Oliver Bell', 'oliver.bell1@example.com', 'Mason Perry', 'RC027', 220, '2025-6-27 15:35:00'),
-- ('Emma King', 'emma.king1@example.com', 'Sophia Sanders', 'RC028', 140, '2025-8-28 12:45:00'),
-- ('Sophia Carter', 'sophia.carter1@example.com', 'Mia Ross', 'RC029', 3, '2025-8-29 11:25:00'),
-- ('Jackson Morris', 'jackson.morris1@example.com', 'Henry Kelly', 'RC030', 270, '2025-10-30 16:30:00'),
-- ('Lucas Mitchell', 'lucas.mitchell1@example.com', 'Charlotte Adams', 'RC100', 20, '2025-11-07 12:10:00');
