# Aplicación NMAP Personalizada

Creación de una aplicación en **Python** utilizando **CustomTkinter** para realizar un mapeo de la red, listar las direcciones IP, MAC, puertos abiertos, y comprobar vulnerabilidades. La vulnerabilidad se detectará comparando los puertos abiertos con una lista predefinida de puertos críticos que suelen tener vulnerabilidades conocidas.

### Pasos:

1. **Recolección de información de la red**: Utilizaremos la herramienta `nmap` para escanear la red local.
2. **Interfaz gráfica con CustomTkinter**: Se mostrará una lista con las direcciones IP, direcciones MAC, puertos abiertos, y un ícono que identifica si el dispositivo tiene vulnerabilidades en función de los puertos encontrados.
3. **Comprobación de vulnerabilidades**: Se realizará una comparación de los puertos abiertos con una lista de puertos comunes que podrían ser vulnerables.

### Código

```python
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox

# Especifica la ruta a nmap.exe en tu sistema (ajusta esta ruta a donde instalaste Nmap)
nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"  # Cambia la ruta según la instalación de Nmap

# Función para agregar mensajes al Text Area
def log_message(message):
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)  # Hace scroll automático hacia abajo

# Función para obtener la información de la red usando nmap con el comando seleccionado
def scan_network(command):
    log_message(f"Iniciando escaneo de la red con el comando: {command}...")
    try:
        # Usa la ruta completa al ejecutable de nmap con el comando seleccionado
        scan_output = subprocess.check_output([nmap_path] + command.split(), text=True)
        log_message("Escaneo de red completo.")
        return scan_output
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar el escaneo de la red: {e}")
        log_message(f"Error al ejecutar el escaneo: {e}")
        return None

# Función para identificar puertos vulnerables usando nmap en cada IP
def check_ports(ip):
    log_message(f"Escaneando puertos abiertos en {ip}...")
    try:
        # Lista de puertos vulnerables conocidos
        vulnerable_ports = [21, 22, 23, 80, 443, 445, 3389]  # Puertos con vulnerabilidades conocidas
        scan_output = subprocess.check_output([nmap_path, '-p-', ip], text=True)
        open_ports = []
        for line in scan_output.split('\n'):
            if '/tcp' in line and 'open' in line:
                port = int(line.split('/')[0])
                open_ports.append(port)

        vulnerabilities = [port for port in open_ports if port in vulnerable_ports]
        log_message(f"Escaneo de puertos en {ip} completo. Puertos abiertos: {open_ports}. Vulnerabilidades: {vulnerabilities}")
        return open_ports, vulnerabilities
    except Exception as e:
        messagebox.showerror("Error", f"Error al escanear puertos en {ip}: {e}")
        log_message(f"Error al escanear puertos en {ip}: {e}")
        return [], []

# Función para ejecutar el escaneo y llenar la lista en la UI
def execute_scan():
    # Obtener el comando seleccionado del combobox
    selected_command = combo_commands.get()
    
    if not selected_command:
        messagebox.showerror("Error", "Por favor, selecciona un comando de Nmap.")
        return

    log_message(f"Ejecutando escaneo completo de red con el comando '{selected_command}'...")
    result = scan_network(selected_command)
    if result:
        ips = []
        for line in result.split('\n'):
            if 'Nmap scan report for' in line:
                ip = line.split()[-1]
                ips.append(ip)
        
        for ip in ips:
            open_ports, vulnerabilities = check_ports(ip)
            mac_address = "00:00:00:00:00:00"  # Simular MAC (Nmap -sP no encuentra MAC en algunos sistemas)
            status_icon = "✅" if not vulnerabilities else "⚠️"
            port_list = ", ".join(map(str, open_ports))
            vul_list = ", ".join(map(str, vulnerabilities))
            data = (ip, mac_address, port_list, status_icon, vul_list)
            listbox.insert("", "end", values=data)

# Función para iniciar el escaneo en un hilo separado
def start_scan_in_thread():
    scan_thread = threading.Thread(target=execute_scan)
    scan_thread.start()

# Configuración inicial de la ventana usando CustomTkinter
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Mapeo de la Red y Vulnerabilidades")

# Configurar columnas de la tabla
columns = ("IP Address", "MAC Address", "Open Ports", "Vulnerability", "Vulnerable Ports")
listbox = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    listbox.heading(col, text=col)

listbox.pack(pady=20)

# Cuadro de texto tipo Text Area para los logs
text_area = tk.Text(root, height=10, width=70, wrap=tk.WORD)
text_area.pack(pady=10)

# Lista desplegable de comandos Nmap  ... RECUERDA COLOCAR LA DIRECCION IP
commands = [
    "-sP 192.168.20.6/24",   # Escaneo de ping para descubrir hosts activos
    "-sS 192.168.20.6/24",   # Escaneo SYN para detectar puertos abiertos
    "-sU 192.168.20.6/24",   # Escaneo de puertos UDP
    "-A 192.168.20.6/24",    # Escaneo agresivo (descubre OS, servicios y versiones)
    "-p 1-65535 192.168.20.6/24",  # Escaneo de todos los puertos TCP
    "-T4 -A -v 192.168.20.6/24",   # Escaneo rápido con detección de OS y versiones
    "-sV 192.168.20.6/24",   # Detectar versiones de servicios
    "-O 192.168.20.6/24"     # Detectar el sistema operativo de los hosts
]

# Label para la lista desplegable
label_combo = ctk.CTkLabel(root, text="Selecciona un comando Nmap:")
label_combo.pack(pady=5)

# Combobox para seleccionar un comando
combo_commands = ttk.Combobox(root, values=commands)
combo_commands.pack(pady=5)

# Botón para iniciar el escaneo de red
scan_button = ctk.CTkButton(root, text="Escanear Red", command=start_scan_in_thread)
scan_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()

```

