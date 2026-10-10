CREATE TABLE IF NOT EXISTS Customers (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    inn VARCHAR(50),
    address VARCHAR(255),
    phone VARCHAR(50),
    type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Orders (
    id INT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
);

CREATE TABLE IF NOT EXISTS Products (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Order_items (
    id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE IF NOT EXISTS Materials (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Specification (
    id INT PRIMARY KEY,
    product_id INT NOT NULL,
    material_id INT NOT NULL,
    qty DECIMAL(10, 4) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(id),
    FOREIGN KEY (material_id) REFERENCES Materials(id)
);

CREATE TABLE IF NOT EXISTS Prices (
    id INT PRIMARY KEY,
    item_id INT NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Sales (
    id INT PRIMARY KEY,
    item_id INT NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    discount_percent DECIMAL(5, 2) NOT NULL
);