-- Database for Cart Microservice
DROP DATABASE IF EXISTS bookstore_cart;
CREATE DATABASE bookstore_cart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bookstore_cart;

-- Cart table (customer_id is a reference to external service)
CREATE TABLE carts_cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id)
) ENGINE=InnoDB;

-- CartItem table (book_id is a reference to external service)
CREATE TABLE carts_cartitem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts_cart(id) ON DELETE CASCADE,
    INDEX idx_cart (cart_id),
    INDEX idx_book (book_id),
    UNIQUE KEY unique_cart_book (cart_id, book_id)
) ENGINE=InnoDB;
