![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **🛠️ Práctica Detallada de Hacking Ético en Aplicaciones Web con WebGoat y Kali Linux**

## **📌 Objetivo de la Práctica**

Esta práctica tiene como objetivo proporcionar un **entorno controlado** en el que los estudiantes puedan aprender a identificar y mitigar ataques en aplicaciones web mediante herramientas de **Kali Linux** y el marco de trabajo **WebGoat**. Se simulará un entorno empresarial vulnerable, aplicando la **metodología NIST 800-115** para realizar pruebas de penetración de manera ética y controlada.

------

## **📌 Escenario Simulado: Empresa “Banco-Alpina”**

### **📌 Descripción de Banco-Alpina**

**Banco-Alpina** es una empresa ficticia que ofrece servicios financieros en línea a sus clientes. Recientemente, han detectado intentos de ataques a su plataforma y han contratado a un equipo de seguridad para realizar pruebas de penetración y detectar vulnerabilidades en su aplicación web.

### **📌 Entorno de Prueba**

Para esta práctica, utilizaremos **WebGoat**, una aplicación web intencionalmente vulnerable desarrollada por OWASP, para aprender sobre las vulnerabilidades de las aplicaciones web y cómo mitigarlas.

------

## **📌 Herramientas Necesarias**

| Herramienta    | Descripción                                            |
| -------------- | ------------------------------------------------------ |
| **Kali Linux** | Sistema operativo con herramientas de pentesting.      |
| **WebGoat**    | Aplicación web vulnerable para pruebas de seguridad.   |
| **Nmap**       | Escaneo de puertos y detección de servicios.           |
| **SQLmap**     | Identificación y explotación de vulnerabilidades SQLi. |
| **Burp Suite** | Manipulación de tráfico web y pruebas de seguridad.    |
| **Nikto**      | Análisis de seguridad en servidores web.               |
| **Gobuster**   | Descubrimiento de directorios ocultos.                 |

------

## **📌 Parte 1: Instalación del Entorno de Práctica**

### **1️⃣ Instalación de WebGoat en Kali Linux**

📌 **Paso 1: Descargar WebGoat**
Abre una terminal en Kali Linux y ejecuta:

```bash
wget https://github.com/WebGoat/WebGoat/releases/download/v8.2.2/webgoat-server-8.2.2.jar -O WebGoat.jar
```

🔹 Descargamos WebGoat en su versión más reciente.

📌 **Paso 2: Ejecutar WebGoat**

```bash
java -jar WebGoat.jar
```

🔹 WebGoat se ejecutará en `http://localhost:8080/WebGoat`.

📌 **Paso 3: Acceder a WebGoat**
🔹 Abre un navegador y accede a `http://localhost:8080/WebGoat`.
🔹 Crea una cuenta con credenciales ficticias para iniciar sesión.

------

## **📌 Parte 2: Metodología de Hacking Ético en WebGoat**

### **🕵️‍♂️ 1️⃣ Fase de Reconocimiento** (Escaneo de la infraestructura)

📌 **Escanear puertos abiertos en el servidor WebGoat**

```bash
nmap -sV -p 8080 localhost
```

🔹 Nos permite identificar el puerto y servicios que están corriendo en WebGoat.

📌 **Descubrir directorios ocultos**

```bash
gobuster dir -u http://localhost:8080/WebGoat -w /usr/share/wordlists/dirb/common.txt
```

🔹 Nos permite encontrar rutas y directorios vulnerables dentro de WebGoat.

------

### **💥 2️⃣ Fase de Análisis de Vulnerabilidades**

📌 **Escaneo de seguridad con Nikto**

```bash
nikto -h http://localhost:8080/WebGoat
```

🔹 Busca vulnerabilidades conocidas en la configuración del servidor web.

📌 **Identificación de Tecnologías Web**

```bash
whatweb http://localhost:8080/WebGoat
```

🔹 Nos permite conocer qué tecnologías utiliza la aplicación para encontrar posibles exploits.

------

### **🚀 3️⃣ Fase de Explotación de Vulnerabilidades**

#### **🔴 Ataque 1: SQL Injection (SQLi)**

📌 **Ejecutar un ataque SQL Injection en WebGoat**
🔹 Dirígete a `SQL Injection (Introduction)` dentro de WebGoat y realiza el siguiente ataque:

```sql
' OR '1'='1' -- 
```

🔹 Esto permite acceder sin credenciales válidas.

📌 **Automatizar SQL Injection con SQLmap**

```bash
sqlmap -u "http://localhost:8080/WebGoat/login" --data "username=admin&password=123" --dbs
```

🔹 Extrae las bases de datos disponibles en el servidor.

✅ **Mitigación:**
🔹 Implementar **validación de entradas** y **uso de consultas preparadas** para prevenir SQLi.

------

#### **🔵 Ataque 2: Cross-Site Scripting (XSS)**

📌 **Ejecutar un ataque XSS**
🔹 Dirígete a `Cross-Site Scripting (XSS)` dentro de WebGoat y en un campo de entrada introduce:

```html
<script>alert('Hacked!')</script>
```

🔹 Esto ejecutará un script en la página web.

✅ **Mitigación:**
🔹 Implementar **escapado de caracteres** y filtros de entrada para evitar la ejecución de scripts maliciosos.

------

#### **🟢 Ataque 3: Cross-Site Request Forgery (CSRF)**

📌 **Ejecutar un ataque CSRF**
🔹 Dirígete a `CSRF` dentro de WebGoat e intenta modificar datos con un enlace como este:

```html
<img src="http://localhost:8080/WebGoat/cambiarClave?clave=nueva123" />
```

🔹 Si la víctima está autenticada, su contraseña se cambiará sin su consentimiento.

✅ **Mitigación:**
🔹 Implementar **tokens CSRF** en formularios y solicitudes críticas.

------

## **📌 Parte 4: Reporte y Mitigación**

🔹 **Documentar** las vulnerabilidades encontradas.
🔹 **Priorizar** los riesgos según impacto y facilidad de explotación.
🔹 **Recomendar soluciones** como sanitización de entradas, autenticación reforzada y configuraciones seguras.

Ejemplo de reporte:

| **Vulnerabilidad** | **Impacto** | **Prueba Realizada**                               | **Mitigación**               |
| ------------------ | ----------- | -------------------------------------------------- | ---------------------------- |
| SQL Injection      | Crítico     | Se accedió a la base de datos sin credenciales     | Usar consultas preparadas    |
| XSS                | Alto        | Se ejecutó un script en el navegador de la víctima | Filtrar y escapar caracteres |
| CSRF               | Medio       | Se manipuló una solicitud sin validación           | Implementar tokens CSRF      |



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)