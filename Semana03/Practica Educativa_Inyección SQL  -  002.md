



![Mesa de trabajo 1Head](D:\0000_CONTRATO_UNIMINUTO\pLANTILLAgNERALcURSOS\2x\Mesa de trabajo 1Head.png)

# **Practica Inyección SQL  -  002**

## Ataque de Inyección SQL utilizando PostgreSQL y DVWA

## Configuración del Entorno Controlado en Kali Linux

### Instalación y Configuración de Kali Linux

1. **Descargar Kali Linux**:
   - Visita el sitio web oficial de Kali Linux https://www.kali.org/downloads/.
   - Descarga la imagen ISO adecuada para tu sistema.
2. **Crear una Máquina Virtual** (opcional):
   - Utiliza software como VirtualBox o VMware para crear una nueva máquina virtual.
   - Asigna recursos adecuados (al menos 2 GB de RAM y 20 GB de espacio en disco).
3. **Instalar Kali Linux**:
   - Monta la imagen ISO de Kali Linux en tu máquina virtual o en tu hardware.
   - Sigue las instrucciones del instalador para completar la instalación.

### Descarga e Instalación de DVWA en Kali Linux

1. **Actualizar el Sistema**:

```bash
sudo apt update
sudo apt upgrade -y
```

2. **Instalar Dependencias**:

```bash
sudo apt install apache2 postgresql postgresql-contrib php php-pgsql php-gd libapache2-mod-php -y
```

3. **Descargar DVWA**:

```bash
cd /var/www/html
sudo git clone https://github.com/digininja/DVWA.git
sudo chown -R www-data:www-data DVWA
sudo chmod -R 755 DVWA
```

### Configuración del Servidor Web Apache y Base de Datos PostgreSQL

1. **Iniciar Servicios**:

```bash
sudo service apache2 start
sudo service postgresql start
```

2. **Configurar la Base de Datos PostgreSQL para DVWA**:

- Cambia al usuario `postgres`:

```bash
sudo -i -u postgres
```

* Inicia el intérprete de comandos de PostgreSQL:

```bash
psql
```

En el prompt de PostgreSQL, ejecuta los siguientes comandos:

```sql
CREATE DATABASE dvwa;
CREATE USER dvwa_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dvwa TO dvwa_user;
\q
```

### **Configurar DVWA**:

- Renombra el archivo `config/config.inc.php.dist` a `config/config.inc.php`.
- Edita `config/config.inc.php` para reflejar las credenciales de la base de datos:

```php
$_DVWA['db_server'] = '127.0.0.1';
$_DVWA['db_database'] = 'dvwa';
$_DVWA['db_user'] = 'dvwa_user';
$_DVWA['db_password'] = 'password';
```

### Configuración de la Base de Datos en DVWA

1. **Acceder a DVWA**:
   - Abre un navegador web y navega a `http://localhost/DVWA/setup.php`.
   - Sigue las instrucciones para crear la base de datos.
2. **Iniciar Sesión en DVWA**:
   - Navega a `http://localhost/DVWA/login.php`.
   - Utiliza las credenciales por defecto: `admin` / `password`.

### Identificación de Fallos de Seguridad en DVWA

1. **Acceder a la Sección de Inyecciones SQL**:
   - Después de iniciar sesión, navega a `Vulnerability` en el menú principal y selecciona `SQL Injection`.
2. **Analizar Vulnerabilidades**:
   - Realiza pruebas en los campos de entrada para identificar posibles vulnerabilidades de inyección SQL.
   - Por ejemplo, introduce `' OR '1'='1` en el campo de entrada para ver si puedes manipular la consulta SQL.

### Posibles Vulnerabilidades al Crear la Base de Datos en PostgreSQL

1. **Configuración Insegura de Usuarios y Permisos**:

   - Asignar todos los privilegios al usuario `dvwa_user` puede ser una práctica insegura. En un entorno de producción, los usuarios deberían tener privilegios mínimos necesarios.

   ```sql
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dvwa_user;
   ```

2. **Falta de Validación y Sanitización de Entradas**:

- Asegurarse de que todas las entradas de los usuarios sean validadas y sanitizadas antes de ser procesadas por la base de datos.

3. **Configuración Insegura de la Conexión**:

- Evitar usar contraseñas débiles y asegurar la conexión a la base de datos mediante SSL/TLS.

### Realización del Ataque de Inyección SQL

1. **Utilizar Metasploit para Ejecutar un Ataque de Inyección SQL**:
   - Abre Metasploit en Kali Linux:

```bash
msfconsole
```

2. **Buscar y Seleccionar un Módulo de SQL Injection**:

```bash
search sql_injection
use auxiliary/scanner/http/sql_injection
```

3. **Configurar el Módulo**:

```bash
set RHOSTS 127.0.0.1
set RPORT 80
set TARGETURI /DVWA/vulnerabilities/sqli/
run
```

4. **Ejecutar el Ataque**:

- Sigue las instrucciones del módulo para realizar el ataque y observa los resultados.

### Mitigación y Protección contra Inyecciones SQL

1. **Estrategias de Protección**:
   - **Usar consultas preparadas (prepared statements)**: Asegúrate de que las consultas SQL se construyan de manera segura utilizando parámetros.
   - **Validación de Entradas**: Implementa una validación robusta de todos los datos de entrada para asegurarte de que solo se permita la entrada esperada.
   - **Escapar Caracteres Especiales**: Utiliza funciones que escapen caracteres especiales en las consultas SQL.
   - **Revisiones de Código y Pruebas de Seguridad**: Realiza revisiones de código regulares y pruebas de seguridad para identificar y corregir vulnerabilidades.
2. **Parchear Vulnerabilidades en DVWA**:
   - Edita los scripts PHP de DVWA para implementar las prácticas de codificación segura mencionadas anteriormente.
   - Actualiza las configuraciones y scripts para asegurar que todas las entradas sean validadas y sanitizadas adecuadamente.

### Conclusión

Esta práctica guiada proporciona una visión detallada de cómo configurar un entorno de prueba seguro utilizando PostgreSQL, identificar vulnerabilidades y realizar un ataque de inyección SQL. Además, destaca la importancia de implementar estrategias de mitigación para proteger las aplicaciones web contra estos ataques.







![Mesa de trabajo 1FOOTER](D:\0000_CONTRATO_UNIMINUTO\pLANTILLAgNERALcURSOS\2x\Mesa de trabajo 1FOOTER.png)











