-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2026 at 07:56 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cyberbooks`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author` varchar(100) NOT NULL,
  `isbn` varchar(13) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `file_format` varchar(10) DEFAULT 'PDF',
  `file_path` varchar(255) DEFAULT NULL,
  `cover_image` varchar(255) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `isbn`, `description`, `price`, `file_format`, `file_path`, `cover_image`, `category_id`, `created_at`, `updated_at`) VALUES
(1, 'Applied Cryptography', 'Bruce Schneier', '9781119096726', 'A comprehensive guide to cryptographic protocols, algorithms, and techniques. This book covers modern cryptography from basic concepts to advanced implementations.', 49.99, 'PDF', 'books/d281dc51c83e4b6085781aa3edd52913_Network_Optimization.pdf', 'img/books/ddf3074418824e06bad69abab9a9129f_4137JFJWbiL._AC_UF8941000_QL80_.jpg', 2, '2026-01-20 07:32:11', '2026-01-27 22:32:03'),
(2, 'The Web Application Hacker\'s Handbook', 'Dafydd Stuttard', '9781118026472', 'Finding and exploiting security flaws in web applications. An essential guide for security professionals and developers.', 44.99, 'PDF', 'books/f0b9509dc4ef48eba2b913e920a38596_Network_Programming_with_Go.pdf', 'img/books/5db6566449884e1e90102246a71b2d13_webhac-1.jpg', 3, '2026-01-20 07:32:11', '2026-01-27 22:52:34'),
(3, 'Network Security Essentials', 'William Stallings', '9780134527338', 'Applications and standards for network security. Covers cryptographic algorithms, protocols, and network security applications.', 39.99, 'ePub', 'books/ba246a6c8713451398148106616d6d4c_Introduction_to_Network_Security_2008_CRC_Press_libgen_li.pdf', 'img/books/6fd1523a042f4373a421c02525ad7ab8_299641.jpg', 1, '2026-01-20 07:32:11', '2026-01-27 22:54:37'),
(4, 'The Art of Memory Forensics', 'Michael Hale Ligh', '9781118825099', 'Detecting malware and threats in Windows, Linux, and Mac memory. A comprehensive guide to memory forensics.', 54.99, 'PDF', 'books/16501bf75f454a75ae6de38c4cf138c8_The_Art_of_Hardware_Architecture.pdf', 'img/books/67dc60329e2146b0915e1ba21da4d4b6_1200x1200wz.jpg', 4, '2026-01-20 07:32:11', '2026-01-27 23:01:37'),
(5, 'Practical Malware Analysis', 'Michael Sikorski', '9781593272906', 'The hands-on guide to dissecting malicious software. Learn how to analyze malware and understand its behavior.', 42.99, 'PDF', 'books/f1cad49a8d9a4c8cb5a2cdd4a0cfc903_Smith_Craig_The_Car_Hackers_Handbook_A_Guide_for_the_Penetration.pdf', 'img/books/923710946cae4fb3afb212b65294ffdd_81GSW7Ee2eL._UF10001000_QL80_.jpg', 5, '2026-01-20 07:32:11', '2026-01-27 23:08:42'),
(6, 'Web Application Security', 'Andrew Hoffman', '9781492053118', 'Exploitation and countermeasures for modern web applications. Learn about common vulnerabilities and how to prevent them.', 38.99, 'ePub', 'books/217b1163def64e60a882de0fb2d457c1_Big_Data_and_Analytics_Applications_in_Government__Current.pdf', 'img/books/3cedcd208b2440d4b0332f1bcc341f94_61g7nrKv7KL._UF350350_QL50_.jpg', 6, '2026-01-20 07:32:11', '2026-01-27 23:10:42'),
(7, 'Penetration Testing', 'Georgia Weidman', '9781593275648', 'A hands-on introduction to hacking. Learn the fundamentals of penetration testing and ethical hacking.', 45.99, 'PDF', 'books/4c904caaef164d828965c3fc8c9570af_Penetration_Testing_with_Kali_NetHunter_Gerald_Tripp_Roybal_III.pdf', 'img/books/121bd931e2bb42dc8a620a12777d2e72_978-1-4842-1857-0.jpg', 3, '2026-01-20 07:32:11', '2026-01-27 23:12:01'),
(8, 'Cryptography Engineering', 'Niels Ferguson', '9780470474242', 'Design principles and practical applications. Learn how to build secure systems using cryptography.', 47.99, 'PDF', 'books/1d5b23ec41f4469abeff226d2553ec15_Cryptography_101_From_Theory_to_Practice.pdf', 'img/books/c9b15aeae127432898eb171d55e5f2fd_photo_2026-01-27_23-14-36.jpg', 2, '2026-01-20 07:32:11', '2026-01-27 23:16:33'),
(10, 'A Visual History of Cybersecurity', 'Jame Dineal', '11141414224', 'We hope this book provides a compelling visual snapshot of the history that led the cyber industry to where it is, along with our bold predictions for the future', 13.00, 'PDF', 'books/51633ddcfb7a45dfb60d52062be2a793_A_Visual_History_of_Cybersecurity-optiv.com_2020.pdf', 'img/books/4cebde80e2d64fd1b977be5a360382ef_978-3-319-75307-2.jpg', 1, '2026-01-24 08:21:10', '2026-01-24 08:38:10'),
(11, 'The Art of Hardware Architecture', 'Mohit Arora', '9781461403975', 'The original idea behind “The Art of Hardware Architecture” was to link my years of experience as a design architect with the extensive research I have conducted. However, achieving the final shape of this book would not have been possible without many contributions.', 20.00, 'PDF', 'books/c177a9f1e44b488eab6498f05b47de4a_The_Art_of_Hardware_Architecture.pdf', 'img/books/7cad370241c846baaf6b0ec6fc3ca432_photo_2026-01-28_09-39-06.jpg', 1, '2026-01-28 09:41:05', '2026-01-28 09:41:05'),
(12, 'The Psychology of Cybersecurity', 'Tranveer Singh and Sarah Y. Zheng', ' 978104041838', 'This book takes a fresh look at the underappreciated role of human psychology in cybersecurity and information technology management. It discusses the latest insights from practice and scholarly work on the role of cognitive bias and human factors in critical decisions that could affect the lives of many people.', 34.00, 'PDF', 'books/de921081eae747c187a38d1e99592c7e_The_Psychology_of_Cybersecurity_Hacking_and_the_Human_Mind.pdf', 'img/books/475b092759eb45ed8b45e7ae636508e2_photo_2026-01-28_09-42-07.jpg', 3, '2026-01-28 09:44:14', '2026-01-28 09:44:14'),
(13, 'Ethical Hacking with Python', 'Abdeladim Fadheli', '8335265164', 'Python is a high-level, general-purpose interpreted programming language. It is designed to be highly readable and easy to use. Today, it\'s widely used in many domains, such as data science, web development, software development, and ethical hacking. With its flexibility and popular and unlimited libraries, you can use it to build your penetration testing tools.', 30.00, 'PDF', 'books/6536b713136147efb7c48dabafbaf10a_Ethical_Hacking_with_Python.pdf', 'img/books/cc5b9d7ea643445eac9f1c4bf5e6fc9e_photo_2026-01-28_09-45-20.jpg', 3, '2026-01-28 09:47:04', '2026-01-28 09:47:04'),
(14, 'Hacking Product Design', 'Tony Jing', '9781484239841', 'This book attempts to answer that question. Years ago, when I switched from graphic design to product design, I had the exact same question. I wished there was a book that covered all the soft skills related to designing products for startups.', 25.00, 'PDF', 'books/5ee98f0b63f441b7826958cbc19a3785_Hacking_Product_Design_A_Guide_to_Designing_Products_for_Startups.pdf', 'img/books/acf876f713a443d99b844d5e4d4e6c65_photo_2025-07-12_06-27-56.jpg', 3, '2026-01-28 10:53:12', '2026-01-28 10:53:12'),
(15, 'Malware Development for Ethical Hackers', 'Zhassulan Zhussupov', '9781801076975', 'Learn how to develop various types of malware to strengthen cybersecurity', 12.00, 'ePub', 'books/d7d26d9d5c9c4e82875b290336b822cc_Malware_Development_for_Ethical_Hackers_Learn_how_to_develop_various.epub', 'img/books/85e50a398de248d196ae41e84b1bd5c9_photo_2026-01-28_10-56-18.jpg', 5, '2026-01-28 10:59:40', '2026-01-28 10:59:40');

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

