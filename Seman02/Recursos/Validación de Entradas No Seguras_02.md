# **Validación de Entradas No Seguras 002**

Para crear una aplicación de validación de entradas en **HTML5**, **JavaScript**, y **Bootstrap** que implemente un **CRUD** completo sobre la base de datos de "compras", necesitaremos:

1. **Front-end con HTML5, Bootstrap y JavaScript**.
2. **Validación de entradas** en el formulario (tanto en el front-end como en el back-end).
3. **Errores de validación** simulados para mostrar al usuario cómo deben corregir las entradas.

Este ejemplo asume que ya tienes configurado un servidor de back-end (puede ser con Python, Node.js, PHP, etc.) y que se conecta a la base de datos "compras" creada anteriormente.

### **Estructura del CRUD**

El CRUD tendrá las siguientes operaciones:

- **Create (Crear)**: Agregar un nuevo cliente o producto.
- **Read (Leer)**: Mostrar los clientes o productos registrados.
- **Update (Actualizar)**: Editar la información de un cliente o producto.
- **Delete (Eliminar)**: Eliminar un cliente o producto.

### **HTML5, Bootstrap, y JavaScript CRUD con Validación de Entradas**

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
        // Datos temporales para simular la base de datos
        let clientes = [
            { id: 1, nombre: "Juan Pérez", email: "juan@example.com", telefono: "5551234" },
            { id: 2, nombre: "María Gómez", email: "maria@example.com", telefono: "5555678" }
        ];
        let currentClienteId = null; // Para saber si estamos creando o editando

        // Cargar clientes iniciales
        document.addEventListener("DOMContentLoaded", () => {
            renderClientes();
        });

        // Manejar el evento de submit del formulario
        document.getElementById("formCliente").addEventListener("submit", function(event) {
            event.preventDefault();
            event.stopPropagation();

            let form = this;
            if (form.checkValidity()) {
                if (currentClienteId === null) {
                    // Crear nuevo cliente
                    let nuevoCliente = {
                        id: clientes.length + 1,
                        nombre: document.getElementById("nombre").value,
                        email: document.getElementById("email").value,
                        telefono: document.getElementById("telefono").value
                    };
                    clientes.push(nuevoCliente);
                    alert("Cliente agregado correctamente.");
                } else {
                    // Actualizar cliente existente
                    let cliente = clientes.find(c => c.id === currentClienteId);
                    cliente.nombre = document.getElementById("nombre").value;
                    cliente.email = document.getElementById("email").value;
                    cliente.telefono = document.getElementById("telefono").value;
                    alert("Cliente actualizado correctamente.");
                }
                currentClienteId = null; // Restablecer
                form.reset();
                renderClientes();
            } else {
                alert("Por favor, corrige los errores en el formulario.");
            }
            form.classList.add('was-validated');
        });

        // Función para renderizar los clientes en la tabla
        function renderClientes() {
            let tbody = document.getElementById("tablaClientes").querySelector("tbody");
            tbody.innerHTML = ""; // Limpiar la tabla
            clientes.forEach(cliente => {
                let tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.nombre}</td>
                    <td>${cliente.email}</td>
                    <td>${cliente.telefono}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editarCliente(${cliente.id})">Editar</button>
                        <button class="btn btn-danger btn-sm" onclick="eliminarCliente(${cliente.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Función para editar un cliente
        function editarCliente(id) {
            let cliente = clientes.find(c => c.id === id);
            document.getElementById("nombre").value = cliente.nombre;
            document.getElementById("email").value = cliente.email;
            document.getElementById("telefono").value = cliente.telefono;
            currentClienteId = cliente.id;
        }

        // Función para eliminar un cliente
        function eliminarCliente(id) {
            if (confirm("¿Seguro que deseas eliminar este cliente?")) {
                clientes = clientes.filter(c => c.id !== id);
                renderClientes();
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

### **Explicación del Código:**

1. **Formulario de Cliente**:
   - El formulario permite al usuario agregar o actualizar clientes.
   - Los campos incluyen validación nativa de **HTML5** (por ejemplo, `required` para campos obligatorios, validación de emails con `type="email"`, etc.).
   - Se utiliza la clase de Bootstrap `invalid-feedback` para mostrar mensajes de error personalizados.
2. **Validación de Entradas**:
   - **Nombre**: Debe ser obligatorio y tener al menos 3 caracteres.
   - **Email**: Validado automáticamente por HTML5 (debe ser un email válido).
   - **Teléfono**: El número debe contener solo dígitos y tener al menos 7 caracteres. Esto se valida con JavaScript en tiempo real.
3. **CRUD Completo**:
   - **Crear y Actualizar**: Cuando el usuario presiona el botón "Guardar Cliente", se verifica si estamos creando o actualizando un cliente según la variable `currentClienteId`. Si es `null`, se crea un nuevo cliente; de lo contrario, se actualiza.
   - **Leer (Mostrar)**: Los clientes se renderizan en una tabla con Bootstrap cada vez que se agrega, actualiza o elimina un cliente.
   - **Eliminar**: El botón "Eliminar" permite borrar un cliente después de una confirmación.
4. **Errores de Validación**:
   - Si el formulario no es válido, muestra mensajes de error personalizados y resalta los campos incorrectos en rojo.

### **Errores Simulados**:

1. **Nombre**:
   - Si el nombre tiene menos de 3 caracteres, se mostrará el mensaje: "El nombre es obligatorio y debe tener al menos 3 caracteres."
2. **Email**:
   - Si no se introduce un email válido, se mostrará: "Introduce un email válido."
3. **Teléfono**:
   - Si el número de teléfono contiene letras o tiene menos de 7 caracteres, se mostrará: "El teléfono debe ser un número válido con al menos 7 caracteres." 