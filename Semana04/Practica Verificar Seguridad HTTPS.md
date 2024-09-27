# **Practica Verificar Seguridad HTTPS**

Para verificar las configuraciones de seguridad en sitios web HTTPS. Esta aplicación realiza una verificación básica del estado de un certificado HTTPS, comprobando si el sitio utiliza un certificado válido, la versión del protocolo SSL/TLS, y si soporta métodos de cifrado seguros.

### Código de la aplicación:

```python
import socket
import ssl
import datetime
import customtkinter as ctk
from tkinter import messagebox

# Configuración inicial de la ventana usando CustomTkinter
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Verificación de Seguridad en HTTPS")

# Función para agregar mensajes al Text Area
def log_message(message):
    text_area.insert(ctk.END, message + "\n")
    text_area.see(ctk.END)  # Hace scroll automático hacia abajo

# Función para verificar la configuración HTTPS
def verify_https():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Por favor, ingrese una URL.")
        return

    if not url.startswith("https://"):
        messagebox.showwarning("Advertencia", "El sitio no está utilizando HTTPS.")
        return

    try:
        # Remover "https://" si está presente
        url = url.replace("https://", "")
        
        log_message(f"Verificando HTTPS para {url}...")

        # Establecer la conexión SSL/TLS con el servidor
        context = ssl.create_default_context()
        with socket.create_connection((url, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                cert = ssock.getpeercert()

                # Validar el certificado
                log_message("Certificado válido encontrado.")
                
                # Obtener la fecha de expiración del certificado
                cert_expiry = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                log_message(f"Fecha de expiración del certificado: {cert_expiry}")

                # Verificar la vigencia del certificado
                if cert_expiry < datetime.datetime.now():
                    log_message("El certificado ha expirado.")
                else:
                    log_message(f"El certificado es válido hasta: {cert_expiry}")

                # Versión del protocolo SSL/TLS
                log_message(f"Versión del protocolo SSL/TLS: {ssock.version()}")

                # Obtener información adicional sobre el cifrado utilizado
                cipher_info = ssock.cipher()
                log_message(f"Algoritmo de cifrado: {cipher_info[0]}")
                log_message(f"Versión del protocolo de cifrado: {cipher_info[1]}")
                log_message(f"Fuerza del cifrado: {cipher_info[2]} bits")

    except ssl.SSLError as e:
        log_message(f"Error SSL: {e}")
    except socket.error as e:
        log_message(f"Error de conexión: {e}")
    except Exception as e:
        log_message(f"Error desconocido: {e}")

# Interfaz gráfica
# Campo para ingresar la URL
url_label = ctk.CTkLabel(root, text="Ingrese URL del sitio web HTTPS:")
url_label.pack(pady=5)

url_entry = ctk.CTkEntry(root, width=300)
url_entry.pack(pady=5)

# Botón para verificar el HTTPS
verify_https_button = ctk.CTkButton(root, text="Verificar HTTPS", command=verify_https)
verify_https_button.pack(pady=10)

# Cuadro de texto para los logs de la aplicación
text_area = ctk.CTkTextbox(root, height=300, width=500)
text_area.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
```

### Descripción del Código:

1. **Verificación HTTPS**:
   - La aplicación verifica la conexión SSL/TLS con un sitio web dado.
   - Extrae el **certificado SSL**, y valida su **vigencia**, es decir, si el certificado ha expirado o es válido.
   - Muestra la **versión del protocolo SSL/TLS** y la **información del cifrado** utilizado por el servidor.
2. **Validación del certificado**:
   - La función `getpeercert()` permite extraer el certificado del servidor y verifica si este es válido.
   - Se extrae la **fecha de expiración** del certificado, y se compara con la fecha actual para comprobar si ha caducado.
3. **Protocolo SSL/TLS**:
   - Se utiliza `ssock.version()` para obtener la versión del protocolo SSL/TLS que el servidor está utilizando.
   - La información del cifrado (algoritmo de cifrado, versión, y fuerza) también se extrae y se muestra.

### Funcionalidades de la Interfaz Gráfica:

- **URL Input**: El usuario ingresa la URL del sitio web a analizar (debe comenzar con `https://`).
- **Botón de Verificación**: Ejecuta la verificación cuando el usuario hace clic.
- **Cuadro de Texto**: Muestra los resultados de la verificación, incluyendo la fecha de expiración del certificado, el protocolo SSL/TLS utilizado, y el algoritmo de cifrado.

### Requisitos:

- Instalar dependencias:

  ```bash
  pip install customtkinter
  ```

### Características adicionales:

1. **Valida si el sitio utiliza HTTPS**: Si no comienza con `https://`, la aplicación mostrará una advertencia.
2. **Detalles del certificado**: Muestra la fecha de expiración del certificado y la versión de SSL/TLS utilizada.
3. **Información del cifrado**: Muestra el algoritmo de cifrado utilizado por el servidor.