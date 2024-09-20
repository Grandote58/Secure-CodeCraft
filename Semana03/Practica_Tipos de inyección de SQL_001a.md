# **Tipos de inyección de SQL**

## **SQL** **en banda**

**SQL basado en errores** y **SQL basado en unión**. La práctica incluye la documentación paso a paso del código, con explicaciones en español.

### **Objetivo:**

Desarrollar una aplicación donde los estudiantes puedan entender y practicar las técnicas de inyección SQL basadas en errores y unión, aprendiendo a prevenir estas vulnerabilidades.

### **Requisitos:**

1. Python 3.x instalado.
2. CustomTkinter instalado (`pip install customtkinter`).
3. SQLite3 (incluido con Python).

### **Paso 1: Crear una Base de Datos Simulada**

Primero, crearemos una base de datos SQLite con una tabla de usuarios que será el objetivo de nuestras pruebas de inyección SQL.

```python
import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT)''')

# Insertar algunos usuarios
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('usuario1', 'pass123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('usuario2', 'micontraseña')")

conn.commit()
conn.close()
```

### **Paso 2: Crear la Interfaz Gráfica con CustomTkinter**

Aquí creamos la interfaz gráfica que permitirá a los usuarios ingresar sus datos y probar las técnicas de inyección SQL.

```python
import customtkinter as ctk
import sqlite3

# Función para simular inyección SQL basada en errores
def login_error_based(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        # Consulta vulnerable a inyección SQL basada en errores
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            label_resultado.config(text="Login exitoso: Usuario encontrado")
        else:
            label_resultado.config(text="Login fallido: Usuario no encontrado")
    except sqlite3.Error as e:
        # Mostrar el error SQL
        label_resultado.config(text=f"Error SQL: {str(e)}")

    conn.close()

# Función para simular inyección SQL basada en unión
def login_union_based(username):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        # Consulta vulnerable a inyección SQL basada en unión
        query = f"SELECT id, username FROM users WHERE username = '{username}' UNION SELECT null, 'datos_expuestos'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            label_resultado.config(text=f"Usuarios expuestos: {result}")
        else:
            label_resultado.config(text="No se encontraron usuarios.")
    except sqlite3.Error as e:
        # Mostrar el error SQL
        label_resultado.config(text=f"Error SQL: {str(e)}")

    conn.close()

# Configuración de la ventana principal
root = ctk.CTk()
root.geometry("400x300")
root.title("Simulación de Inyección SQL")

# Etiquetas y entradas para el login basado en errores
ctk.CTkLabel(root, text="Prueba de Inyección SQL Basada en Errores").pack(pady=10)
entry_username_error = ctk.CTkEntry(root, placeholder_text="Usuario")
entry_username_error.pack(pady=5)
entry_password_error = ctk.CTkEntry(root, placeholder_text="Contraseña", show="*")
entry_password_error.pack(pady=5)

# Botón para realizar login con inyección basada en errores
ctk.CTkButton(root, text="Login Basado en Errores", 
              command=lambda: login_error_based(entry_username_error.get(), entry_password_error.get())).pack(pady=10)

# Etiquetas y entradas para la inyección basada en unión
ctk.CTkLabel(root, text="Prueba de Inyección SQL Basada en Unión").pack(pady=10)
entry_username_union = ctk.CTkEntry(root, placeholder_text="Usuario")
entry_username_union.pack(pady=5)

# Botón para realizar inyección SQL basada en unión
ctk.CTkButton(root, text="Login Basado en Unión", 
              command=lambda: login_union_based(entry_username_union.get())).pack(pady=10)

# Etiqueta para mostrar los resultados
label_resultado = ctk.CTkLabel(root, text="")
label_resultado.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
```

### **Documentación del Código:**

1. **Base de Datos y Tabla:**
   - Creamos una base de datos SQLite llamada `usuarios.db` con una tabla `users` que contiene los campos `id`, `username` y `password`.
   - Insertamos tres usuarios de ejemplo para realizar las pruebas.
2. **Interfaz Gráfica con CustomTkinter:**
   - Creamos dos secciones: una para la inyección SQL basada en errores y otra para la inyección SQL basada en unión.
   - Cada sección tiene campos de texto para ingresar el nombre de usuario y la contraseña, según el tipo de ataque.
3. **Inyección SQL Basada en Errores:**
   - En la función `login_error_based`, construimos una consulta SQL vulnerable al recibir directamente las entradas del usuario.
   - Si el usuario introduce una entrada maliciosa, el programa intentará ejecutarla y devolverá un error SQL si falla, lo que puede exponer información valiosa para un atacante.
4. **Inyección SQL Basada en Unión:**
   - La función `login_union_based` explota una vulnerabilidad en la consulta SQL al combinar dos consultas usando `UNION`. Esto puede revelar información adicional de la base de datos al combinar diferentes conjuntos de resultados.
5. **Prevención:**
   - Después de demostrar estas vulnerabilidades, es importante guiar a los estudiantes en la prevención de inyecciones SQL utilizando **consultas parametrizadas** o **ORM**. Esto garantiza que los datos del usuario no se traten como código SQL.