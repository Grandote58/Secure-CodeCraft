![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **🛠️ Tutorial: Instalación de SQLi Labs en Kali Linux**

🔍 **Nivel**: Avanzado
🎯 **Objetivo**: Aprender a instalar y configurar **SQLi Labs** en Kali Linux para realizar pruebas de inyección SQL de manera segura.

## **📌 Introducción**

SQLi Labs es un entorno de aprendizaje diseñado para practicar ataques de **Inyección SQL** en aplicaciones web. Proporciona múltiples niveles de vulnerabilidades y diferentes tipos de consultas SQL para desarrollar habilidades en **hacking ético y seguridad web**.

En este tutorial aprenderás a:

✅ Instalar y configurar un servidor web en **Kali Linux**.
✅ Descargar e instalar **SQLi Labs**.
✅ Configurar la base de datos MySQL para usar el entorno.
✅ Acceder a SQLi Labs y verificar la instalación.

> 📢 **Nota**: Este entorno debe usarse únicamente con fines educativos en sistemas donde tengas permiso para realizar pruebas de seguridad.

## **📌 Requisitos Previos**

Antes de comenzar, asegúrate de tener:

✔️ **Kali Linux** instalado (puede ser en una máquina virtual o equipo físico).
✔️ Conocimientos básicos de **Linux y MySQL**.
✔️ Conexión a Internet para descargar dependencias.

## **🔹 Paso 1: Instalar Dependencias Necesarias**

Kali Linux ya viene con **Apache, MySQL y PHP**, pero es recomendable asegurarse de que estén instalados y actualizados.

1️⃣ **Abre una terminal en Kali Linux** y ejecuta:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install apache2 mariadb-server php php-mysql libapache2-mod-php unzip -y
```

📌 **Explicación**:

- `apache2`: Servidor web necesario para ejecutar SQLi Labs.
- `mariadb-server`: Base de datos compatible con MySQL.
- `php php-mysql libapache2-mod-php`: Módulos PHP para ejecutar scripts en Apache.
- `unzip`: Para descomprimir archivos.

------

## **🔹 Paso 2: Descargar SQLi Labs**

Ahora descargamos **SQLi Labs** desde GitHub.

1️⃣ **Clona el repositorio en la carpeta web de Apache**:

```
bashCopiarcd /var/www/html/
sudo git clone https://github.com/Audi-1/sqli-labs.git
```

2️⃣ **Verifica que los archivos se descargaron correctamente**:

```bash
ls -la /var/www/html/sqli-labs
```

📌 **Resultado esperado**:

```bash
drwxr-xr-x  5 root root  4096 Feb 12 16:35 .
drwxr-xr-x 10 root root  4096 Feb 12 16:30 ..
-rw-r--r--  1 root root  1420 Feb 12 16:35 README.md
-rw-r--r--  1 root root  5120 Feb 12 16:35 setup.sql
```

------

## **🔹 Paso 3: Configurar la Base de Datos MySQL**

1️⃣ **Inicia el servicio de MySQL**:

```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

2️⃣ **Accede a la base de datos**:

```bash
sudo mysql -u root -p
```

*(Si no tienes contraseña configurada, presiona **Enter** cuando te lo pida).*

3️⃣ **Ejecuta los siguientes comandos en MySQL**:

```bash
CREATE DATABASE security;
CREATE USER 'sqli_user'@'localhost' IDENTIFIED BY 'sqli_password';
GRANT ALL PRIVILEGES ON security.* TO 'sqli_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

📌 **Explicación**:

- Crea una base de datos llamada `security`.
- Crea un usuario `sqli_user` con contraseña `sqli_password`.
- Da permisos completos a ese usuario en la base de datos.

4️⃣ **Importar la base de datos desde el script de SQLi Labs**:

```bash
sudo mysql -u root -p security < /var/www/html/sqli-labs/sql-connections/setup-db.sql
```

📌 **Esto inicializará las tablas necesarias en la base de datos `security`.**

------

## **🔹 Paso 4: Configurar SQLi Labs en Apache**

1️⃣ **Modificar permisos de archivos y directorios**:

```bash
sudo chmod -R 755 /var/www/html/sqli-labs/
sudo chown -R www-data:www-data /var/www/html/sqli-labs/
```

📌 **Esto permite que el servidor Apache acceda a los archivos correctamente.**

2️⃣ **Editar configuración de Apache para que reconozca SQLi Labs**: Abre el archivo de configuración:

```bash
sudo nano /etc/apache2/apache2.conf
```

Busca esta línea:

```bash
<Directory /var/www/>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

Cambia `AllowOverride None` por `AllowOverride All`, así:

```bash
<Directory /var/www/>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
```

Guarda y cierra (`CTRL + X`, luego `Y` y `Enter`).

3️⃣ **Reinicia Apache para aplicar los cambios**:

```bash
sudo systemctl restart apache2
```

------

## **🔹 Paso 5: Acceder a SQLi Labs**

1️⃣ **Abre tu navegador en Kali Linux** y ve a:

```bash
http://localhost/sqli-labs/
```

2️⃣ **Verifica que se muestra la pantalla de SQLi Labs.**
Si ves un mensaje de bienvenida y una lista de niveles, significa que la instalación fue exitosa. 🚀

------

## **🔹 Paso 6: Resolver Problemas Comunes**

🔴 **Error 403 o 404 al acceder a SQLi Labs**

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

🔴 **Error de conexión con la base de datos**

- Verifica que el usuario `sqli_user` y la base de datos `security` existen.

```bash
sudo mysql -u root -p -e "SHOW DATABASES;"
sudo mysql -u root -p -e "SELECT user, host FROM mysql.user;"
```

- Verifica que la configuración en `sql-connections/db-creds.inc` es correcta.

------

## **📌 Conclusión**

🎯 ¡Felicidades! Has instalado **SQLi Labs** en Kali Linux correctamente. Ahora puedes comenzar a practicar inyecciones SQL en un entorno controlado.

![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)