# Sanitización de una URL de Origin para Evitar Vulnerabilidades de CORS

Cross-Origin Resource Sharing (CORS) permite que los recursos de un servidor web se soliciten desde un dominio diferente al propio. Sin embargo, si no se maneja correctamente, puede abrir la puerta a ataques, como la ejecución de solicitudes no autorizadas desde orígenes maliciosos. Un aspecto crucial para protegerse de estos ataques es sanitizar y validar el origen de las solicitudes antes de permitir el acceso.

## Código Ejemplo en Java con Spring Boot

### **1. Verificación Básica del Origin usando un WhiteList**

```java
import org.springframework.stereotype.Service;
import javax.servlet.http.HttpServletRequest;
import java.util.HashSet;
import java.util.Set;

@Service
public class CorsService {
    
    private static final Set<String> ALLOWED_ORIGINS = new HashSet<>();

    static {
        ALLOWED_ORIGINS.add("https://trusteddomain.com");
        ALLOWED_ORIGINS.add("https://anothertrusteddomain.com");
    }

    public boolean isValidOrigin(HttpServletRequest request) {
        String origin = request.getHeader("Origin");
        return origin != null && ALLOWED_ORIGINS.contains(origin);
    }
}
```

Este ejemplo básico utiliza una lista blanca (`whiteList`) de orígenes permitidos. Antes de procesar la solicitud, se verifica si el origen está en la lista blanca.

### **2. Expresión Regular para Validar el Formato del Origin**

```java
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import java.util.regex.Pattern;

@Service
public class CorsService {

    private static final Pattern ORIGIN_PATTERN = Pattern.compile("https://[a-zA-Z0-9.-]+\\.com");

    public boolean isValidOrigin(HttpServletRequest request) {
        String origin = request.getHeader("Origin");
        return origin != null && ORIGIN_PATTERN.matcher(origin).matches();
    }
}
```

Este enfoque utiliza una expresión regular para verificar que el origen cumple con un patrón esperado, por ejemplo, asegurando que proviene de un dominio `.com` específico.

### **3. Verificación Dinámica con Dominio y Subdominios Permitidos**

```java
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import java.net.URI;
import java.net.URISyntaxException;

@Service
public class CorsService {

    private static final String TRUSTED_DOMAIN = "trusteddomain.com";

    public boolean isValidOrigin(HttpServletRequest request) {
        String origin = request.getHeader("Origin");
        if (origin == null) {
            return false;
        }
        
        try {
            URI originUri = new URI(origin);
            String host = originUri.getHost();
            return host != null && host.endsWith(TRUSTED_DOMAIN);
        } catch (URISyntaxException e) {
            return false;
        }
    }
}
```

En este ejemplo, el código verifica si el host del origen es un dominio confiable o uno de sus subdominios. Esto es útil cuando se desea permitir subdominios de un dominio principal confiable.

## Tres Posibles Opciones en Validación de Entradas y Gestión de Sesiones

### **1. Validación de Entradas:**

- **Validación de Cabecera Origin**: Como se mostró en los ejemplos anteriores, siempre valida la cabecera `Origin` contra una lista de dominios confiables.
- **Saneamiento de Entradas**: Utiliza bibliotecas como `OWASP Java HTML Sanitizer` para limpiar entradas que puedan ser utilizadas en la construcción de URLs o para la creación de recursos, evitando inyecciones de código malicioso.
- **Normalización de URLs**: Asegúrate de que todas las URLs estén en su forma canónica antes de realizar cualquier validación o comparación para prevenir ataques de manipulación de rutas.

### **2. Gestión de Sesiones:**

- **Utilizar Cookies Seguras**: Configura las cookies de sesión con las banderas `HttpOnly` y `Secure` para prevenir el acceso a las cookies mediante scripts y asegurar que solo se envíen a través de HTTPS.
- **Expiración y Renovación de Sesiones**: Implementa una política de expiración de sesiones y renueva las sesiones activas para mitigar ataques de sesión prolongada o secuestro de sesión.
- **Almacenamiento Seguro del Token de Sesión**: En aplicaciones SPA, almacena los tokens de sesión en un `HttpOnly Cookie` en lugar de `localStorage` o `sessionStorage` para mitigar el riesgo de XSS.