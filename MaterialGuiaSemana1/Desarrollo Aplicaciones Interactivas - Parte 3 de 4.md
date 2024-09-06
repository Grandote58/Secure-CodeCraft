# Desarrollo Aplicaciones Interactivas - Parte 3 de 4

**CustomTkinter** - https://customtkinter.tomschimansky.com/

Agregar la funcionalidad para **actualizar** la información de los estudiantes. Con esta mejora, podrás seleccionar un estudiante en la tabla, cargar sus datos en los campos de entrada, modificar la información y luego actualizarla en la base de datos.

### Paso 1: Agregar la funcionalidad de actualización

Aquí está el código actualizado con la nueva función para **actualizar estudiantes**:

```python
# Importar las librerías necesarias
import customtkinter as ctk
import sqlite3
from tkinter import ttk

# Conectar a la base de datos SQLite
conexion = sqlite3.connect('estudiantes.db')
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

# Función para actualizar los datos del estudiante en la base de datos
def actualizar_estudiante(id_estudiante, nombre, edad, grado):
    cursor.execute("UPDATE estudiantes SET nombre = ?, edad = ?, grado = ? WHERE id = ?", (nombre, edad, grado, id_estudiante))
    conexion.commit()

# Función para obtener todos los estudiantes de la base de datos
def obtener_estudiantes():
    cursor.execute("SELECT * FROM estudiantes")
    return cursor.fetchall()

# Función para eliminar estudiante por ID
def eliminar_estudiante(id):
    cursor.execute("DELETE FROM estudiantes WHERE id = ?", (id,))
    conexion.commit()

# Crear la aplicación principal con CustomTkinter
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Estudiantes")
        self.geometry("500x450")

        self.id_seleccionado = None  # Para guardar el ID del estudiante seleccionado

        # Widgets de entrada para nombre, edad y grado
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.pack(pady=5)

        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.pack()

        self.label_edad = ctk.CTkLabel(self, text="Edad:")
        self.label_edad.pack(pady=5)

        self.entry_edad = ctk.CTkEntry(self)
        self.entry_edad.pack()

        self.label_grado = ctk.CTkLabel(self, text="Grado:")
        self.label_grado.pack(pady=5)

        self.entry_grado = ctk.CTkEntry(self)
        self.entry_grado.pack()

        # Botón para agregar estudiante
        self.boton_agregar = ctk.CTkButton(self, text="Agregar Estudiante", command=self.guardar_estudiante)
        self.boton_agregar.pack(pady=10)

        # Botón para actualizar estudiante
        self.boton_actualizar = ctk.CTkButton(self, text="Actualizar Estudiante", command=self.actualizar_estudiante)
        self.boton_actualizar.pack(pady=10)

        # Crear un Treeview para mostrar los estudiantes
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Edad", "Grado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Grado", text="Grado")
        self.tree.pack(pady=10, fill="x")

        # Botón para eliminar estudiante
        self.boton_eliminar = ctk.CTkButton(self, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        self.boton_eliminar.pack(pady=10)

        # Evento para seleccionar estudiante
        self.tree.bind('<ButtonRelease-1>', self.seleccionar_estudiante)

        # Cargar estudiantes al iniciar la aplicación
        self.cargar_estudiantes()

    # Función para obtener los datos ingresados y agregarlos a la base de datos
    def guardar_estudiante(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        grado = self.entry_grado.get()

        if nombre and edad and grado:
            agregar_estudiante(nombre, int(edad), grado)
            self.entry_nombre.delete(0, ctk.END)
            self.entry_edad.delete(0, ctk.END)
            self.entry_grado.delete(0, ctk.END)
            self.cargar_estudiantes()  # Actualizar tabla
        else:
            print("Por favor, ingrese todos los datos.")

    # Función para cargar estudiantes en el Treeview
    def cargar_estudiantes(self):
        # Eliminar filas previas
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Obtener estudiantes de la base de datos
        estudiantes = obtener_estudiantes()
        for estudiante in estudiantes:
            self.tree.insert("", "end", values=estudiante)

    # Función para eliminar estudiante seleccionado
    def eliminar_estudiante(self):
        # Obtener el estudiante seleccionado
        seleccionado = self.tree.focus()
        if seleccionado:
            valores = self.tree.item(seleccionado, "values")
            id_estudiante = valores[0]
            eliminar_estudiante(id_estudiante)
            self.cargar_estudiantes()  # Actualizar tabla

    # Función para seleccionar un estudiante del Treeview
    def seleccionar_estudiante(self, event):
        seleccionado = self.tree.focus()
        if seleccionado:
            valores = self.tree.item(seleccionado, "values")
            self.id_seleccionado = valores[0]
            self.entry_nombre.delete(0, ctk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_edad.delete(0, ctk.END)
            self.entry_edad.insert(0, valores[2])
            self.entry_grado.delete(0, ctk.END)
            self.entry_grado.insert(0, valores[3])

    # Función para actualizar los datos del estudiante seleccionado
    def actualizar_estudiante(self):
        if self.id_seleccionado:
            nombre = self.entry_nombre.get()
            edad = self.entry_edad.get()
            grado = self.entry_grado.get()
            if nombre and edad and grado:
                actualizar_estudiante(self.id_seleccionado, nombre, int(edad), grado)
                self.cargar_estudiantes()  # Actualizar tabla
                print(f"Estudiante {nombre} actualizado correctamente.")
                self.limpiar_campos()
            else:
                print("Por favor, ingrese todos los datos.")
        else:
            print("Por favor, seleccione un estudiante para actualizar.")

    # Función para limpiar los campos de entrada
    def limpiar_campos(self):
        self.entry_nombre.delete(0, ctk.END)
        self.entry_edad.delete(0, ctk.END)
        self.entry_grado.delete(0, ctk.END)
        self.id_seleccionado = None

# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

# Cerrar la conexión a la base de datos al finalizar
conexion.close()
```

### Explicación de las mejoras:

1. **Selección del estudiante**: Ahora, al hacer clic en un estudiante en la tabla, los datos se cargarán en los campos de entrada (nombre, edad, grado), permitiendo su edición.
2. **Actualización del estudiante**: Se ha añadido un botón y una función para actualizar la información de un estudiante seleccionado. Al hacer clic en "Actualizar Estudiante", los datos se actualizan en la base de datos.
3. **Limpieza de campos**: Después de actualizar o agregar un estudiante, los campos de entrada se limpian para facilitar el ingreso de nuevos datos.