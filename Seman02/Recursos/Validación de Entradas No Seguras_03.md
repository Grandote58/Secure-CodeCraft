# **Validación de Entradas No Seguras 003**

### **Verificar la Estructura del Proyecto**

Asegúrate de que tu estructura del proyecto sea como esta:

```css
/tu_proyecto
├── /templates
│   └── index.html
├── app.py
└── compras.db
```

- **`index.html`** debe estar dentro de la carpeta `templates`.
- **`app.py`** debe estar en el mismo nivel que la carpeta `templates`.

### Pasos a seguir:

1. **Crear el Backend con Flask**: Flask permitirá manejar las operaciones de la base de datos (Create, Read, Update, Delete) y la conexión con **"compras.db"**.
2. **Conectar el Frontend (HTML/JavaScript) al Backend (Flask)**: El frontend enviará solicitudes HTTP (AJAX) al backend para realizar las operaciones en la base de datos.

### **1. Código del Backend con Flask**

Primero, vamos a crear el backend en **Python** utilizando **Flask** para manejar las operaciones CRUD con la base de datos `compras.db`:

```bash
pip install Flask
```

Crea un archivo llamado `app.py` con el siguiente código:

```python
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Función para conectarse a la base de datos
def get_db_connection():
    conn = sqlite3.connect('compras.db')
    conn.row_factory = sqlite3.Row  # Retorna las filas como diccionarios
    return conn


# Ruta para servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza el archivo HTML



# Ruta para obtener todos los clientes
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        conn = get_db_connection()
        customers = conn.execute('SELECT * FROM customers').fetchall()
        conn.close()

        if not customers:
            return jsonify({"message": "No se encontraron clientes"}), 404

        return jsonify([dict(customer) for customer in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener un cliente por ID
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        conn = get_db_connection()
        customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()
        conn.close()

        if customer is None:
            return jsonify({"message": "Cliente no encontrado"}), 404

        return jsonify(dict(customer)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para agregar un cliente
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.get_json()

        # Validación de los datos
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')

        if not nombre or not email:
            return jsonify({"error": "Nombre y email son obligatorios"}), 400

        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
                (nombre, email, telefono)
            )
            conn.commit()

        return jsonify({"message": "Cliente agregado correctamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un cliente
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        data = request.get_json()

        # Validación de los datos
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')

        if not nombre or not email:
            return jsonify({"error": "Nombre y email son obligatorios"}), 400

        with get_db_connection() as conn:
            result = conn.execute(
                'UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?',
                (nombre, email, telefono, id)
            )
            conn.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Cliente no encontrado"}), 404

        return jsonify({"message": "Cliente actualizado correctamente"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un cliente
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        with get_db_connection() as conn:
            result = conn.execute('DELETE FROM customers WHERE id = ?', (id,))
            conn.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Cliente no encontrado"}), 404

        return jsonify({"message": "Cliente eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

```

### **2. Conectar el Frontend con el Backend**

