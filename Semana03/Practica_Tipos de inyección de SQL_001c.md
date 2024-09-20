# **Tipos de inyección de SQL**

## Inyección de SQL mediante la modificación de cookies.

Las cookies pueden ser manipuladas por un atacante para enviar datos maliciosos al servidor, con el objetivo de realizar consultas SQL no autorizadas. Este ejercicio te permitirá entender cómo los datos almacenados en cookies pueden ser un vector para inyecciones SQL si no se gestionan correctamente.

### **Objetivo:**

Desarrollar una aplicación que simule una vulnerabilidad donde las cookies del usuario pueden ser manipuladas para ejecutar una inyección SQL y extraer datos no autorizados. Los estudiantes aprenderán cómo prevenir este tipo de ataques validando correctamente los datos provenientes de cookies.

### **Requisitos:**

1. **Python 3.x** instalado.
2. **CustomTkinter** instalado (`pip install customtkinter`).
3. **SQLite3** (incluido con Python).
4. Entender los conceptos básicos de cookies y cómo los servidores web las utilizan para gestionar sesiones.

### **Paso 1: Crear una Base de Datos Simulada**

Primero, creamos una base de datos SQLite con una tabla de usuarios que simulará la autenticación basada en cookies.

```python
import sqlite3

# Crear la conexión a la base de datos
conn = sqlite3.connect('usuarios_cookies.db')
cursor = conn.cursor()

# Crear una tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    user_role TEXT)''')

# Insertar algunos usuarios
cursor.execute("INSERT INTO users (username, password, user_role) VALUES ('admin', 'admin123', 'admin')")
cursor.execute("INSERT INTO users (username, password, user_role) VALUES ('usuario1', 'pass123', 'usuario')")
cursor.execute("INSERT INTO users (username, password, user_role) VALUES ('usuario2', 'micontraseña', 'usuario')")

conn.commit()
conn.close()
```

### **Paso 2: Crear la Interfaz Gráfica con CustomTkinter**

Ahora, crearemos una aplicación con CustomTkinter que simulará la autenticación basada en cookies. Aquí, los estudiantes podrán modificar la cookie manualmente para intentar explotar la vulnerabilidad de inyección SQL.

```python
import customtkinter as ctk
import sqlite3

# Función que simula la lectura de una cookie y la inyección SQL
def login_with_cookie(cookie):
    conn = sqlite3.connect('usuarios_cookies.db')
    cursor = conn.cursor()

    try:
        # Consulta vulnerable a inyección SQL a través de cookies
        query = f"SELECT username, user_role FROM users WHERE id = '{cookie}'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            label_resultado.config(text=f"Usuario: {result[0][0]}, Rol: {result[0][1]}")
        else:
            label_resultado.config(text="Cookie no válida o usuario no encontrado")
        
        # Simular el caso donde el atacante modifica la cookie
        if "' OR '1'='1" in cookie:
            label_resultado.config(text="Inyección SQL detectada: Se ha recuperado toda la información de los usuarios")
    except sqlite3.Error as e:
        # Mostrar el error SQL
        label_resultado.config(text=f"Error SQL: {str(e)}")

    conn.close()

# Configuración de la ventana principal
root = ctk.CTk()
root.geometry("400x300")
root.title("Simulación de Inyección SQL mediante Cookies")

# Etiquetas y entradas para la cookie
ctk.CTkLabel(root, text="Prueba de Inyección SQL mediante Modificación de Cookies").pack(pady=10)
entry_cookie = ctk.CTkEntry(root, placeholder_text="ID de cookie (usuario)")
entry_cookie.pack(pady=5)

# Botón para simular login con la cookie
ctk.CTkButton(root, text="Login con Cookie", 
              command=lambda: login_with_cookie(entry_cookie.get())).pack(pady=10)

# Etiqueta para mostrar los resultados
label_resultado = ctk.CTkLabel(root, text="")
label_resultado.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
```

### **Documentación del Código:**

1. **Base de Datos y Tabla:**
   - Se crea una base de datos SQLite llamada `usuarios_cookies.db` con una tabla `users` que contiene los campos `id`, `username`, `password`, y `user_role`.
   - Se insertan usuarios con diferentes roles para simular un entorno con niveles de permisos.
2. **Simulación de la Modificación de Cookies:**
   - En la función `login_with_cookie`, se simula la lectura de una cookie que contiene el ID del usuario. Esta cookie es usada en la consulta SQL.
   - Si el atacante modifica la cookie e introduce una carga maliciosa como `' OR '1'='1`, esto permite obtener toda la información de los usuarios.
   - El resultado de la consulta se muestra en la interfaz gráfica.
3. **Interfaz Gráfica con CustomTkinter:**
   - Creamos una interfaz gráfica con un campo para ingresar una cookie (el ID de usuario).
   - Un botón permite al usuario simular un login basado en cookies, que puede incluir cargas maliciosas.
   - Los resultados se muestran en la etiqueta, incluyendo si la inyección SQL ha sido exitosa.

### **Paso 3: Prueba de la Inyección SQL mediante Cookies**

1. Ejecuta la aplicación.

2. Ingresa un valor válido para la cookie, como `1` o `2`. Esto debería devolver el nombre del usuario y su rol.

3. Simula la inyección SQL modificando la cookie de esta manera:

   ```bash
   ' OR '1'='1
   ```

   Esto explotará la vulnerabilidad y mostrará un mensaje indicando que todos los usuarios han sido expuestos debido a la inyección SQL.

### **Prevención:**

Para evitar este tipo de ataques, es esencial validar y sanear correctamente los datos que provienen de las cookies. Utiliza **consultas parametrizadas** para evitar que las entradas del usuario sean ejecutadas como código SQL:

```python
def login_seguro(cookie):
    conn = sqlite3.connect('usuarios_cookies.db')
    cursor = conn.cursor()

    # Consulta segura utilizando parámetros
    query = "SELECT username, user_role FROM users WHERE id = ?"
    cursor.execute(query, (cookie,))
    result = cursor.fetchall()

    if result:
        label_resultado.config(text=f"Usuario: {result[0][0]}, Rol: {result[0][1]}")
    else:
        label_resultado.config(text="Cookie no válida o usuario no encontrado")

    conn.close()
```







