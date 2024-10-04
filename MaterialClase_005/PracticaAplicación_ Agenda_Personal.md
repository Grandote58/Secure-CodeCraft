# **Aplicación  Agenda Personal** 

### Usando Python, Flask, SQLite, Bootstrap, y JavaScript

### 1. Diseño de la base de datos

Para la agenda, necesitaremos una tabla que almacene información de contactos como nombre, teléfono, correo electrónico, dirección y otros datos relevantes.

Aquí está el **diseño de la base de datos** con la estructura SQL para **SQLite**:

```sqlite
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Modelo Entidad-Relación (ER)

El diagrama ER de esta base de datos será simple, ya que solo tenemos una tabla sin relaciones con otras entidades. La tabla **contacts** tiene los siguientes atributos:

- **id**: Clave primaria.
- **name**: Nombre del contacto.
- **phone**: Teléfono del contacto.
- **email**: Correo electrónico.
- **address**: Dirección física del contacto.
- **created_at**: Fecha de creación del registro.

No se requieren claves foráneas en este caso, ya que es una agenda personal básica.

#### Modelo ER simple:

- Tabla Contacts:
  - Clave primaria: `id`
  - Atributos: `name`, `phone`, `email`, `address`, `created_at`.

### 3. Datos de prueba

Puedes generar datos de prueba manualmente o crear un procedimiento en Python para insertar automáticamente 20 contactos. A continuación, te dejo un código Python para insertar datos aleatorios:

```python
import sqlite3
import random

# Conexión a la base de datos
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Nombres y direcciones de ejemplo
names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Clark"]
addresses = ["123 Elm St", "456 Oak St", "789 Pine St", "101 Maple Ave", "202 Birch Blvd"]

# Insertar 20 registros aleatorios
for _ in range(20):
    name = random.choice(names)
    phone = f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    email = f"{name.split()[0].lower()}@example.com"
    address = random.choice(addresses)
    
    cursor.execute('''
        INSERT INTO contacts (name, phone, email, address)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, email, address))

conn.commit()
conn.close()
```

Este código generará aleatoriamente 20 contactos de ejemplo con nombres, teléfonos, emails y direcciones para poblar la base de datos.

### 4. Página de inicio

La página de inicio de la aplicación será la lista de contactos actuales. Usaremos **Bootstrap** para hacerla más atractiva y funcional, con opciones de agregar, editar y eliminar contactos.

#### HTML (página de inicio con Flask y Bootstrap):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agenda Personal</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Agenda Personal</h1>
        <a href="/add" class="btn btn-success mb-3">Agregar Contacto</a>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Teléfono</th>
                    <th>Email</th>
                    <th>Dirección</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for contact in contacts %}
                <tr>
                    <td>{{ contact.name }}</td>
                    <td>{{ contact.phone }}</td>
                    <td>{{ contact.email }}</td>
                    <td>{{ contact.address }}</td>
                    <td>
                        <a href="/edit/{{ contact.id }}" class="btn btn-warning btn-sm">Editar</a>
                        <a href="/delete/{{ contact.id }}" class="btn btn-danger btn-sm">Eliminar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
```

### 5. CRUD Completo

Implementaremos las funcionalidades **CRUD** (Crear, Leer, Actualizar, Eliminar) utilizando **Flask**. Aquí está el código principal para manejar estas operaciones:

#### `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página de inicio - Leer (Read)
@app.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

# Crear contacto (Create)
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn = get_db_connection()
        conn.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)',
                     (name, phone, email, address))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Editar contacto (Update)
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn.execute('UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?',
                     (name, phone, email, address, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', contact=contact)

# Eliminar contacto (Delete)
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

### 6. Documentación del código

El código está comentado para explicar cada parte clave de la aplicación. Los puntos importantes incluyen:

- **`get_db_connection()`**: Función para conectar a la base de datos SQLite.
- **`index()`**: Función para listar todos los contactos en la página principal.
- **`add()`**: Función para agregar un nuevo contacto.
- **`edit()`**: Función para editar un contacto existente.
- **`delete()`**: Función para eliminar un contacto de la agenda.