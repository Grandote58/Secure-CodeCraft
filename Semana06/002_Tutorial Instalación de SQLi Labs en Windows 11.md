![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **🛠️ Tutorial: Instalación de SQLi Labs en Windows 11**

🔍 **Nivel**: Avanzado
🎯 **Objetivo**: Instalar y configurar **SQLi Labs** en **Windows 11** para realizar pruebas de inyección SQL de manera segura.

## **📌 Introducción**

SQLi Labs es un entorno de práctica para la explotación de **Inyección SQL**, proporcionando múltiples niveles de vulnerabilidades en una aplicación web realista.

Este tutorial te guiará en la instalación y configuración en **Windows 11**, utilizando **XAMPP** como servidor web.

✔️ **¿Qué aprenderás?**
✅ Configurar un servidor web con Apache, PHP y MySQL.
✅ Instalar y ejecutar SQLi Labs en Windows.
✅ Configurar la base de datos correctamente.
✅ Acceder a SQLi Labs para comenzar las pruebas.

> 📢 **Importante**: Este entorno debe usarse **exclusivamente para fines educativos** en sistemas donde tengas permiso para realizar pruebas de seguridad.

------

## **📌 Requisitos Previos**

✔️ Windows 11 instalado.
✔️ Conexión a Internet.
✔️ Conocimientos básicos de **PHP, MySQL y servidores web**.
✔️ Descargar las herramientas necesarias:

- XAMPP
- [Git](https://git-scm.com/downloads)

------

## **🔹 Paso 1: Instalar XAMPP**

XAMPP es un paquete que incluye **Apache (servidor web), MySQL (gestor de bases de datos) y PHP**.

1️⃣ **Descargar XAMPP**

- Ve al sitio oficial: Descargar XAMPP
- Descarga la versión más reciente para Windows.

2️⃣ **Instalar XAMPP**

- Ejecuta el instalador descargado (`xampp-windows-x64-<versión>.exe`).

- Selecciona los componentes **Apache, MySQL y PHP**.

- Elige la ruta de instalación:

  ```bash
  C:\xampp
  ```

- Completa la instalación y **no inicies XAMPP aún**.

3️⃣ **Configurar MySQL en XAMPP**

- Abre **XAMPP Control Panel** desde `C:\xampp\xampp-control.exe`.
- Activa los servicios **Apache** y **MySQL** pulsando `Start`.
- Asegúrate de que **Apache** y **MySQL** muestran el estado `Running`.

📢 **Verificación**:

- Abre tu navegador y accede a:

  ```bash
  http://localhost/
  ```

- Si ves la página de bienvenida de XAMPP, la instalación fue exitosa.

------

## **🔹 Paso 2: Descargar e Instalar SQLi Labs**

SQLi Labs está alojado en GitHub, así que utilizaremos **Git** para descargarlo.

1️⃣ **Abrir la terminal de Git**

- Si no tienes Git instalado, descárgalo desde: [Git para Windows](https://git-scm.com/downloads)

- Abre Git Bash  y ejecuta:

  ```bash
  cd C:/xampp/htdocs
  git clone https://github.com/Audi-1/sqli-labs.git
  ```

2️⃣ **Verifica la instalación**

- Abre el Explorador de Archivos y navega a:

  ```bash
  C:\xampp\htdocs\sqli-labs
  ```

- Deberías ver archivos como `index.html`, `setup-db.sql`, y carpetas de niveles (`Lesson-1`, `Lesson-2`, etc.).

------

## **🔹 Paso 3: Configurar la Base de Datos**

SQLi Labs necesita una base de datos **MySQL** funcional.

1️⃣ **Accede a phpMyAdmin**

- En el navegador, entra a:

  ```bash
  http://localhost/phpmyadmin
  ```

- Crea una nueva base de datos llamada `security`:

  - Ve a la pestaña `Bases de datos`.
  - Escribe `security` en el campo `Nombre de la base de datos` y presiona `Crear`.

2️⃣ **Importar el archivo SQL de SQLi Labs**

- En `phpMyAdmin`, selecciona la base de datos `security`.

- Ve a la pestaña `Importar`.

- Haz clic en `Seleccionar archivo`  y sube el archivo:

  ```bash
  C:\xampp\htdocs\sqli-labs\sql-connections\setup-db.sql
  ```

- Pulsa `Continuar`.

📌 **Verifica la Importación**:

- Si ves las tablas `users`, `emails`, `orders`, etc., significa que la base de datos se configuró correctamente.

## **🔹 Paso 4: Configurar Conexión de SQLi Labs**

1️⃣ **Editar las credenciales de la base de datos**

- Abre el archivo:

  ```bash
  C:\xampp\htdocs\sqli-labs\sql-connections\db-creds.inc
  ```

- Modifica las credenciales:

  ```php
  <?php
  $dbhost = '127.0.0.1';  // Servidor local
  $dbuser = 'root';       // Usuario por defecto en XAMPP
  $dbpass = '';           // Dejar vacío si no has configurado contraseña
  $dbname = 'security';   // Nombre de la base de datos
  ?>
  ```

2️⃣ **Guardar y cerrar el archivo**.

## **🔹 Paso 5: Verificar Instalación**

📢 **Abre el navegador y accede a SQLi Labs**:

```html
http://localhost/sqli-labs/
```

🔹 Si ves la pantalla de bienvenida con los diferentes niveles (`Lesson 1`, `Lesson 2`, etc.), la instalación fue **EXITOSA**. 🚀

## **🔹 Paso 6: Resolver Problemas Comunes**

🔴 **Error "Database Connection Failed"**

- Asegúrate de que MySQL está corriendo en XAMPP.
- Verifica que las credenciales en `db-creds.inc` sean correctas.

🔴 **Error "404 Not Found"**

- Revisa que SQLi Labs está en `C:\xampp\htdocs\sqli-labs`.
- Reinicia Apache en XAMPP.

🔴 **Problemas con permisos de archivos**

- Asegúrate de ejecutar XAMPP como **Administrador**.

- Edita `C:\xampp\apache\conf\httpd.conf` y busca:

  ```bash
  DocumentRoot "C:/xampp/htdocs"
  <Directory "C:/xampp/htdocs">
      Options Indexes FollowSymLinks Includes ExecCGI
      AllowOverride All
      Require all granted
  </Directory>
  ```

  Si `AllowOverride None`, cámbialo a `AllowOverride All`.

- Guarda y reinicia Apache.

## **📌 Conclusión**

🎯 **¡SQLi Labs está listo para usarse en Windows 11!**
Ahora puedes comenzar a practicar **ataques de inyección SQL** en un entorno seguro.

📢 **Próximos Pasos**:

✔️ Explora cada lección de SQLi Labs.
✔️ Usa herramientas como **Burp Suite y SQLmap** para automatizar ataques.
✔️ Aprende a evadir filtros y esquivar WAFs.

💡 **Recuerda siempre practicar hacking ético y solo en entornos donde tengas autorización. 🚀**

![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)