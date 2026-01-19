-- Database for Book Microservice
DROP DATABASE IF EXISTS bookstore_book;
CREATE DATABASE bookstore_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bookstore_book;

-- Book table
CREATE TABLE books_book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_author (author)
) ENGINE=InnoDB;

-- Sample data for testing
INSERT INTO books_book (title, author, price, stock) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 12.99, 50),
('To Kill a Mockingbird', 'Harper Lee', 14.99, 30),
('1984', 'George Orwell', 13.99, 40),
('Pride and Prejudice', 'Jane Austen', 11.99, 25),
('The Catcher in the Rye', 'J.D. Salinger', 12.49, 35);
