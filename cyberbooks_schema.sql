-- ============================================================================
-- CyberBooks Database Schema
-- MySQL Database Creation Script
-- ============================================================================
-- Description: Complete database schema for CyberBooks e-commerce platform
-- Date: January 20, 2026
-- Database: MySQL 5.7+ or 8.0+
-- ============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS cyberbooks 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE cyberbooks;

-- ============================================================================
-- DROP TABLES (if exists) - For clean installation
-- ============================================================================

DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

-- ============================================================================
-- TABLE: users
-- Description: User accounts and authentication
-- ============================================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME DEFAULT NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: categories
-- Description: Book categories (Network Security, Cryptography, etc.)
-- ============================================================================

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: books
-- Description: Book catalog with pricing and details
-- ============================================================================

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    file_format VARCHAR(10) DEFAULT 'PDF',
    file_path VARCHAR(255),
    cover_image VARCHAR(255),
    category_id INT,
    stock INT DEFAULT 999,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_category (category_id),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    CHECK (price >= 0),
    CHECK (stock >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: orders
-- Description: Customer orders
-- ============================================================================

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    payment_method VARCHAR(50) DEFAULT 'simulated',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_number (order_number),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (total_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: order_items
-- Description: Items in each order
-- ============================================================================

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT DEFAULT 1,
    price DECIMAL(10, 2) NOT NULL,
    INDEX idx_order_id (order_id),
    INDEX idx_book_id (book_id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT,
    CHECK (quantity > 0),
    CHECK (price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: reviews
-- Description: Book reviews and ratings
-- ============================================================================

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_book_id (book_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_book_review (user_id, book_id),
    CHECK (rating >= 1 AND rating <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: cart_items
-- Description: Shopping cart items
-- ============================================================================

CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT DEFAULT 1,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_book_id (book_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_book_cart (user_id, book_id),
    CHECK (quantity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT SAMPLE DATA
-- ============================================================================

-- Insert Categories
INSERT INTO categories (name, description) VALUES
('Network Security', 'Books about network protocols, firewalls, and network defense'),
('Cryptography', 'Encryption, decryption, and cryptographic algorithms'),
('Ethical Hacking', 'Penetration testing and ethical hacking techniques'),
('Digital Forensics', 'Computer forensics and digital investigation'),
('Malware Analysis', 'Analyzing and understanding malicious software'),
('Web Security', 'Web application security and OWASP guidelines');

-- Insert Admin User
-- Password: admin123 (bcrypt hashed)
-- Note: This is a bcrypt hash of 'admin123' - Change this password after first login!
INSERT INTO users (username, email, password_hash, full_name, is_admin, created_at) VALUES
('admin', 'admin@cyberbooks.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LV7W8Oy5C', 'Administrator', TRUE, NOW());

-- Insert Sample Books
INSERT INTO books (title, author, isbn, description, price, file_format, category_id, stock, created_at) VALUES
('Applied Cryptography', 'Bruce Schneier', '9781119096726', 
 'A comprehensive guide to cryptographic protocols, algorithms, and techniques. This book covers modern cryptography from basic concepts to advanced implementations.',
 49.99, 'PDF', 
 (SELECT id FROM categories WHERE name = 'Cryptography'),
 999, NOW()),

('The Web Application Hacker''s Handbook', 'Dafydd Stuttard', '9781118026472',
 'Finding and exploiting security flaws in web applications. An essential guide for security professionals and developers.',
 44.99, 'PDF',
 (SELECT id FROM categories WHERE name = 'Ethical Hacking'),
 999, NOW()),

('Network Security Essentials', 'William Stallings', '9780134527338',
 'Applications and standards for network security. Covers cryptographic algorithms, protocols, and network security applications.',
 39.99, 'ePub',
 (SELECT id FROM categories WHERE name = 'Network Security'),
 999, NOW()),

('The Art of Memory Forensics', 'Michael Hale Ligh', '9781118825099',
 'Detecting malware and threats in Windows, Linux, and Mac memory. A comprehensive guide to memory forensics.',
 54.99, 'PDF',
 (SELECT id FROM categories WHERE name = 'Digital Forensics'),
 999, NOW()),

('Practical Malware Analysis', 'Michael Sikorski', '9781593272906',
 'The hands-on guide to dissecting malicious software. Learn how to analyze malware and understand its behavior.',
 42.99, 'PDF',
 (SELECT id FROM categories WHERE name = 'Malware Analysis'),
 999, NOW()),

('Web Application Security', 'Andrew Hoffman', '9781492053118',
 'Exploitation and countermeasures for modern web applications. Learn about common vulnerabilities and how to prevent them.',
 38.99, 'ePub',
 (SELECT id FROM categories WHERE name = 'Web Security'),
 999, NOW()),

('Penetration Testing', 'Georgia Weidman', '9781593275648',
 'A hands-on introduction to hacking. Learn the fundamentals of penetration testing and ethical hacking.',
 45.99, 'PDF',
 (SELECT id FROM categories WHERE name = 'Ethical Hacking'),
 999, NOW()),

('Cryptography Engineering', 'Niels Ferguson', '9780470474242',
 'Design principles and practical applications. Learn how to build secure systems using cryptography.',
 47.99, 'PDF',
 (SELECT id FROM categories WHERE name = 'Cryptography'),
 999, NOW());

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify table creation
SELECT 'Database tables created successfully!' AS Status;

-- Show table statistics
SELECT 
    'users' AS table_name, COUNT(*) AS record_count FROM users
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'books', COUNT(*) FROM books
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'cart_items', COUNT(*) FROM cart_items;

-- ============================================================================
-- USEFUL QUERIES FOR TESTING
-- ============================================================================

-- View all categories with book counts
-- SELECT c.id, c.name, COUNT(b.id) as book_count
-- FROM categories c
-- LEFT JOIN books b ON c.id = b.category_id
-- GROUP BY c.id, c.name
-- ORDER BY c.name;

-- View all books with category names
-- SELECT b.id, b.title, b.author, b.price, c.name as category, b.stock
-- FROM books b
-- LEFT JOIN categories c ON b.category_id = c.id
-- ORDER BY b.created_at DESC;

-- View all users
-- SELECT id, username, email, full_name, is_admin, created_at
-- FROM users
-- ORDER BY created_at DESC;

-- ============================================================================
-- ADMIN USER CREDENTIALS
-- ============================================================================
-- Username: admin
-- Password: admin123
-- 
-- IMPORTANT: Change this password immediately after first login!
-- ============================================================================

-- End of script
