# Importar las librerías necesarias
import customtkinter as ctk
import sqlite3
from tkinter import ttk
import csv

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

# Función para buscar estudiantes por nombre
def buscar_estudiantes(nombre):
    cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ?", ('%' + nombre + '%',))
    return cursor.fetchall()

# Función para eliminar estudiante por ID
def eliminar_estudiante(id):
    cursor.execute("DELETE FROM estudiantes WHERE id = ?", (id,))
    conexion.commit()

# Función para exportar estudiantes a CSV
def exportar_csv(estudiantes):
    with open("estudiantes.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nombre", "Edad", "Grado"])
        writer.writerows(estudiantes)

# Crear la aplicación principal con CustomTkinter
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Estudiantes No. 3")
        self.geometry("500x500")

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

        # Entrada de búsqueda
        self.label_busqueda = ctk.CTkLabel(self, text="Buscar por Nombre:")
        self.label_busqueda.pack(pady=5)

        self.entry_busqueda = ctk.CTkEntry(self)
        self.entry_busqueda.pack()

        # Botón para buscar estudiante
        self.boton_buscar = ctk.CTkButton(self, text="Buscar Estudiante", command=self.buscar_estudiantes)
        self.boton_buscar.pack(pady=10)

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

        # Botón para exportar a CSV
        self.boton_exportar = ctk.CTkButton(self, text="Exportar a CSV", command=self.exportar_estudiantes)
        self.boton_exportar.pack(pady=10)

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

    # Función para buscar estudiantes por nombre
    def buscar_estudiantes(self):
        nombre = self.entry_busqueda.get()
        estudiantes = buscar_estudiantes(nombre)
        # Limpiar la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insertar los resultados en la tabla
        for estudiante in estudiantes:
            self.tree.insert("", "end", values=estudiante)

    # Función para exportar los datos de estudiantes a un archivo CSV
    def exportar_estudiantes(self):
        estudiantes = obtener_estudiantes()
        exportar_csv(estudiantes)
        print("Datos exportados a estudiantes.csv")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

# Cerrar la conexión a la base de datos al finalizar
conexion.close()
