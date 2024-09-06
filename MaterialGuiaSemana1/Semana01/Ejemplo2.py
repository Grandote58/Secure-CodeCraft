# Importar las librerías necesarias
import customtkinter as ctk
import sqlite3
from tkinter import ttk

# Conectar a la base de datos SQLite (se creará si no existe)
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

        self.title("Gestión de Estudiantes No. 2")
        self.geometry("500x600")

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

# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

# Cerrar la conexión a la base de datos al finalizar
conexion.close()