CREATE TABLE `cart_items` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `added_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cart_items`
--

INSERT INTO `cart_items` (`id`, `user_id`, `book_id`, `added_at`) VALUES
(4, 2, 15, '2026-01-28 11:00:19'),
(12, 4, 13, '2026-01-28 22:28:18');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'Network Security', 'Books about network protocols, firewalls, and network defense'),
(2, 'Cryptography', 'Encryption, Decryption, and Cryptographic Algorithms'),
(3, 'Ethical Hacking', 'Penetration testing and ethical hacking techniques'),
(4, 'Digital Forensics', 'Computer forensics and digital investigation'),
(5, 'Malware Analysis', 'Analyzing and understanding malicious software'),
(6, 'Web Security', 'Web application security and OWASP guidelines');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `order_number` varchar(20) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `status` varchar(20) DEFAULT 'completed',
  `payment_method` varchar(50) DEFAULT 'simulated',
  `created_at` datetime DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `order_number`, `total_amount`, `status`, `payment_method`, `created_at`) VALUES
(1, 2, 'ORD-20260121063116-0', 49.99, 'completed', 'simulated', '2026-01-21 06:31:16'),
(2, 2, 'ORD-20260124084402-B', 13.00, 'completed', 'simulated', '2026-01-24 08:44:02'),
(3, 4, 'ORD-20260128130107-N', 25.00, 'completed', 'stripe', '2026-01-28 13:01:07'),
(4, 4, 'ORD-20260128130654-J', 12.00, 'completed', 'stripe', '2026-01-28 13:06:54'),
(5, 4, 'ORD-20260128131127-R', 20.00, 'completed', 'stripe', '2026-01-28 13:11:27'),
(6, 4, 'ORD-20260128131444-Z', 90.98, 'pending', 'stripe', '2026-01-28 13:14:44'),
(7, 4, 'ORD-20260128132443-0', 13.00, 'completed', 'stripe', '2026-01-28 13:24:43'),
(8, 5, 'ORD-20260128233105-Z', 55.00, 'completed', 'stripe', '2026-01-28 23:31:05');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `book_id`, `price`) VALUES
(1, 1, 1, 49.99),
(2, 2, 10, 13.00),
(3, 3, 14, 25.00),
(4, 4, 15, 12.00),
(5, 5, 11, 20.00),
(6, 6, 5, 42.99),
(7, 6, 8, 47.99),
(8, 7, 10, 13.00),
(9, 8, 13, 30.00),
(10, 8, 14, 25.00);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `comment` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `user_id`, `book_id`, `rating`, `comment`, `created_at`) VALUES
(1, 2, 10, 3, 'This book is a thoughtful discussion of a text\'s contents, strengths, and limitations.', '2026-01-28 09:36:46'),
(2, 4, 10, 5, 'I think this book would help other children to learn that trying new things can be scary, but sometimes when we try, we can find things that make us happy too. And this book will help others know that mistakes are okay and part of learning.', '2026-01-28 22:03:48'),
(3, 4, 15, 5, 'I liked this book. People who are interested in national disasters and US history as well as immigration will most probably be interested in reading this book.', '2026-01-28 22:04:20'),
(4, 4, 14, 4, 'Have you ever wondered if the neighborhood cat is spying on you? Read about Operation Acoustic Kitty and find out if this feline fantasy fiction or fact. ', '2026-01-28 22:35:57'),
(5, 5, 13, 5, ' would highly recommend this book to anyone who desires a guide to the future of biological science and technology. Frankenstein\'s Cat is best read by the light of a glow-in-the-dark fish, while cuddling your favorite cloned dog and drinking a glass of genetically modified milk.', '2026-01-28 23:32:36'),
(6, 5, 14, 4, 'What about a zombified cyborg beetle? Is Fido so special that you want two of him? Money can buy you an almost exact copy of your pooch BUT don\'t expect the same personality. Emily Anthes makes you crave more information. She makes you want to know the future of Earth\'s flora and fauna, as well as humanity itself.', '2026-01-28 23:33:09'),
(7, 2, 1, 4, 'The glossary of facts in the back of About Marsupials is the most useful part. I thought the most interesting parts were that some marsupials have their pouch at their back legs and one marsupial, the Yellow-footed Rock Wallaby, is very small but can jump 13 feet wide!', '2026-01-29 00:11:06');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(120) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `last_login` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `full_name`, `is_admin`, `created_at`, `last_login`) VALUES
(1, 'admin', 'admin@cyberbooks.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LV7W8Oy5C', 'Administrator', 1, '2026-01-20 07:32:11', NULL),
(2, 'admin123', 'adminuser123@gmail.com', '$2b$12$LwEomGi2tcsM42BUeTqFEuPka0q9wsq6RfgUrDYUADfjDy0s6yquW', 'Admin Kyaw Kyaw', 1, '2026-01-20 07:37:16', '2026-01-29 05:10:53'),
(3, 'kyawkyaw', 'kyawkyaw@gmail.com', '$2b$12$/U6pQdKv7f6k8qH7ID6n7OygHi1wA0VayrcMUsPvrKio2jxd5NdTK', 'Kyaw Kyaw', 0, '2026-01-21 04:45:16', '2026-01-21 04:45:32'),
(4, 'John007', 'johnsmith222@gmail.com', '$2b$12$Bo8KDkT3VT8gk141BETRG.Cph5f5hpEX4jfj3Pj0dOL5b5U2hDQ8C', 'John Smith', 0, '2026-01-28 12:03:40', '2026-01-28 21:34:07'),
(5, 'willam007', 'willam007@gamil.com', '$2b$12$wQD2Z5wvZ2nEFqRzP48HWeqtoKMtYrwBOE.mCQXT82WiELTXbZkMW', 'Willam Mikk', 0, '2026-01-28 23:00:44', '2026-01-28 23:05:23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `isbn` (`isbn`),
  ADD KEY `idx_title` (`title`),
  ADD KEY `idx_category` (`category_id`);

--
-- Indexes for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_book_cart` (`user_id`,`book_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_book_id` (`book_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `idx_order_number` (`order_number`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_order_id` (`order_id`),
  ADD KEY `idx_book_id` (`book_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_book_review` (`user_id`,`book_id`),
  ADD KEY `idx_book_id` (`book_id`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `cart_items`
--
ALTER TABLE `cart_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
