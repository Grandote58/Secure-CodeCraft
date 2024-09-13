# **Validación de Entradas No Seguras 001**

La validación de entradas es uno de los aspectos clave para prevenir ataques como **Inyección SQL**, **Cross-Site Scripting (XSS)**, y **Cross-Site Request Forgery (CSRF)**.

Práctica detallada y documentada sobre cómo crear la base de datos **"COMPRAS"** en SQLite utilizando Python y CustomTkinter, junto con un CRUD (Create, Read, Update, Delete) para gestionar las tablas. También se cubre la validación de entradas para prevenir ataques como inyecciones SQL y otros.

## **Proceso de Instalación**

### 1. **Instalar las Dependencias**:

- Instala 

  CustomTkinter:

  ```bash
  pip install customtkinter
  ```

- Instala 

  Requests para la simulación de ataques CSRF:

  ```bash
  pip install requests
  ```

  

### 2.  Crear la Base de Datos

Vamos a crear la base de datos **COMPRAS** con las tablas **customers**, **products**, **orders**, y **order_items**. El siguiente código crea la base de datos y las tablas:

```python
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
```

### 3.  Crear CRUD con Python y CustomTkinter

```python
import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
import re

# Función para validar los campos de entrada
def validar_cliente(nombre, email):
    if not nombre or not email:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return False

    patron_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(patron_email, email):
        messagebox.showerror("Error", "Correo electrónico no es válido.")
        return False

    return True

# Función para gestionar la conexión a la base de datos
def ejecutar_query(query, params=()):
    try:
        conn = sqlite3.connect('compras.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")
        return None
    finally:
        conn.close()

# Función para agregar un cliente
def agregar_cliente():
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    telefono = entry_telefono.get().strip()

    if validar_cliente(nombre, email):
        query = "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)"
        params = (nombre, email, telefono)
        resultado = ejecutar_query(query, params)
        
        if resultado is not None:
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            actualizar_vista_clientes()
        else:
            messagebox.showerror("Error", "El correo electrónico ya está en uso")

# Función para actualizar un cliente
def actualizar_cliente():
    seleccionado = tabla_clientes.focus()
    if seleccionado == "":
        messagebox.showwarning("Advertencia", "Selecciona un cliente en la tabla para actualizar")
        return
    
    cliente = tabla_clientes.item(seleccionado, 'values')
    id_cliente = cliente[0]
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    telefono = entry_telefono.get().strip()

    if validar_cliente(nombre, email) and id_cliente:
        query = "UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?"
        params = (nombre, email, telefono, id_cliente)
        ejecutar_query(query, params)
        messagebox.showinfo("Éxito", f"Cliente {id_cliente} actualizado")
        actualizar_vista_clientes()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

# Función para eliminar un cliente
def eliminar_cliente():
    seleccionado = tabla_clientes.focus()
    if seleccionado == "":
        messagebox.showwarning("Advertencia", "Selecciona un cliente en la tabla para eliminar")
        return
    
    cliente = tabla_clientes.item(seleccionado, 'values')
    id_cliente = cliente[0]
    
    if id_cliente:
        query = "DELETE FROM customers WHERE id = ?"
        ejecutar_query(query, (id_cliente,))
        messagebox.showinfo("Éxito", f"Cliente {id_cliente} eliminado")
        actualizar_vista_clientes()
    else:
        messagebox.showerror("Error", "ID de cliente es obligatorio")

# Función para buscar clientes por nombre o email
def buscar_cliente():
    criterio = entry_busqueda.get().strip()
    if criterio:
        query = "SELECT * FROM customers WHERE name LIKE ? OR email LIKE ?"
        params = (f"%{criterio}%", f"%{criterio}%")
        clientes = ejecutar_query(query, params)
        
        actualizar_tabla(clientes)
    else:
        messagebox.showwarning("Advertencia", "Introduce un criterio de búsqueda")

# Función para visualizar clientes en la tabla
def actualizar_vista_clientes():
    query = "SELECT * FROM customers"
    clientes = ejecutar_query(query)
    actualizar_tabla(clientes)

# Función para actualizar la tabla con datos
def actualizar_tabla(clientes):
    # Limpiar tabla antes de agregar nuevos datos
    tabla_clientes.delete(*tabla_clientes.get_children())
    
    if clientes:
        for cliente in clientes:
            tabla_clientes.insert('', 'end', values=(cliente[0], cliente[1], cliente[2], cliente[3]))

# Función para cargar el cliente seleccionado en los campos
def cargar_cliente():
    seleccionado = tabla_clientes.focus()
    if seleccionado == "":
        messagebox.showwarning("Advertencia", "Selecciona un cliente en la tabla para cargar")
        return
    
    cliente = tabla_clientes.item(seleccionado, 'values')
    
    entry_nombre.delete(0, ctk.END)
    entry_nombre.insert(0, cliente[1])
    
    entry_email.delete(0, ctk.END)
    entry_email.insert(0, cliente[2])
    
    entry_telefono.delete(0, ctk.END)
    entry_telefono.insert(0, cliente[3])

# Interfaz gráfica con CustomTkinter
def inicializar_interfaz():
    root = ctk.CTk()

    # Configuración de la ventana
    root.title("Gestión de Clientes")
    root.geometry("800x600")

    # Crear Frame para el formulario
    frame_formulario = ctk.CTkFrame(root)
    frame_formulario.pack(side="top", fill="x", padx=20, pady=10)

    # Sección para agregar cliente
    ctk.CTkLabel(frame_formulario, text="Formulario de Cliente").grid(row=0, column=0, columnspan=2, pady=10)

    global entry_nombre, entry_email, entry_telefono
    ctk.CTkLabel(frame_formulario, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
    entry_nombre = ctk.CTkEntry(frame_formulario)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_formulario, text="Email").grid(row=2, column=0, padx=10, pady=5)
    entry_email = ctk.CTkEntry(frame_formulario)
    entry_email.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_formulario, text="Teléfono").grid(row=3, column=0, padx=10, pady=5)
    entry_telefono = ctk.CTkEntry(frame_formulario)
    entry_telefono.grid(row=3, column=1, padx=10, pady=5)

    # Botón para agregar cliente
    btn_agregar = ctk.CTkButton(frame_formulario, text="Agregar Cliente", command=agregar_cliente)
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=10)

    # Botones de actualizar, eliminar y cargar cliente
    btn_cargar = ctk.CTkButton(frame_formulario, text="Cargar Cliente", command=cargar_cliente)
    btn_cargar.grid(row=5, column=0, padx=10, pady=10)

    btn_actualizar = ctk.CTkButton(frame_formulario, text="Actualizar Cliente", command=actualizar_cliente)
    btn_actualizar.grid(row=5, column=1, padx=10, pady=10)

    btn_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Cliente", command=eliminar_cliente)
    btn_eliminar.grid(row=6, column=0, columnspan=2, pady=10)

    # Frame para la tabla de clientes
    frame_tabla = ctk.CTkFrame(root)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    # Crear tabla con Treeview
    global tabla_clientes
    columnas = ('ID', 'Nombre', 'Email', 'Teléfono')
    tabla_clientes = ttk.Treeview(frame_tabla, columns=columnas, show='headings')
    
    # Definir encabezados
    for col in columnas:
        tabla_clientes.heading(col, text=col)

    tabla_clientes.pack(fill="both", expand=True, padx=10, pady=10)

    # Sección para buscar clientes
    frame_busqueda = ctk.CTkFrame(root)
    frame_busqueda.pack(side="bottom", fill="x", padx=20, pady=10)

    global entry_busqueda
    ctk.CTkLabel(frame_busqueda, text="Buscar Cliente").grid(row=0, column=0, padx=10, pady=5)
    entry_busqueda = ctk.CTkEntry(frame_busqueda)
    entry_busqueda.grid(row=0, column=1, padx=10, pady=5)

    btn_buscar = ctk.CTkButton(frame_busqueda, text="Buscar", command=buscar_cliente)
    btn_buscar.grid(row=0, column=2, padx=10, pady=5)

    # Inicializar la vista de clientes
    actualizar_vista_clientes()

    root.mainloop()

# Inicializar la interfaz
inicializar_interfaz()

```



