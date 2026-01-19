-- Database for Clean Architecture
DROP DATABASE IF EXISTS bookstore_clean;
CREATE DATABASE bookstore_clean CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bookstore_clean;

-- Customer table
CREATE TABLE infrastructure_customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- Book table
CREATE TABLE infrastructure_book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_author (author)
) ENGINE=InnoDB;

-- Cart table
CREATE TABLE infrastructure_cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES infrastructure_customer(id) ON DELETE CASCADE,
    INDEX idx_customer (customer_id)
) ENGINE=InnoDB;

-- CartItem table
CREATE TABLE infrastructure_cartitem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES infrastructure_cart(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES infrastructure_book(id) ON DELETE CASCADE,
    INDEX idx_cart (cart_id),
    INDEX idx_book (book_id),
    UNIQUE KEY unique_cart_book (cart_id, book_id)
) ENGINE=InnoDB;

-- Sample data for testing
INSERT INTO infrastructure_book (title, author, price, stock) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 12.99, 50),
('To Kill a Mockingbird', 'Harper Lee', 14.99, 30),
('1984', 'George Orwell', 13.99, 40),
('Pride and Prejudice', 'Jane Austen', 11.99, 25),
('The Catcher in the Rye', 'J.D. Salinger', 12.49, 35);
