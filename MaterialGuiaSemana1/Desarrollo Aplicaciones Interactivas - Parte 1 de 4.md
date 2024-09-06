# Desarrollo Aplicaciones Interactivas - Parte 1 de 4

**CustomTkinter** - https://customtkinter.tomschimansky.com/

Desarrollar aplicaciones interactivas utilizando **Python**, **CustomTkinter** para la interfaz gráfica, y **SQL** para el manejo de bases de datos. A medida que avancemos, documentaré cada línea de código para asegurar que sea fácil de entender y aplicable en un entorno de aprendizaje.

## Objetivo

Crear una aplicación interactiva que permita a los usuarios gestionar una base de datos de estudiantes, con las siguientes funcionalidades:

1. **Interfaz gráfica** con **CustomTkinter** para ingresar y visualizar datos.
2. **Base de datos** en **SQLite** para almacenar la información de los estudiantes.

## Estructura del proyecto

1. **Instalar las dependencias necesarias**: Asegúrate de tener instalados los paquetes `CustomTkinter` y `SQLite` (que viene integrado con Python).
2. **Crear la interfaz gráfica** con CustomTkinter.
3. **Conectar la aplicación a una base de datos SQLite** para almacenar la información.

### Paso 1: Instalación de CustomTkinter

Si no tienes CustomTkinter instalado, puedes hacerlo con el siguiente comando:

```bash
pip install customtkinter
```

**Crea el archivo de Python**: Copia el código anterior en un archivo llamado `ejemplo1.py` y ejecútalo con `python ejemplo1.py`.

### Paso 2: Estructura básica de la aplicación

```python
# Importar las librerías necesarias
import customtkinter as ctk
import sqlite3

# Conectar a la base de datos SQLite (se creará si no existe)
conexion = sqlite3.connect('estudiantes.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear tabla de estudiantes si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS estudiantes (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  edad INTEGER NOT NULL,
                  grado TEXT NOT NULL)''')
conexion.commit()

# Función para insertar datos en la base de datos
def agregar_estudiante(nombre, edad, grado):
    cursor.execute("INSERT INTO estudiantes (nombre, edad, grado) VALUES (?, ?, ?)", (nombre, edad, grado))
    conexion.commit()

# Función para obtener todos los estudiantes de la base de datos
def obtener_estudiantes():
    cursor.execute("SELECT * FROM estudiantes")
    return cursor.fetchall()

# Función para mostrar estudiantes en consola (puede mejorarse para mostrar en la interfaz)
def mostrar_estudiantes():
    estudiantes = obtener_estudiantes()
    for estudiante in estudiantes:
        print(f"ID: {estudiante[0]}, Nombre: {estudiante[1]}, Edad: {estudiante[2]}, Grado: {estudiante[3]}")

# Crear la aplicación principal con CustomTkinter
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Title de la ventana y tamaño de la ventana
        self.title("Gestión de Estudiantes") 
        self.geometry("400x300")

        # Widgets de entrada para nombre, edad y grado
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.pack(pady=10)

        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.pack()

        self.label_edad = ctk.CTkLabel(self, text="Edad:")
        self.label_edad.pack(pady=10)

        self.entry_edad = ctk.CTkEntry(self)
        self.entry_edad.pack()

        self.label_grado = ctk.CTkLabel(self, text="Grado:")
        self.label_grado.pack(pady=10)

        self.entry_grado = ctk.CTkEntry(self)
        self.entry_grado.pack()

        # Botón para agregar estudiante
        self.boton_agregar = ctk.CTkButton(self, text="Agregar Estudiante", command=self.guardar_estudiante)
        self.boton_agregar.pack(pady=20)

    # Función para obtener los datos ingresados y agregarlos a la base de datos
    def guardar_estudiante(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        grado = self.entry_grado.get()

        if nombre and edad and grado:
            agregar_estudiante(nombre, int(edad), grado)
            print(f"Estudiante {nombre} agregado correctamente.")
            self.entry_nombre.delete(0, ctk.END)
            self.entry_edad.delete(0, ctk.END)
            self.entry_grado.delete(0, ctk.END)
        else:
            print("Por favor, ingrese todos los datos.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

# Cerrar la conexión a la base de datos al finalizar
conexion.close()
```

### Explicación del código

1. **Conexión a la base de datos**: Se crea una base de datos SQLite llamada `estudiantes.db`, que almacena la información de los estudiantes. La tabla `estudiantes` contiene las columnas `id`, `nombre`, `edad`, y `grado`.
2. **Funciones para interactuar con la base de datos**:
   - `agregar_estudiante`: Inserta un nuevo estudiante en la base de datos.
   - `obtener_estudiantes`: Devuelve todos los estudiantes registrados.
   - `mostrar_estudiantes`: Imprime los estudiantes en la consola (más adelante se integrará en la interfaz gráfica).
3. **Interfaz gráfica con CustomTkinter**:
   - Se crean campos de entrada para el nombre, la edad y el grado del estudiante.
   - Un botón que llama a la función `guardar_estudiante` para añadir los datos a la base de datos.