Ahora actualizaremos el archivo HTML para que se conecte con este backend mediante solicitudes AJAX. Aquí está el código actualizado:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRUD Compras - Validación de Entradas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h2>Gestión de Compras - Clientes</h2>

        <!-- Formulario para agregar/actualizar clientes -->
        <form id="formCliente" novalidate>
            <div class="mb-3">
                <label for="nombre" class="form-label">Nombre</label>
                <input type="text" class="form-control" id="nombre" required>
                <div class="invalid-feedback">El nombre es obligatorio y debe tener al menos 3 caracteres.</div>
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" required>
                <div class="invalid-feedback">Introduce un email válido.</div>
            </div>

            <div class="mb-3">
                <label for="telefono" class="form-label">Teléfono</label>
                <input type="text" class="form-control" id="telefono">
                <div class="invalid-feedback">El teléfono debe tener solo números y al menos 7 caracteres.</div>
            </div>

            <button type="submit" class="btn btn-primary">Guardar Cliente</button>
        </form>

        <!-- Tabla para mostrar los clientes -->
        <h3 class="mt-5">Lista de Clientes</h3>
        <table class="table table-bordered mt-3" id="tablaClientes">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                <!-- Las filas serán generadas dinámicamente -->
            </tbody>
        </table>
    </div>

    <!-- Script para manejar las acciones CRUD y validación de entradas -->
    <script>
        const apiUrl = 'http://127.0.0.1:5000/customers';  // URL correcta del backend Flask
        let currentClienteId = null; // Para saber si estamos creando o editando

        // Cargar clientes iniciales
        document.addEventListener("DOMContentLoaded", () => {
            cargarClientes();
        });

        // Función para cargar los clientes desde el servidor Flask
        function cargarClientes() {
            fetch(apiUrl)
                .then(response => response.json())
                .then(clientes => {
                    renderClientes(clientes);
                })
                .catch(error => {
                    console.error('Error al cargar los clientes:', error);
                });
        }

        // Función para renderizar los clientes en la tabla
        function renderClientes(clientes) {
            let tbody = document.getElementById("tablaClientes").querySelector("tbody");
            tbody.innerHTML = ""; // Limpiar la tabla
            clientes.forEach(cliente => {
                let tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.name}</td>
                    <td>${cliente.email}</td>
                    <td>${cliente.phone}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editarCliente(${cliente.id})">Editar</button>
                        <button class="btn btn-danger btn-sm" onclick="eliminarCliente(${cliente.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Manejar el evento de submit del formulario para agregar o actualizar un cliente
        document.getElementById("formCliente").addEventListener("submit", function(event) {
            event.preventDefault();
            event.stopPropagation();

            let form = this;
            if (form.checkValidity()) {
                const clienteData = {
                    nombre: document.getElementById("nombre").value,
                    email: document.getElementById("email").value,
                    telefono: document.getElementById("telefono").value
                };

                if (currentClienteId === null) {
                    // Crear nuevo cliente
                    fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(clienteData)
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error al agregar cliente');
                        }
                        return response.json();
                    })
                    .then(() => {
                        alert("Cliente agregado correctamente.");
                        cargarClientes();
                    })
                    .catch(error => {
                        console.error('Error al agregar cliente:', error);
                    });
                } else {
                    // Actualizar cliente existente
                    fetch(`${apiUrl}/${currentClienteId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(clienteData)
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error al actualizar cliente');
                        }
                        return response.json();
                    })
                    .then(() => {
                        alert("Cliente actualizado correctamente.");
                        cargarClientes();
                    })
                    .catch(error => {
                        console.error('Error al actualizar cliente:', error);
                    });
                }
                currentClienteId = null; // Restablecer
                form.reset();
            } else {
                alert("Por favor, corrige los errores en el formulario.");
            }
            form.classList.add('was-validated');
        });

        // Función para editar un cliente
        function editarCliente(id) {
            fetch(`${apiUrl}/${id}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al obtener cliente');
                    }
                    return response.json();
                })
                .then(cliente => {
                    document.getElementById("nombre").value = cliente.name;
                    document.getElementById("email").value = cliente.email;
                    document.getElementById("telefono").value = cliente.phone;
                    currentClienteId = cliente.id;
                })
                .catch(error => {
                    console.error('Error al obtener cliente:', error);
                });
        }

        // Función para eliminar un cliente
        function eliminarCliente(id) {
            if (confirm("¿Seguro que deseas eliminar este cliente?")) {
                fetch(`${apiUrl}/${id}`, { method: 'DELETE' })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error al eliminar cliente');
                        }
                        return response.json();
                    })
                    .then(() => {
                        alert("Cliente eliminado correctamente.");
                        cargarClientes();
                    })
                    .catch(error => {
                        console.error('Error al eliminar cliente:', error);
                    });
            }
        }

        // Validaciones adicionales para el teléfono
        document.getElementById("telefono").addEventListener("input", function() {
            if (isNaN(this.value) || this.value.length < 7) {
                this.setCustomValidity("El teléfono debe ser un número válido con al menos 7 caracteres.");
            } else {
                this.setCustomValidity("");
            }
        });
    </script>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>
</body>
</html>

```

------

### **Explicación**:

1. **Backend (Flask)**:
   - Se implementaron rutas para realizar las operaciones **CRUD** en la base de datos SQLite (`compras.db`).
   - Rutas:
     - `GET /clientes`: Devuelve todos los clientes.
     - `POST /clientes`: Agrega un nuevo cliente.
     - `PUT /clientes/<id>`: Actualiza un cliente existente.
     - `DELETE /clientes/<id>`: Elimina un cliente.
2. **Frontend (HTML y JavaScript)**:
   - El frontend ahora realiza solicitudes AJAX al backend utilizando **fetch()** para cargar, agregar, actualizar y eliminar clientes.
   - **Validación**: Se sigue utilizando HTML5 para validar entradas (nombre, email, teléfono).
   - **Renderizado Dinámico**: La tabla de clientes se actualiza dinámicamente al realizar las operaciones CRUD.

------

### **Ejecución**:

1. **Correr el Backend**:

   - Guarda el archivo 

     ```bash
     app.py
     ```

      y ejecuta el servidor Flask:

     ```bash
     python app.py
     ```

### **Cambios y Mejoras en el Código**:

1. **`with` para la conexión de la base de datos**:
   - Uso de `with` asegura que la conexión a la base de datos se cierre automáticamente después de la ejecución, incluso si hay errores.
2. **Manejo de errores**:
   - Cada operación está envuelta en bloques `try-except`, lo que permite capturar errores y devolver respuestas apropiadas, como códigos de error HTTP 400 (datos faltantes) y 500 (errores internos del servidor).
3. **Validación de datos**:
   - Antes de insertar o actualizar un cliente, el código verifica que los campos obligatorios (`nombre`, `email`) estén presentes.
   - En el caso de duplicados de correo electrónico, devuelve un error 409 (conflicto).
4. **Código de respuesta HTTP apropiado**:
   - **200** para respuestas exitosas (GET, PUT, DELETE).
   - **201** para creación exitosa de un recurso (POST).
   - **404** para recursos no encontrados (clientes inexistentes).
   - **400** para errores en las solicitudes (datos faltantes o inválidos).
   - **409** para conflictos (cuando el correo electrónico ya está en uso).
   - **500** para errores en el servidor.
5. **Nuevo endpoint `GET /customers/<id>`**:
   - Se añade un endpoint adicional para obtener un cliente por su ID (`GET /customers/<int:id>`).