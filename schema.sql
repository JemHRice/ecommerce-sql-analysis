-- Drop tables if they exist
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Customers table
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_age INTEGER,
    customer_gender VARCHAR(10),
    region VARCHAR(50)
);

-- Products table
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    category VARCHAR(50),
    price DECIMAL(10,2)
);

-- Orders table
CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10),
    order_date DATE,
    payment_method VARCHAR(50),
    shipping_cost DECIMAL(10,2),
    delivery_time_days INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order items table
CREATE TABLE order_items (
    order_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity INTEGER,
    discount DECIMAL(5,2),
    total_amount DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    returned VARCHAR(3),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);