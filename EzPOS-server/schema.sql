CREATE TABLE menu_items (
  item_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category_id INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  image_url VARCHAR(255),
  active TINYINT(1) DEFAULT 1,
  CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  active TINYINT(1) DEFAULT 1
);

CREATE TABLE ingredients (
  ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  unit_type VARCHAR(255) NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  active TINYINT(1) DEFAULT 1
);

CREATE TABLE item_ingredients (
  item_id INT NOT NULL,
  ingredient_id INT NOT NULL,
  quantity DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (item_id, ingredient_id),
  CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES menu_items(item_id),
  CONSTRAINT fk_ingredient FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(10,2) NOT NULL,
  status ENUM('pending', 'processing', 'completed', 'cancelled') DEFAULT 'pending'
);

CREATE TABLE order_items (
  order_id INT NOT NULL,
  item_id INT NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (order_id, item_id),
  CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
  CONSTRAINT fk_item_again FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

CREATE TABLE inventory (
  ingredient_id INT NOT NULL,
  quantity DECIMAL(10,2) NOT NULL,
  reorder_point DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_ingredient_inventory FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role ENUM('admin', 'cashier', 'manager') DEFAULT 'cashier'
);