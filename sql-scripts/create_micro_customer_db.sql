-- Database for Customer Microservice
DROP DATABASE IF EXISTS bookstore_customer;
CREATE DATABASE bookstore_customer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bookstore_customer;

-- Customer table
CREATE TABLE customers_customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;