## Código para Simular Ataques de Inyección SQL

### Descripción del Ataque:

La inyección SQL permite a los atacantes manipular consultas SQL enviando entradas maliciosas a través de formularios que no validan correctamente las entradas. Esto permite al atacante realizar acciones no autorizadas en la base de datos.

### Código de la Aplicación para **Inyección SQL**:

```python
import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Función para realizar el ataque de inyección SQL
def atacar_sql_inyeccion():
    conn = sqlite3.connect('compras.db')
    cursor = conn.cursor()

    # Capturar la entrada maliciosa
    entrada_maliciosa = entry_maliciosa.get()

    try:
        # Consulta vulnerable (simulación del ataque de inyección SQL)
        query = f"SELECT * FROM customers WHERE name = '{entrada_maliciosa}'"
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Mostrar resultados
        cuadro_resultado.delete(1.0, ctk.END)
        if resultados:
            for row in resultados:
                cuadro_resultado.insert(ctk.END, f"ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Teléfono: {row[3]}\n")
        else:
            cuadro_resultado.insert(ctk.END, "No se encontraron resultados")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")
    finally:
        conn.close()

# Interfaz gráfica para ataque de Inyección SQL
def inicializar_interfaz_sql_inyeccion():
    root = ctk.CTk()
    root.title("Ataque de Inyección SQL")
    root.geometry("500x400")

    ctk.CTkLabel(root, text="Simulación de Ataque de Inyección SQL").pack(pady=10)

    global entry_maliciosa, cuadro_resultado

    # Campo para la entrada maliciosa
    ctk.CTkLabel(root, text="Introduce la entrada maliciosa").pack(pady=5)
    entry_maliciosa = ctk.CTkEntry(root, width=400)
    entry_maliciosa.pack(pady=5)

    # Botón para ejecutar el ataque
    ctk.CTkButton(root, text="Lanzar Ataque SQL", command=atacar_sql_inyeccion).pack(pady=10)

    # Cuadro de texto para mostrar resultados del ataque
    cuadro_resultado = ctk.CTkTextbox(root, width=400, height=200)
    cuadro_resultado.pack(pady=10)

    root.mainloop()

inicializar_interfaz_sql_inyeccion()
```

