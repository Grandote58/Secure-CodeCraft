# **Tipos de inyección de SQL**

## SQL **fuera de banda (OOB)**. 

La inyección SQL fuera de banda es más difícil de detectar porque en lugar de devolver resultados directamente en la aplicación, utiliza canales de comunicación externos para exfiltrar datos (por ejemplo, mediante DNS, HTTP, etc.).

### **Objetivo:**

Desarrollar una aplicación que permita simular un ataque de inyección SQL fuera de banda en una base de datos SQLite, mostrando cómo se puede enviar información a un servidor externo simulado. La práctica incluye la documentación del código en español.

### **Requisitos:**

1. **Python 3.x** instalado.
2. **CustomTkinter** instalado (`pip install customtkinter`).
3. **SQLite3** (incluido con Python).
4. Uso de una herramienta de simulación externa (en este caso, simularemos el canal fuera de banda con un simple log de archivos).

### **Paso 1: Crear una Base de Datos Simulada**

Primero, creamos la base de datos en SQLite con una tabla básica de usuarios.

```python
import sqlite3

# Crear la conexión a la base de datos
conn = sqlite3.connect('usuarios_oob.db')
cursor = conn.cursor()

# Crear una tabla de usuarios
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

Ahora crearemos la interfaz gráfica con **CustomTkinter**, donde los usuarios pueden intentar realizar una inyección SQL fuera de banda.

```python
import customtkinter as ctk
import sqlite3

# Función que simula un canal fuera de banda, escribe el ataque en un archivo simulado
def enviar_fuera_de_banda(datos_exfiltrados):
    with open("exfiltracion_oob.log", "a") as f:
        f.write(f"Datos exfiltrados: {datos_exfiltrados}\n")

# Función para simular inyección SQL fuera de banda
def login_oob_injection(username, password):
    conn = sqlite3.connect('usuarios_oob.db')
    cursor = conn.cursor()

    try:
        # Consulta vulnerable a inyección SQL fuera de banda
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            label_resultado.config(text="Login exitoso: Usuario encontrado")
        else:
            label_resultado.config(text="Login fallido: Usuario no encontrado")
        
        # Aquí simulamos la extracción de datos a través de un canal fuera de banda
        # Por ejemplo, si el atacante añade una carga maliciosa para exfiltrar datos
        if "exfiltrar" in username:
            enviar_fuera_de_banda(f"Exfiltración de datos usando el nombre de usuario: {username}")

    except sqlite3.Error as e:
        # Mostrar el error SQL
        label_resultado.config(text=f"Error SQL: {str(e)}")

    conn.close()

# Configuración de la ventana principal
root = ctk.CTk()
root.geometry("400x300")
root.title("Simulación de Inyección SQL Fuera de Banda")

# Etiquetas y entradas para el login
ctk.CTkLabel(root, text="Prueba de Inyección SQL Fuera de Banda").pack(pady=10)
entry_username_oob = ctk.CTkEntry(root, placeholder_text="Usuario")
entry_username_oob.pack(pady=5)
entry_password_oob = ctk.CTkEntry(root, placeholder_text="Contraseña", show="*")
entry_password_oob.pack(pady=5)

# Botón para realizar login con inyección SQL fuera de banda
ctk.CTkButton(root, text="Login SQL Fuera de Banda", 
              command=lambda: login_oob_injection(entry_username_oob.get(), entry_password_oob.get())).pack(pady=10)

# Etiqueta para mostrar los resultados
label_resultado = ctk.CTkLabel(root, text="")
label_resultado.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
```

### **Documentación del Código:**

1. **Base de Datos y Tabla:**
   - Se crea una base de datos SQLite llamada `usuarios_oob.db` con una tabla de usuarios que incluye `id`, `username`, y `password`.
   - Se insertan tres usuarios para realizar pruebas con datos válidos.
2. **Función `enviar_fuera_de_banda`:**
   - Esta función simula un canal fuera de banda (OOB). En un escenario real, los datos podrían ser exfiltrados a un servidor remoto usando peticiones HTTP, DNS, etc.
   - Aquí, los datos exfiltrados se registran en un archivo de log llamado `exfiltracion_oob.log`, para simular el envío de la información a un servidor externo.
3. **Función `login_oob_injection`:**
   - Realiza una consulta SQL vulnerable que utiliza directamente las entradas del usuario sin protección.
   - Si el nombre de usuario contiene la palabra clave `"exfiltrar"`, la función llama a `enviar_fuera_de_banda` para simular la extracción de información sensible.
4. **Interfaz Gráfica con CustomTkinter:**
   - Se crea una interfaz gráfica que permite a los usuarios ingresar un nombre de usuario y una contraseña, simulando un ataque SQL fuera de banda.
   - Los resultados se muestran en la interfaz gráfica, indicando si el login fue exitoso o fallido.
   - Si se detecta un intento de exfiltración de datos (al ingresar `"exfiltrar"` en el campo de usuario), los datos se registran en el archivo de log.

### **Paso 3: Prueba de la Inyección SQL Fuera de Banda**

1. Ejecuta la aplicación.

2. Ingresa un nombre de usuario que incluya `"exfiltrar"`, como por ejemplo:

   ```yaml
   exfiltrar_admin
   ```

   Esto activará la función de exfiltración de datos.

3. Verifica el archivo de log `exfiltracion_oob.log`. El archivo debería contener una línea similar a:

   ```yaml
   Datos exfiltrados: Exfiltración de datos usando el nombre de usuario: exfiltrar_admin
   ```

### **Prevención:**

En este punto, puedes enseñar a los estudiantes cómo prevenir este tipo de ataques usando **consultas parametrizadas** y validando adecuadamente las entradas del usuario, para evitar que se ejecuten comandos maliciosos.







