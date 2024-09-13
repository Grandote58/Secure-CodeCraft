import sqlite3

# Conectar o crear la base de datos "COMPRAS"
conn = sqlite3.connect('compras.db')
cursor = conn.cursor()

# Crear la tabla de clientes (customers)
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
)''')

# Crear la tabla de productos (products)
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL
)''')

# Crear la tabla de órdenes (orders)
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)''')

# Crear la tabla de ítems de órdenes (order_items)
cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)''')

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("Base de datos y tablas creadas correctamente.")