------

## **Código para Simular Ataques de Cross-Site Request Forgery (CSRF)**

### Descripción del Ataque:

CSRF es un ataque que fuerza a un usuario autenticado a realizar acciones no deseadas en una aplicación sin su consentimiento. En este ejemplo, simularemos un ataque CSRF enviando una solicitud maliciosa.

### Código de la Aplicación para **CSRF**:

```python
import customtkinter as ctk
import requests
from tkinter import messagebox

# Función para realizar el ataque CSRF
def atacar_csrf():
    url_vulnerable = entry_url.get()
    id_cliente = entry_id_cliente.get()
    
    # Payload malicioso simulado
    payload = {'id': id_cliente}
    
    try:
        # Simular la solicitud CSRF sin token de validación
        response = requests.post(url_vulnerable, data=payload)
        cuadro_resultado.delete(1.0, ctk.END)
        if response.status_code == 200:
            cuadro_resultado.insert(ctk.END, f"Ataque CSRF realizado con éxito. Respuesta:\n{response.text}")
        else:
            cuadro_resultado.insert(ctk.END, f"Error en la solicitud: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al realizar el ataque: {e}")

# Interfaz gráfica para ataque CSRF
def inicializar_interfaz_csrf():
    root = ctk.CTk()
    root.title("Simulación de Ataque CSRF")
    root.geometry("500x400")

    ctk.CTkLabel(root, text="Simulación de Ataque CSRF").pack(pady=10)

    global entry_url, entry_id_cliente, cuadro_resultado

    # Entrada para la URL del endpoint vulnerable
    ctk.CTkLabel(root, text="Introduce la URL Vulnerable").pack(pady=5)
    entry_url = ctk.CTkEntry(root, width=400)
    entry_url.pack(pady=5)

    # Entrada para el ID del cliente
    ctk.CTkLabel(root, text="Introduce el ID del cliente").pack(pady=5)
    entry_id_cliente = ctk.CTkEntry(root, width=400)
    entry_id_cliente.pack(pady=5)

    # Botón para ejecutar el ataque
    ctk.CTkButton(root, text="Lanzar Ataque CSRF", command=atacar_csrf).pack(pady=10)

    # Cuadro de texto para mostrar resultados del ataque
    cuadro_resultado = ctk.CTkTextbox(root, width=400, height=200)
    cuadro_resultado.pack(pady=10)

    root.mainloop()

inicializar_interfaz_csrf()
```

