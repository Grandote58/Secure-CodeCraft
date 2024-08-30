# **Modelo Entidad-Relación (ER)** 

### Sistema de login que incluye el seguimiento de las conexiones, IPs, fechas, tiempos de conexión y roles de acceso

### Modelo Entidad-Relación (ER)

Primero, definiremos las entidades necesarias y sus atributos, así como las relaciones entre ellas.

#### Entidades:

1. **Usuario**:
   - **id_usuario** (PK, INT, Auto Increment)
   - **nombre_usuario** (VARCHAR, Unique)
   - **email** (VARCHAR, Unique)
   - **contraseña** (VARCHAR)
   - **fecha_creación** (DATETIME)
   - **estado** (ENUM: activo, inactivo)
2. **Rol**:
   - **id_rol** (PK, INT, Auto Increment)
   - **nombre_rol** (VARCHAR, Unique)
   - **descripcion** (VARCHAR)
3. **Usuario_Rol**: (Asociativa para definir los roles de cada usuario)
   - **id_usuario** (FK, INT)
   - **id_rol** (FK, INT)
4. **Conexión**:
   - **id_conexion** (PK, INT, Auto Increment)
   - **id_usuario** (FK, INT)
   - **ip_conexion** (VARCHAR)
   - **fecha_conexion** (DATETIME)
   - **tiempo_conexion** (INT, en segundos)
   - **navegador** (VARCHAR)
   - **sistema_operativo** (VARCHAR)
5. **Intento_Login**: (Para registrar intentos fallidos de login)
   - **id_intento** (PK, INT, Auto Increment)
   - **id_usuario** (FK, INT)
   - **ip_intento** (VARCHAR)
   - **fecha_intento** (DATETIME)
   - **exitoso** (BOOLEAN)

#### Relaciones:

- **Usuario** tiene una relación de uno a muchos con **Conexión**.
- **Usuario** tiene una relación de uno a muchos con **Intento_Login**.
- **Usuario** tiene una relación de muchos a muchos con **Rol** a través de la entidad asociativa **Usuario_Rol**.

## Script SQL

### Script SQL

```sql
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS sistema_login;
USE sistema_login;

-- Crear la tabla de Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    fecha_creación DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo'
);

-- Crear la tabla de Rol
CREATE TABLE Rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

-- Crear la tabla de Usuario_Rol (Tabla asociativa para la relación muchos a muchos)
CREATE TABLE Usuario_Rol (
    id_usuario INT,
    id_rol INT,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol) ON DELETE CASCADE
);

-- Crear la tabla de Conexión
CREATE TABLE Conexión (
    id_conexion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    ip_conexion VARCHAR(45) NOT NULL,
    fecha_conexion DATETIME DEFAULT CURRENT_TIMESTAMP,
    tiempo_conexion INT NOT NULL,
    navegador VARCHAR(100),
    sistema_operativo VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- Crear la tabla de Intento_Login
CREATE TABLE Intento_Login (
    id_intento INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    ip_intento VARCHAR(45) NOT NULL,
    fecha_intento DATETIME DEFAULT CURRENT_TIMESTAMP,
    exitoso BOOLEAN NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- Insertar roles básicos
INSERT INTO Rol (nombre_rol, descripcion) VALUES 
('Admin', 'Administrador del sistema con todos los permisos'),
('Usuario', 'Usuario estándar con permisos limitados'),
('Moderador', 'Usuario con permisos de moderación');

-- Ejemplo de inserción de un usuario
INSERT INTO Usuario (nombre_usuario, email, contraseña) VALUES 
('admin', 'admin@example.com', 'password_hash_123'), 
('user1', 'user1@example.com', 'password_hash_456');

-- Asignar roles a los usuarios
INSERT INTO Usuario_Rol (id_usuario, id_rol) VALUES 
(1, 1),  -- Admin
(2, 2);  -- Usuario

-- Ejemplo de inserción de una conexión
INSERT INTO Conexión (id_usuario, ip_conexion, tiempo_conexion, navegador, sistema_operativo) VALUES 
(1, '192.168.1.1', 3600, 'Chrome', 'Windows 10'),
(2, '192.168.1.2', 1800, 'Firefox', 'Ubuntu');

-- Ejemplo de inserción de un intento de login
INSERT INTO Intento_Login (id_usuario, ip_intento, exitoso) VALUES 
(2, '192.168.1.3', FALSE), 
(1, '192.168.1.4', TRUE);
```

