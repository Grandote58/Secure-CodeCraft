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
