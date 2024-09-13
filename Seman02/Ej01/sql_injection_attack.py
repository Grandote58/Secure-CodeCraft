import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Función para realizar el ataque de inyección SQL
def atacar_sql_inyeccion():
    conn = sqlite3.connect('compras.db')
    cursor = conn.cursor()

    # Capturar la entrada maliciosa
    entrada_maliciosa = entry_maliciosa.get()

    try:
        # Consulta vulnerable (simulación del ataque de inyección SQL)
        query = f"SELECT * FROM customers WHERE name = '{entrada_maliciosa}'"
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Mostrar resultados
        cuadro_resultado.delete(1.0, ctk.END)
        if resultados:
            for row in resultados:
                cuadro_resultado.insert(ctk.END, f"ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Teléfono: {row[3]}\n")
        else:
            cuadro_resultado.insert(ctk.END, "No se encontraron resultados")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")
    finally:
        conn.close()

# Interfaz gráfica para ataque de Inyección SQL
def inicializar_interfaz_sql_inyeccion():
    root = ctk.CTk()
    root.title("Ataque de Inyección SQL")
    root.geometry("500x400")

    ctk.CTkLabel(root, text="Simulación de Ataque de Inyección SQL").pack(pady=10)

    global entry_maliciosa, cuadro_resultado

    # Campo para la entrada maliciosa
    ctk.CTkLabel(root, text="Introduce la entrada maliciosa").pack(pady=5)
    entry_maliciosa = ctk.CTkEntry(root, width=400)
    entry_maliciosa.pack(pady=5)

    # Botón para ejecutar el ataque
    ctk.CTkButton(root, text="Lanzar Ataque SQL", command=atacar_sql_inyeccion).pack(pady=10)

    # Cuadro de texto para mostrar resultados del ataque
    cuadro_resultado = ctk.CTkTextbox(root, width=400, height=200)
    cuadro_resultado.pack(pady=10)

    root.mainloop()

inicializar_interfaz_sql_inyeccion()