### Explicación del código:

1. **Nmap**: Se usa la herramienta `nmap` para escanear las direcciones IP y puertos en la red local. El escaneo de puertos usa `nmap -p-` para obtener todos los puertos abiertos en una dirección IP.
2. **CustomTkinter**:
   - Se utiliza **CustomTkinter** para crear la interfaz gráfica, mostrando una tabla que contiene las direcciones IP, direcciones MAC, puertos abiertos, y un ícono que identifica si el dispositivo tiene vulnerabilidades.
   - Un ícono "⚠️" indica que la dirección IP tiene puertos abiertos que coinciden con los de la lista de puertos vulnerables.
   - Un ícono "✅" indica que no se detectaron puertos vulnerables en esa IP.
3. **Comprobación de vulnerabilidades**: Se define una lista de puertos comunes que son conocidos por tener vulnerabilidades (ejemplo: 22 para SSH, 445 para SMB, etc.). Si un puerto abierto coincide con esta lista, se marca como vulnerable.
4. **Ejecutar el escaneo**: El botón "Escanear Red" ejecuta el escaneo, inserta los datos en la tabla y comprueba las vulnerabilidades.

### Lista de puertos comunes con vulnerabilidades:

- **21 (FTP)**: Transmite datos en texto plano.
- **22 (SSH)**: Ataques de fuerza bruta.
- **23 (Telnet)**: Transmite datos en texto plano.
- **80 (HTTP)**: Vulnerabilidades en aplicaciones web.
- **443 (HTTPS)**: Vulnerabilidades en configuraciones de certificados SSL.
- **445 (SMB)**: Objetivo común de ransomware.
- **3389 (RDP)**: Escalada de privilegios y acceso remoto.

### Requisitos:

1. Instalar Nmap: Debes tener 

   ```bash
   nmap
   ```

    instalado en tu sistema. Puedes instalarlo usando:

   - En Linux: `sudo apt install nmap`
   - En Windows: Descárgalo desde la página oficial. https://nmap.org/

2. Instalar CustomTkinter:

   ```bash
   pip install customtkinter
   ```

### Consideraciones:

- El escaneo de red puede tardar dependiendo del número de dispositivos en tu red.
- En algunos sistemas, `nmap -sP` no recoge direcciones MAC sin privilegios de superusuario. Puedes ejecutar el script como administrador si necesitas obtener las direcciones MAC.





