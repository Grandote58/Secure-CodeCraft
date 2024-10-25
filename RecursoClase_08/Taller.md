# TALLER DE APLICACION



### **Paso 1: Preparación del Entorno**

#### Instalación de Kali Linux

1. **Descargar Kali Linux**:
   Visita el sitio oficial de Kali Linux y selecciona la versión para máquina virtual (VM) o instalación en un equipo físico.
2. **Configuración de Red**:
   En el entorno virtual, configura la red en “NAT” o “Bridged” para que Kali tenga acceso a Internet y permita la simulación de tráfico.

------

### **Paso 2: Instalación y Configuración de DVWA con MariaDB**

#### 1. Instalar Apache, MariaDB y PHP

Ejecuta los siguientes comandos en la terminal para instalar los servicios necesarios:

```bash
sudo apt update
sudo apt install apache2 mariadb-server php php-mysqli git -y
```

#### 2. Configurar MariaDB

1. Inicia el servicio de MariaDB y asegúrate de que esté activo:

   ```bash
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```

2. Configura MariaDB ejecutando el siguiente comando y sigue las instrucciones (especifica una contraseña segura para el usuario root):

   ```bash
   sudo mysql_secure_installation
   ```

3. Accede a MariaDB para crear la base de datos para DVWA:

   ```bash
   sudo mysql -u root -p
   ```

   Dentro de la consola de MariaDB, ejecuta estos comandos para crear la base de datos y el usuario:

   ```bash
   CREATE DATABASE dvwa;
   CREATE USER 'dvwa_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

#### 3. Descargar DVWA desde GitHub

1. Navega al directorio de Apache y descarga DVWA:

   ```bash
   cd /var/www/html
   sudo git clone https://github.com/digininja/DVWA.git
   ```

2. Cambia los permisos de los archivos de DVWA:

   ```bash
   sudo chown -R www-data:www-data DVWA/
   ```

#### 4. Configurar DVWA

1. Copia el archivo de configuración de DVWA:

   ```bash
   cd DVWA/config
   sudo cp config.inc.php.dist config.inc.php
   ```

2. Edita el archivo de configuración para conectar MariaDB.  Abre el archivo `config.inc.php` con un editor de texto:

   ```bash
   sudo nano config.inc.php
   ```

   Cambia las siguientes líneas:

   ```php
   $_DVWA[ 'db_server' ] = '127.0.0.1';
   $_DVWA[ 'db_database' ] = 'dvwa';
   $_DVWA[ 'db_user' ] = 'dvwa_user';
   $_DVWA[ 'db_password' ] = 'password';
   ```

3. Reinicia Apache para que los cambios surtan efecto:

   ```bash
   sudo systemctl restart apache2
   ```

4. Accede a DVWA en el navegador usando `http://<IP_DE_TU_SERVIDOR>/DVWA` y sigue las instrucciones para completar la instalación.

------

### **Paso 3: Escaneo de Servicios Web con Nmap**

#### Instalación de Nmap

Nmap ya viene instalado en Kali Linux, pero puedes actualizarlo si es necesario:

```bash
sudo apt update
sudo apt install nmap -y
```

#### Escaneo de Puertos y Servicios

1. Para realizar un escaneo básico de puertos y servicios, ejecuta:

   ```bash
   nmap -sV <IP_DE_DVWA>
   ```

2. Para detectar vulnerabilidades en el servidor web, utiliza el script de vulnerabilidades:

   ```bash
   nmap --script vuln <IP_DE_DVWA>
   ```

Este paso permite identificar servicios y posibles vulnerabilidades en el servidor.

------

### **Paso 4: Auditoría de Vulnerabilidades con Nikto**

#### Instalación de Nikto

Nikto también está preinstalado en Kali Linux. Si no lo tienes, instálalo:

```bash
sudo apt update
sudo apt install nikto -y
```

#### Uso de Nikto

1. Ejecuta Nikto para escanear el servidor en busca de configuraciones débiles:

   ```bash
   nikto -h http://<IP_DE_DVWA>
   ```

Nikto escaneará el servidor y te mostrará los resultados de posibles configuraciones y archivos inseguros.

------

### **Paso 5: Identificación y Mitigación con OWASP ZAP**

#### Instalación de OWASP ZAP

OWASP ZAP también está preinstalado en Kali Linux. Si no lo tienes, descárgalo:

```bash
sudo apt update
sudo apt install zaproxy -y
```

#### Configuración y Escaneo

1. Abre OWASP ZAP:

   ```bash
   zaproxy
   ```

2. En la interfaz, selecciona el "Modo de ataque" y usa la opción “Quick Start”.

3. Introduce la URL de DVWA (`http://<IP_DE_DVWA>`) y ejecuta el escaneo.

