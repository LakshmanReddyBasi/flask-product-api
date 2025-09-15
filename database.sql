r-- database.sql

-- Drop the table if it already exists to start fresh
DROP TABLE IF EXISTS `products`;

-- Create the products table
CREATE TABLE `products` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `price` DECIMAL(10, 2) NOT NULL,
  `category` VARCHAR(100),
  `stock_quantity` INT NOT NULL,
  `manufacturer` VARCHAR(255),
  `release_date` DATE,
  `rating` DECIMAL(3, 2)
);

-- Insert some sample data into the products table
INSERT INTO `products` (name, description, price, category, stock_quantity, manufacturer, release_date, rating)
VALUES
('Wireless Mouse', 'A high-precision wireless optical mouse.', 25.99, 'Electronics', 150, 'Logitech', '2023-05-20', 4.5),
('Mechanical Keyboard', 'A durable mechanical keyboard with RGB backlighting.', 79.99, 'Electronics', 80, 'Corsair', '2023-01-15', 4.8),
('The Alchemist', 'A novel by Paulo Coelho.', 12.50, 'Books', 200, 'HarperCollins', '1988-01-01', 4.7);