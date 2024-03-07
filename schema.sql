CREATE TABLE IF NOT EXISTS menu_items (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  category_id INTEGER NOT NULL,
  price REAL NOT NULL,
  image_url TEXT,
  active INTEGER DEFAULT 1,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS categories (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS ingredients (
  ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  unit_type TEXT NOT NULL,
  unit_price REAL NOT NULL,
  active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS item_ingredients (
  item_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  PRIMARY KEY (item_id, ingredient_id),
  FOREIGN KEY (item_id) REFERENCES menu_items(item_id),
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount REAL NOT NULL,
  status TEXT DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS order_items (
  order_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  PRIMARY KEY (order_id, item_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

CREATE TABLE IF NOT EXISTS inventory (
  ingredient_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  reorder_point REAL NOT NULL,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  role TEXT DEFAULT 'cashier'
);
-- INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin');

CREATE TABLE IF NOT EXISTS flags (
  flag_name TEXT PRIMARY KEY,
  stat TEXT NOT NULL
);
INSERT INTO flags (flag_name, stat) VALUES ('first_start', 'true');