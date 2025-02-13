![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **INSTALACIÓN DETALLADA DE SQLi LABS EN WINDOWS 11**

**🎯 Objetivo:**
En este tutorial aprenderás a instalar **SQLi Labs** en **Windows 11** usando **XAMPP** como servidor web y base de datos. SQLi Labs es una plataforma de aprendizaje para probar **ataques de inyección SQL** de diferentes niveles.

✅ **Nivel:** Principiante - Intermedio
✅ **Tiempo estimado:** 30 - 45 minutos
✅ **Requisitos previos:** Conocimientos básicos de **PHP, MySQL y entornos web locales**

## **📌 INSTALACIÓN DE XAMPP EN WINDOWS 11**

**🔹 Paso 1: Descargar XAMPP**

1. **Accede a la web oficial de XAMPP:**
   📍 https://www.apachefriends.org/download.html
2. Descarga la versión de **XAMPP para Windows**.
3. Guarda el archivo en tu computadora y ejecútalo.

**🔹 Paso 2: Instalar XAMPP**

1. **Ejecuta el instalador** (`xampp-windows-x64-xx.x.x-installer.exe`).
2. Selecciona los componentes necesarios:
   - **Apache** ✅ (Servidor web)
   - **MySQL** ✅ (Base de datos)
   - **PHP** ✅
   - **phpMyAdmin** ✅
3. Haz clic en **Next** y selecciona la carpeta de instalación (por defecto `C:\xampp`).
4. Completa la instalación y **espera que finalice**.

**🔹 Paso 3: Iniciar XAMPP**

1. Abre el **Panel de Control de XAMPP** (`xampp-control.exe`).
2. Inicia los siguientes servicios:
   - ✅ Apache (servidor web)
   - ✅ MySQL (base de datos)
3. Verifica que el servidor funciona:
   - Abre tu navegador y entra a:
     📍 **http://localhost**
   - Si ves la página de inicio de XAMPP, la instalación fue exitosa.

## **📌 DESCARGA E INSTALACIÓN DE SQLi LABS**

**🔹 Paso 4: Descargar SQLi Labs**

1. Abre **una terminal de Windows (CMD)** y ejecuta:

   ```bash
   C:\xampp\htdocs
   git clone https://github.com/Audi-1/sqli-labs.git
   ```

   *💡 Si no tienes Git instalado, descarga e instala Git desde:*
   📍 https://git-scm.com/downloads

2. Alternativamente, **descarga manualmente SQLi Labs**:

   - Ve a https://github.com/Audi-1/sqli-labs.
   - Haz clic en **Code > Download ZIP**.
   - Extrae el contenido en `C:\xampp\htdocs\sqli-labs`.

**🔹 Paso 5: Configurar la Base de Datos**

1. **Abre phpMyAdmin** en tu navegador:
   📍 **http://localhost/phpmyadmin**

2. **Crea una nueva base de datos:**

   - Haz clic en **Nueva**.
   - Ingresa **security** como nombre de la base de datos.
   - Selecciona **utf8_general_ci** como cotejamiento.
   - Pulsa **Crear**.

3. **Importar las tablas de SQLi Labs:**

   - En phpMyAdmin, selecciona **security**.

   - Ve a la pestaña **Importar**.

   - Pulsa Seleccionar Archivo y busca:

     ```bash
     C:\xampp\htdocs\sqli-labs\databases\setup-db.sql
     ```

   - Haz clic en **Continuar**.

------

**🔹 Paso 6: Configurar SQLi Labs en el Servidor**

1. Abre el archivo de configuración:

   ```bash
   C:\xampp\htdocs\sqli-labs\sql-connections\db-creds.inc
   ```

2. Modifica las credenciales de la base de datos:

   ```php+HTML
   <?php
   $dbuser = "root";  // Usuario por defecto en XAMPP
   $dbpass = "";      // En XAMPP no hay contraseña por defecto
   $dbname = "security";
   ?>
   ```

3. Guarda los cambios y cierra el archivo.

------

**🔹 Paso 7: Verificar la Instalación**

1. Abre tu navegador y accede a: 📍 **http://localhost/sqli-labs**
2. Si ves la pantalla de inicio de SQLi Labs, ¡todo está listo! 🚀

## **📌 SOLUCIÓN DE PROBLEMAS**

### **🔹 Error: Apache no Inicia en XAMPP**

✅ **Causa:** Otro programa usa el puerto 80 (Ej: Skype, IIS).
🔹 **Solución:**

1. Abre el Panel de Control de XAMPP.

2. Haz clic en **Config > Apache (httpd.conf)**.

3. Busca la línea:

   ```bash
   Listen 80
   ```

4. Cambia el puerto (Ej: 8080):

   ```bash
   Listen 8080
   ```

5. Guarda y reinicia Apache.

📍 Ahora accede a **http://localhost:8080/sqli-labs**

### **🔹 Error: No se Puede Conectar a la Base de Datos**

✅ **Causa:** Credenciales incorrectas en `db-creds.inc`.
🔹 **Solución:**

1. Verifica que `$dbuser` sea root  y `$dbpass` esté vacío:

   ```php+HTML
   $dbuser = "root";
   $dbpass = "";
   ```

2. Asegúrate de haber importado correctamente **setup-db.sql** en phpMyAdmin.

### **🔹 Error: Página en Blanco en SQLi Labs**

✅ **Causa:** PHP no muestra errores.
🔹 **Solución:**

1. Abre `C:\xampp\php\php.ini`.

2. Busca:

   ```php+HTML
   display_errors = Off
   ```

3. Cambia a:

   ```php+HTML
   display_errors = On
   ```

4. Guarda y reinicia Apache.

## **📌 PRIMEROS PASOS EN SQLi LABS**

Una vez que SQLi Labs esté funcionando, puedes comenzar con **prácticas de inyección SQL**.

### **🔹 Práctica 1: Verificar si un Campo es Vulnerable**

1. Abre el **Lesson 1**: 📍 **http://localhost/sqli-labs/Less-1**

2. Prueba ingresar en la URL:

   ```php+HTML
   http://localhost/sqli-labs/Less-1/?id=1'
   ```

3. Si ves un error SQL, la página es vulnerable.



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)