### Descripción de la Implementación

1. **Tablas:** Se crean las tablas `Usuario`, `Rol`, `Usuario_Rol`, `Conexión` y `Intento_Login` conforme al modelo ER que diseñamos.
2. **Llaves Primarias y Foráneas:** Cada tabla tiene su llave primaria y las relaciones están implementadas con llaves foráneas para mantener la integridad referencial.
3. **Enum y valores por defecto:** La tabla `Usuario` utiliza un `ENUM` para el estado de la cuenta y tiene valores por defecto en algunos campos, como la fecha de creación.
4. **Reglas de eliminación en cascada:** Las relaciones con `ON DELETE CASCADE` aseguran que cuando un usuario es eliminado, todas sus conexiones, intentos de login y roles asociados también se eliminen automáticamente.
5. **Datos iniciales:** Se insertan roles básicos (`Admin`, `Usuario`, `Moderador`), un par de usuarios de ejemplo, y se asignan roles a estos usuarios.

### Procedimiento Almacenado

```sql
DELIMITER //

CREATE PROCEDURE InsertarDatosAleatorios()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE randomUsername VARCHAR(50);
    DECLARE randomEmail VARCHAR(100);
    DECLARE randomPassword VARCHAR(255);
    DECLARE randomEstado ENUM('activo', 'inactivo');
    DECLARE randomIP VARCHAR(45);
    DECLARE randomBrowser VARCHAR(100);
    DECLARE randomOS VARCHAR(100);
    DECLARE randomRoleId INT;
    DECLARE randomTiempoConexion INT;
    DECLARE randomSuccess BOOLEAN;

    WHILE i < 40 DO
        -- Generar datos aleatorios para el Usuario
        SET randomUsername = CONCAT('user', FLOOR(1000 + RAND() * 9000));
        SET randomEmail = CONCAT(randomUsername, '@example.com');
        SET randomPassword = CONCAT('password', FLOOR(1000 + RAND() * 9000));
        SET randomEstado = IF(RAND() < 0.5, 'activo', 'inactivo');

        -- Insertar Usuario
        INSERT INTO Usuario (nombre_usuario, email, contraseña, estado) 
        VALUES (randomUsername, randomEmail, randomPassword, randomEstado);

        -- Obtener el ID del último usuario insertado
        SET @lastUserId = LAST_INSERT_ID();

        -- Asignar un rol aleatorio al usuario
        SET randomRoleId = FLOOR(1 + RAND() * 3);
        INSERT INTO Usuario_Rol (id_usuario, id_rol) 
        VALUES (@lastUserId, randomRoleId);

        -- Generar datos aleatorios para la Conexión
        SET randomIP = CONCAT('192.168.', FLOOR(1 + RAND() * 254), '.', FLOOR(1 + RAND() * 254));
        SET randomBrowser = IF(RAND() < 0.5, 'Chrome', 'Firefox');
        SET randomOS = IF(RAND() < 0.5, 'Windows 10', 'Ubuntu');
        SET randomTiempoConexion = FLOOR(60 + RAND() * 3600); -- entre 1 min y 1 hora

        -- Insertar Conexión
        INSERT INTO Conexión (id_usuario, ip_conexion, tiempo_conexion, navegador, sistema_operativo) 
        VALUES (@lastUserId, randomIP, randomTiempoConexion, randomBrowser, randomOS);

        -- Generar datos aleatorios para el Intento_Login
        SET randomIP = CONCAT('192.168.', FLOOR(1 + RAND() * 254), '.', FLOOR(1 + RAND() * 254));
        SET randomSuccess = IF(RAND() < 0.5, TRUE, FALSE);

        -- Insertar Intento_Login
        INSERT INTO Intento_Login (id_usuario, ip_intento, exitoso) 
        VALUES (@lastUserId, randomIP, randomSuccess);

        -- Incrementar el contador
        SET i = i + 1;
    END WHILE;
END //

DELIMITER ;
```



Herramienta para crear el MER

https://chartdb.io/