4. En la pestaña “Alert”, examina vulnerabilidades como XSS o SQLi.

OWASP ZAP te mostrará detalles de cada vulnerabilidad, lo cual permite profundizar en la mitigación.

------

### **Paso 6: Pruebas de Interceptación con Burp Suite**

#### Instalación de Burp Suite

Burp Suite está incluido en Kali Linux. Si necesitas instalarlo, ejecuta:

```bash
sudo apt update
sudo apt install burpsuite -y
```

#### Configuración del Proxy

1. Abre Burp Suite:

   ```bash
   burpsuite
   ```

2. Configura el navegador para que use el proxy de Burp Suite (`127.0.0.1:8080`).

3. Activa “Intercept” para capturar las solicitudes HTTP de DVWA.

#### Ejemplo de Interceptación para SQLi

1. Ingresa a un formulario en DVWA y envía un valor de prueba en el formulario.
2. Observa la solicitud en Burp Suite e intenta modificar los parámetros para explorar SQLi.
3. Usa la pestaña de “Repeater” para probar diferentes cargas de entrada y ver las respuestas del servidor.

Este paso es fundamental para aprender cómo se podrían explotar vulnerabilidades manualmente.

------

### **Paso 7: Explotación Controlada con Metasploit**

#### Instalación de Metasploit

Metasploit está incluido en Kali Linux. Para abrirlo, ejecuta:

```bash
msfconsole
```

#### Escaneo de Servicios con Metasploit

1. Usa el siguiente módulo para identificar la versión del servicio:

   ```bash
   use auxiliary/scanner/http/http_version
   set RHOSTS <IP_DE_DVWA>
   run
   ```

2. Carga un módulo de explotación si identificas una vulnerabilidad aplicable (por ejemplo, módulos de SQLi).

Metasploit permite realizar pruebas controladas para evaluar cómo se comporta la aplicación frente a ataques avanzados.

------



## Herramientas de Auditoria

### **a. Lynis: Auditoría de Seguridad del Sistema**

**Descripción**:
Lynis es una herramienta de auditoría de seguridad que evalúa la seguridad del sistema operativo, analizando configuraciones y buscando posibles vulnerabilidades en Linux.

#### Instalación de Lynis

Lynis ya viene preinstalado en Kali Linux. Si no lo tienes, puedes instalarlo ejecutando:

```bash
sudo apt update
sudo apt install lynis -y
```

#### Uso de Lynis para Auditoría de Seguridad

1. **Ejecutar un escaneo completo**: En la terminal, ejecuta el siguiente comando para iniciar un análisis completo de seguridad del sistema:

   ```bash
   sudo lynis audit system
   ```

2. **Interpretar los resultados**: Lynis presentará un informe que incluye recomendaciones para mejorar la seguridad. Los resultados están divididos en secciones (autenticación, red, servicios, etc.), lo que permite una revisión exhaustiva de cada área.

3. **Acciones recomendadas**: En el informe, busca la sección de "Warning" o "Suggestions" y aplica las recomendaciones para fortalecer la seguridad, como ajustes en la configuración de red o autenticación de usuarios.

------

### **b. Wpscan: Escáner de Vulnerabilidades en WordPress**

**Descripción**:
Wpscan es una herramienta especializada en detectar vulnerabilidades en sitios web que usan WordPress. Permite analizar temas, plugins y configuraciones de seguridad específicas.

#### Instalación de Wpscan

Wpscan viene preinstalado en Kali Linux, pero asegúrate de tener la última versión ejecutando:

```bash
sudo apt update
sudo apt install wpscan -y
```

#### Uso de Wpscan para Detectar Vulnerabilidades

