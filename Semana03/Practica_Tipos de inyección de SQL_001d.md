# **Tipos de inyección de SQL**

## Técnica de inyección SQL a través de variables de servidor. 

Las variables de servidor, como las cabeceras HTTP o direcciones IP, pueden ser manipuladas por un atacante para intentar inyectar código malicioso en una aplicación.

### **Objetivo:**

Desarrollar una aplicación que permita simular una inyección de SQL mediante variables de servidor, como la dirección IP del cliente. Esto ayudará a los estudiantes a entender cómo estos valores pueden ser manipulados y cómo prevenir este tipo de vulnerabilidades.

### **Requisitos:**

1. **Python 3.x** instalado.
2. **CustomTkinter** instalado (`pip install customtkinter`).
3. **SQLite3** (incluido con Python).

### **Paso 1: Crear una Base de Datos Simulada**

Comenzamos creando la base de datos en SQLite con una tabla de usuarios que almacenará el nombre de usuario y el rol asociado a cada cuenta.

```python
import sqlite3

# Crear la conexión a la base de datos
conn = sqlite3.connect('usuarios_servidor.db')
cursor = conn.cursor()

# Crear una tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    user_role TEXT,
                    ip_address TEXT)''')

# Insertar algunos usuarios con una dirección IP simulada
cursor.execute("INSERT INTO users (username, password, user_role, ip_address) VALUES ('admin', 'admin123', 'admin', '192.168.0.1')")
cursor.execute("INSERT INTO users (username, password, user_role, ip_address) VALUES ('usuario1', 'pass123', 'usuario', '192.168.0.2')")
cursor.execute("INSERT INTO users (username, password, user_role, ip_address) VALUES ('usuario2', 'micontraseña', 'usuario', '192.168.0.3')")

conn.commit()
conn.close()
```

### **Paso 2: Crear la Interfaz Gráfica con CustomTkinter**

Ahora creamos la interfaz gráfica usando **CustomTkinter**. Simulamos una consulta basada en la dirección IP del usuario, que podría ser manipulada por un atacante.

```php
import customtkinter as ctk
import sqlite3

# Función que simula la inyección SQL mediante variables de servidor (IP en este caso)
def login_by_ip(ip_address):
    conn = sqlite3.connect('usuarios_servidor.db')
    cursor = conn.cursor()

    try:
        # Consulta vulnerable a inyección SQL utilizando la IP
        query = f"SELECT username, user_role FROM users WHERE ip_address = '{ip_address}'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            label_resultado.config(text=f"Usuario: {result[0][0]}, Rol: {result[0][1]}")
        else:
            label_resultado.config(text="IP no válida o usuario no encontrado")

        # Simulación de inyección SQL: Si la IP contiene un intento de inyección
        if "' OR '1'='1" in ip_address:
            label_resultado.config(text="Inyección SQL detectada: Todos los usuarios expuestos")
    except sqlite3.Error as e:
        # Mostrar el error SQL
        label_resultado.config(text=f"Error SQL: {str(e)}")

    conn.close()

# Configuración de la ventana principal
root = ctk.CTk()
root.geometry("400x300")
root.title("Simulación de Inyección SQL mediante Variables de Servidor")

# Etiquetas y entrada para la IP
ctk.CTkLabel(root, text="Prueba de Inyección SQL mediante la Dirección IP").pack(pady=10)
entry_ip_address = ctk.CTkEntry(root, placeholder_text="Dirección IP (servidor)")
entry_ip_address.pack(pady=5)

# Botón para simular el login por dirección IP
ctk.CTkButton(root, text="Login por IP", 
              command=lambda: login_by_ip(entry_ip_address.get())).pack(pady=10)

# Etiqueta para mostrar los resultados
label_resultado = ctk.CTkLabel(root, text="")
label_resultado.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
```

### **Documentación del Código:**

1. **Base de Datos y Tabla:**
   - Creamos una base de datos SQLite llamada `usuarios_servidor.db` con una tabla `users` que contiene `id`, `username`, `password`, `user_role`, y `ip_address`.
   - Se añaden varios usuarios con sus direcciones IP simuladas para representar cómo una aplicación podría almacenar esta información.
2. **Simulación de Inyección SQL mediante Variables de Servidor:**
   - La función `login_by_ip` realiza una consulta SQL vulnerable utilizando la dirección IP del usuario, que simula una variable de servidor.
   - Si la IP contiene una carga maliciosa como `"' OR '1'='1"`, la consulta SQL se ejecuta y expone toda la información de los usuarios.
3. **Interfaz Gráfica con CustomTkinter:**
   - Creamos una interfaz gráfica donde el usuario puede ingresar una dirección IP.
   - Un botón permite ejecutar la consulta simulada con la IP, mostrando los resultados en la interfaz gráfica.

### **Paso 3: Prueba de la Inyección SQL mediante Variables de Servidor**

1. Ejecuta la aplicación.

2. Ingresa una dirección IP válida, como `192.168.0.1` o `192.168.0.2`. Esto debería devolver el nombre de usuario y su rol.

3. Simula una inyección SQL modificando la IP de esta manera:

   ```bash
   ' OR '1'='1
   ```

   Esto explotará la vulnerabilidad y mostrará un mensaje indicando que todos los usuarios han sido expuestos debido a la inyección SQL.

### **Prevención:**

Para prevenir este tipo de ataque, debemos validar y sanear correctamente las variables de servidor. Utiliza **consultas parametrizadas** para evitar que las entradas sean tratadas como código SQL:

```python
def login_seguro_by_ip(ip_address):
    conn = sqlite3.connect('usuarios_servidor.db')
    cursor = conn.cursor()

    # Consulta segura utilizando parámetros
    query = "SELECT username, user_role FROM users WHERE ip_address = ?"
    cursor.execute(query, (ip_address,))
    result = cursor.fetchall()

    if result:
        label_resultado.config(text=f"Usuario: {result[0][0]}, Rol: {result[0][1]}")
    else:
        label_resultado.config(text="IP no válida o usuario no encontrado")

    conn.close()
```

### **Conclusión:**

Esta práctica ayuda a los estudiantes a comprender cómo las variables de servidor, como la dirección IP, pueden ser utilizadas para realizar inyecciones SQL si no se validan correctamente. Además, se muestra cómo prevenir estos ataques mediante el uso de consultas parametrizadas y una correcta validación de las entradas.