------

## Informe de Vulnerabilidades y Fallas

### **Vulnerabilidad de Inyección SQL**:

- **Falla**: En el código de la aplicación vulnerable, no se están utilizando consultas parametrizadas. Las entradas del usuario se concatenan directamente en la consulta SQL, lo que permite que el atacante modifique la consulta.

- **Mitigación**: Usa **consultas parametrizadas** o **sentencias preparadas** en lugar de concatenar las entradas del usuario directamente en las consultas SQL.

  **Mitigación Ejemplo**:

  ```python
  query = "SELECT * FROM customers WHERE name = ?"
  cursor.execute(query, (entrada_maliciosa,))
  ```

### **Vulnerabilidad de CSRF**:

- **Falla**: No hay validación de un token CSRF en la aplicación vulnerable. Esto permite que cualquier usuario autenticado envíe solicitudes en nombre de otro usuario sin su consentimiento.

- **Mitigación**: Implementar un **token CSRF** único por usuario y verificarlo en cada solicitud que involucre acciones críticas.

  **Mitigación Ejemplo**:

  - Generar un token CSRF al cargar el formulario y verificarlo en el servidor antes de procesar la solicitud.

------

## **4. Ejemplos de Entradas Maliciosas para Inyección SQL**

1. **Entrada para Obtener Todos los Registros**:
   - **Entrada maliciosa**: `' OR '1'='1`
   - **Descripción**: Esto fuerza la consulta SQL a devolver todos los registros de la tabla.
2. **Eludir Autenticación**:
   - **Entrada maliciosa**: `' OR 'x'='x`
   - **Descripción**: Esto simula un ataque donde el atacante se autentica sin un usuario válido.
3. **Eliminar una Tabla**:
   - **Entrada maliciosa**: `'; DROP TABLE customers; --`
   - **Descripción**: Esto intenta eliminar la tabla `customers`.
4. **Modificar Datos de la Base de Datos**:
   - **Entrada maliciosa**: `'; UPDATE customers SET email='hacked@example.com'; --`
   - **Descripción**: Modifica el correo de todos los clientes a uno malicioso.
5. **Entrada para Inyectar Comentarios**:
   - **Entrada maliciosa**: `admin' --`
   - **Descripción**: Esto ignora todo lo que sigue en la consulta SQL después del comentario, eludiendo así el sistema de autenticación.
6. **Obtener Información de Todas las Tablas**:
   - **Entrada maliciosa**: `' UNION SELECT name, email, phone FROM customers; --`
   - **Descripción**: Realiza un ataque de unión para obtener información de otra tabla en la base de datos.



## **Correr las Aplicaciones**:

- Ejecuta el archivo Python de inyección SQL para simular el ataque:

  ```python
  python sql_injection_attack.py
  ```

- Ejecuta el archivo Python de CSRF para simular el ataque:

  ```python
  python csrf_attack.py
  ```