1. **Registrar una clave de API gratuita**: Para usar Wpscan, necesitas una clave de API de [Wpscan](https://wpscan.com/). Regístrate y obtén una clave de API gratuita.

2. **Ejecutar el escaneo básico**: Una vez que tengas la clave de API, realiza un escaneo en el sitio web de WordPress:

   ```bash
   wpscan --url http://<URL_DEL_SITIO> --api-token <TU_API_KEY>
   ```

3. **Detección de vulnerabilidades en plugins y temas**: Para escanear plugins y temas, ejecuta:

   ```bash
   wpscan --url http://<URL_DEL_SITIO> --enumerate p,t --api-token <TU_API_KEY>
   ```

4. **Interpretación de resultados**: Wpscan generará un informe de posibles vulnerabilidades en el sitio, indicando si existen plugins o temas vulnerables que requieren actualizaciones o medidas de seguridad adicionales.

------

### **c. Searchsploit: Búsqueda de Explotaciones y Vulnerabilidades**

**Descripción**:
Searchsploit es una interfaz de línea de comandos para la base de datos de Exploit-DB, que contiene exploits y pruebas de concepto de vulnerabilidades. Es útil para encontrar posibles exploits específicos para software o servicios identificados en un sistema.

#### Instalación de Searchsploit

Searchsploit está incluido en Kali Linux. Puedes actualizar su base de datos ejecutando:

```bash
sudo apt update
searchsploit -u
```

#### Uso de Searchsploit para Buscar Vulnerabilidades

1. **Buscar vulnerabilidades en software específico**: Si conoces el nombre del software o servicio en el que deseas encontrar vulnerabilidades (por ejemplo, Apache), ejecuta:

   ```bash
   searchsploit apache
   ```

2. **Filtrar resultados**: Para obtener resultados específicos, puedes incluir la versión del software. Por ejemplo:

   ```bash
   searchsploit apache 2.4
   ```

3. **Explorar los exploits encontrados**: Cada exploit estará asociado con un archivo de prueba de concepto. Puedes ver la ubicación de estos archivos y copiarlos a tu sistema para realizar pruebas controladas:

   ```bash
   searchsploit -p <ID_DEL_EXPLOIT>
   ```

4. **Ejecutar exploits en un entorno seguro**: Antes de ejecutar cualquier exploit, asegúrate de estar en un entorno controlado (como DVWA o un laboratorio). Esto te permitirá probar vulnerabilidades sin afectar el sistema de producción.



## Herramientas Generación de Reportes



### 1. **Faraday**

**Descripción**:
Faraday es una plataforma de colaboración para auditorías de seguridad que permite centralizar los resultados de múltiples herramientas de análisis de vulnerabilidades y crear reportes detallados. Es especialmente útil para trabajos en equipo, ya que permite compartir y analizar los resultados en tiempo real.

#### Instalación de Faraday

1. **Instalación en Kali Linux**: Faraday está incluido en los repositorios de Kali, pero también puedes instalarlo manualmente. Ejecuta:

   ```bash
   sudo apt update
   sudo apt install faraday
   ```

2. **Iniciar Faraday**: Después de instalar, inicia el servidor con el siguiente comando:

   ```bash
   faraday-server
   ```

3. **Acceso a la Interfaz Web**: Abre tu navegador y accede a `http://localhost:5985/` para ver la interfaz web de Faraday. Aquí podrás gestionar proyectos y ver los resultados de los escaneos en un formato centralizado.

4. **Integración con otras herramientas**: Faraday permite importar resultados de herramientas de análisis como Nmap, Nikto, Burp Suite, y otras. Puedes subir los archivos de reporte generados por estas herramientas y Faraday los estructurará en un formato de informe.

#### Generación de Reportes

- Faraday permite exportar los resultados en diferentes formatos, como **PDF** y **HTML**, con detalles de cada vulnerabilidad identificada, las herramientas utilizadas y recomendaciones.

------

### 2. **Dradis**

**Descripción**:
Dradis es una plataforma de colaboración diseñada para gestionar la información de pruebas de seguridad y generar reportes detallados. Dradis organiza los resultados y permite agregar notas, comentarios y descripciones, lo cual facilita la generación de informes personalizados y detallados.

#### Instalación de Dradis

1. **Instalación en Kali Linux**: Dradis también está disponible en los repositorios de Kali. Instálalo con:

   ```bash
   sudo apt update
   sudo apt install dradis
   ```

2. **Iniciar Dradis**: Una vez instalado, inicia Dradis desde la terminal:

   ```bash
   dradis
   ```

3. **Acceso a la Interfaz Web**: Al igual que Faraday, Dradis ofrece una interfaz web a la que puedes acceder en `http://localhost:3000/`. Aquí puedes gestionar proyectos, cargar resultados y trabajar con ellos.

4. **Importación de Resultados**: Dradis admite archivos de exportación de herramientas de análisis de vulnerabilidades como Nmap, Burp Suite, y Nessus. Puedes importar estos archivos para organizarlos y analizarlos en un formato más detallado.

#### Generación de Reportes

- Dradis facilita la exportación de los resultados en formatos como **HTML**, **XML**, y **PDF**. Los informes generados incluyen detalles de las vulnerabilidades encontradas, posibles soluciones, y recomendaciones específicas para la mitigación.



### **Paso 8: Documentación y Presentación de Resultados**

1. **Registro de Hallazgos**:
   Documenta cada vulnerabilidad encontrada, su impacto potencial y los pasos específicos para la mitigación.
2. **Informe de Seguridad**:
   Organiza los hallazgos en un informe detallado para tu organización, destacando las vulnerabilidades críticas.
3. **Conclusiones**:
   Sugiere la implementación de controles de seguridad periódicos y una revisión de las prácticas de codificación segura.