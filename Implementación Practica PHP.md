# Implementación Practica PHP

## Estructura de Carpetas

Organizar tu proyecto en una estructura de carpetas clara facilita el mantenimiento y la escalabilidad. A continuación, se muestra una estructura recomendada para la aplicación `sistema_login`:

```css
sistema_login/
│
├── css/
│   └── styles.css
│
├── includes/
│   ├── config.php
│   ├── header.php
│   └── footer.php
│   └── conexionesip.php
│
├── register.php
├── login.php
├── dashboard.php
└── logout.php
```

- **css/**: Contendrá los archivos CSS personalizados.
- **includes/**: Contendrá archivos PHP reutilizables como la configuración de la base de datos, encabezados y pies de página.
- **register.php**: Página de registro de usuarios.
- **login.php**: Página de inicio de sesión.
- **dashboard.php**: Página protegida que solo pueden acceder usuarios autenticados.
- **logout.php**: Script para cerrar sesión.

------

## Configuración de la Base de Datos

Antes de comenzar con los archivos de la aplicación, asegúrate de tener la base de datos configurada correctamente. Utiliza el script SQL proporcionado anteriormente para crear las tablas necesarias.

**Nota:** Asegúrate de que la base de datos `sistema_login` y las tablas (`Usuario`, `Rol`, `Usuario_Rol`, `Conexión`, `Intento_Login`) estén creadas y configuradas según tus necesidades.

------

## Archivos de la Aplicación

A continuación, se detallan cada uno de los archivos necesarios para la aplicación `sistema_login`, incluyendo su código y documentación.

### 1. `config.php`

Este archivo contiene la configuración de la conexión a la base de datos y se incluirá en otros archivos PHP para facilitar el acceso a la base de datos.

```php+HTML
<?php

/**
 * Configuración de la conexión a la base de datos MySQL.
 * Asegúrate de actualizar las credenciales según tu entorno.
 */

$servername = "localhost";
$username = "root"; // Cambia esto por tu usuario de MySQL
$password = "";     // Cambia esto por tu contraseña de MySQL
$dbname = "sistema_login";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}
?>

```

### 2. `styles.css`

Archivo CSS personalizado para estilizar la aplicación. Puedes modificar o ampliar estos estilos según tus necesidades.

```css
/* css/styles.css */

/* Estilos generales */
body {
    background-color: #f8f9fa;
}

/* Estilo para el contenedor principal */
.container {
    margin-top: 50px;
    max-width: 500px;
}

/* Estilos para el formulario */
form {
    background: #ffffff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

/* Estilo para los botones */
.btn-custom {
    background-color: #007bff;
    color: #ffffff;
}

.btn-custom:hover {
    background-color: #0056b3;
}
```

### 3. `header.php`

Encabezado común para las páginas de la aplicación, incluye enlaces a Bootstrap y el CSS personalizado.

```php+HTML
<!-- includes/header.php -->

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema Login</title>
    <!-- Enlace a Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Enlace al CSS personalizado -->
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <!-- Barra de navegación -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Sistema Login</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" 
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <?php if(isset($_SESSION['id_usuario'])): ?>
                        <li class="nav-item">
                            <a class="nav-link" href="dashboard.php">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="logout.php">Cerrar Sesión</a>
                        </li>
                    <?php else: ?>
                        <li class="nav-item">
                            <a class="nav-link" href="register.php">Registrarse</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="login.php">Iniciar Sesión</a>
                        </li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>
    </nav>
    <!-- Fin de la barra de navegación -->

    <div class="container">
```

### 4. `footer.php`

Pie de página común para las páginas de la aplicación, incluye enlaces a scripts de Bootstrap.

```php+HTML
<!-- includes/footer.php -->

    </div> <!-- Fin del contenedor -->

    <!-- Enlace a Bootstrap JS y dependencias -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 5. `register.php`

Página de registro de usuarios. Permite a los nuevos usuarios crear una cuenta.

```php+HTML
<?php
// register.php
session_start();
require_once 'includes/config.php';

// Inicializar variables
$nombre_usuario = $email = $password = $confirm_password = "";
$nombre_usuario_err = $email_err = $password_err = $confirm_password_err = "";

// Procesar datos del formulario cuando se envía
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Validar nombre de usuario
    if (empty(trim($_POST["nombre_usuario"]))) {
        $nombre_usuario_err = "Por favor, ingresa un nombre de usuario.";
    } else {
        // Preparar una declaración SELECT
        $sql = "SELECT id_usuario FROM Usuario WHERE nombre_usuario = ?";

        if ($stmt = $conn->prepare($sql)) {
            $stmt->bind_param("s", $param_username);
            $param_username = trim($_POST["nombre_usuario"]);

            if ($stmt->execute()) {
                $stmt->store_result();

                if ($stmt->num_rows == 1) {
                    $nombre_usuario_err = "Este nombre de usuario ya está en uso.";
                } else {
                    $nombre_usuario = trim($_POST["nombre_usuario"]);
                }
            } else {
                echo "Algo salió mal. Por favor, inténtalo de nuevo.";
            }

            $stmt->close();
        }
    }

    // Validar email
    if (empty(trim($_POST["email"]))) {
        $email_err = "Por favor, ingresa un correo electrónico.";
    } else {
        // Validar formato de email
        if (!filter_var(trim($_POST["email"]), FILTER_VALIDATE_EMAIL)) {
            $email_err = "Formato de correo electrónico inválido.";
        } else {
            // Preparar una declaración SELECT
            $sql = "SELECT id_usuario FROM Usuario WHERE email = ?";

            if ($stmt = $conn->prepare($sql)) {
                $stmt->bind_param("s", $param_email);
                $param_email = trim($_POST["email"]);

                if ($stmt->execute()) {
                    $stmt->store_result();

                    if ($stmt->num_rows == 1) {
                        $email_err = "Este correo electrónico ya está registrado.";
                    } else {
                        $email = trim($_POST["email"]);
                    }
                } else {
                    echo "Algo salió mal. Por favor, inténtalo de nuevo.";
                }

                $stmt->close();
            }
        }
    }

    // Validar contraseña
    if (empty(trim($_POST["password"]))) {
        $password_err = "Por favor, ingresa una contraseña.";     
    } elseif (strlen(trim($_POST["password"])) < 6) {
        $password_err = "La contraseña debe tener al menos 6 caracteres.";
    } else {
        $password = trim($_POST["password"]);
    }

    // Validar confirmación de contraseña
    if (empty(trim($_POST["confirm_password"]))) {
        $confirm_password_err = "Por favor, confirma la contraseña.";     
    } else {
        $confirm_password = trim($_POST["confirm_password"]);
        if (empty($password_err) && ($password != $confirm_password)) {
            $confirm_password_err = "Las contraseñas no coinciden.";
        }
    }

    // Verificar errores antes de insertar en la base de datos
    if (empty($nombre_usuario_err) && empty($email_err) && empty($password_err) && empty($confirm_password_err)) {
        
        // Preparar una declaración INSERT
        $sql = "INSERT INTO Usuario (nombre_usuario, email, contraseña, estado) VALUES (?, ?, ?, 'activo')";

        if ($stmt = $conn->prepare($sql)) {
            // Enlazar variables a la declaración preparada como parámetros
            $stmt->bind_param("sss", $param_username, $param_email, $param_password);

            // Establecer parámetros
            $param_username = $nombre_usuario;
            $param_email = $email;
            $param_password = password_hash($password, PASSWORD_DEFAULT); // Crear un hash de la contraseña

            // Intentar ejecutar la declaración preparada
            if ($stmt->execute()) {
                // Obtener el ID del último usuario insertado
                $last_user_id = $conn->insert_id;

                // Asignar un rol predeterminado (por ejemplo, 'Usuario' con id_rol = 2)
                $sql_role = "INSERT INTO Usuario_Rol (id_usuario, id_rol) VALUES (?, 2)";
                if ($stmt_role = $conn->prepare($sql_role)) {
                    $stmt_role->bind_param("i", $param_user_id);
                    $param_user_id = $last_user_id;
                    $stmt_role->execute();
                    $stmt_role->close();
                }

                // Redirigir al usuario a la página de inicio de sesión
                header("location: login.php");
                exit();
            } else {
                echo "Algo salió mal. Por favor, inténtalo de nuevo.";
            }

            $stmt->close();
        }
    }

    // Cerrar conexión
    $conn->close();
}
?>

<?php include 'includes/header.php'; ?>

<h2>Registrarse</h2>
<p>Por favor, completa este formulario para crear una cuenta.</p>
<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
    <!-- Nombre de Usuario -->
    <div class="mb-3">
        <label>Nombre de Usuario</label>
        <input type="text" name="nombre_usuario" class="form-control <?php echo (!empty($nombre_usuario_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $nombre_usuario; ?>">
        <span class="invalid-feedback"><?php echo $nombre_usuario_err; ?></span>
    </div>    
    <!-- Correo Electrónico -->
    <div class="mb-3">
        <label>Correo Electrónico</label>
        <input type="email" name="email" class="form-control <?php echo (!empty($email_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $email; ?>">
        <span class="invalid-feedback"><?php echo $email_err; ?></span>
    </div>
    <!-- Contraseña -->
    <div class="mb-3">
        <label>Contraseña</label>
        <input type="password" name="password" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $password; ?>">
        <span class="invalid-feedback"><?php echo $password_err; ?></span>
    </div>
    <!-- Confirmar Contraseña -->
    <div class="mb-3">
        <label>Confirmar Contraseña</label>
        <input type="password" name="confirm_password" class="form-control <?php echo (!empty($confirm_password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $confirm_password; ?>">
        <span class="invalid-feedback"><?php echo $confirm_password_err; ?></span>
    </div>
    <!-- Botón de Registro -->
    <div class="mb-3">
        <input type="submit" class="btn btn-custom" value="Registrarse">
        <input type="reset" class="btn btn-secondary ml-2" value="Resetear">
    </div>
    <p>¿Ya tienes una cuenta? <a href="login.php">Inicia sesión aquí</a>.</p>
</form>

<?php include 'includes/footer.php'; ?>
```

### 6. `login.php`

Página de inicio de sesión. Permite a los usuarios autenticarse en el sistema.

```php+HTML
<?php
session_start();
require_once 'includes/config.php';

// Verificar si el usuario ya está logueado, si es así, redirigir a dashboard
if (isset($_SESSION["id_usuario"]) && $_SESSION["id_usuario"] === true) {
    header("location: dashboard.php");
    exit;
}

// Inicializar variables
$nombre_usuario = $password = "";
$nombre_usuario_err = $password_err = $login_err = "";

// Procesar datos del formulario cuando se envía
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Verificar si el nombre de usuario está vacío
    if (empty(trim($_POST["nombre_usuario"]))) {
        $nombre_usuario_err = "Por favor, ingresa tu nombre de usuario.";
    } else {
        $nombre_usuario = trim($_POST["nombre_usuario"]);
    }

    // Verificar si la contraseña está vacía
    if (empty(trim($_POST["password"]))) {
        $password_err = "Por favor, ingresa tu contraseña.";
    } else {
        $password = trim($_POST["password"]);
    }

    // Validar credenciales
    if (empty($nombre_usuario_err) && empty($password_err)) {
        // Preparar una declaración SELECT
        $sql = "SELECT id_usuario, nombre_usuario, contraseña FROM Usuario WHERE nombre_usuario = ?";

        if ($stmt = $conn->prepare($sql)) {
            // Enlazar variables a la declaración preparada como parámetros
            $stmt->bind_param("s", $param_username);
            $param_username = $nombre_usuario;

            // Intentar ejecutar la declaración preparada
            if ($stmt->execute()) {
                // Almacenar el resultado
                $stmt->store_result();

                // Verificar si el nombre de usuario existe, si es así, verificar la contraseña
                if ($stmt->num_rows == 1) {
                    // Enlazar variables de resultado
                    $stmt->bind_result($id_usuario, $nombre_usuario_db, $hashed_password);
                    if ($stmt->fetch()) {
                        if (password_verify($password, $hashed_password)) {
                            // La contraseña es correcta, así que iniciar una nueva sesión
                            session_start();

                            // Almacenar datos en variables de sesión
                            $_SESSION["id_usuario"] = $id_usuario;
                            $_SESSION["nombre_usuario"] = $nombre_usuario_db;

                            // Registrar la conexión IP del usuario
                            require_once 'includes/conexionesip.php';
                            registrarConexion($conn, $id_usuario);

                            // Redirigir al usuario a la página del dashboard
                            header("location: dashboard.php");
                            exit();
                        } else {
                            // Contraseña no válida
                            $login_err = "Nombre de usuario o contraseña incorrectos.";
                        }
                    }
                } else {
                    // Nombre de usuario no existe
                    $login_err = "Nombre de usuario o contraseña incorrectos.";
                }
            } else {
                echo "Algo salió mal. Por favor, inténtalo de nuevo.";
            }

            $stmt->close();
        }
    }

    // Cerrar conexión
    $conn->close();
}
?>

<?php include 'includes/header.php'; ?>

<h2>Iniciar Sesión</h2>
<p>Por favor, completa tus credenciales para iniciar sesión.</p>

<?php 
if (!empty($login_err)) {
    echo '<div class="alert alert-danger">' . $login_err . '</div>';
}        
?>

<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
    <!-- Nombre de Usuario -->
    <div class="mb-3">
        <label>Nombre de Usuario</label>
        <input type="text" name="nombre_usuario" class="form-control <?php echo (!empty($nombre_usuario_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $nombre_usuario; ?>">
        <span class="invalid-feedback"><?php echo $nombre_usuario_err; ?></span>
    </div>    
    <!-- Contraseña -->
    <div class="mb-3">
        <label>Contraseña</label>
        <input type="password" name="password" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>">
        <span class="invalid-feedback"><?php echo $password_err; ?></span>
    </div>
    <!-- Botón de Iniciar Sesión -->
    <div class="mb-3">
        <input type="submit" class="btn btn-custom" value="Iniciar Sesión">
    </div>
    <p>¿No tienes una cuenta? <a href="register.php">Regístrate aquí</a>.</p>
</form>

<?php include 'includes/footer.php'; ?>

```

### 7. `dashboard.php`

Página protegida que solo pueden acceder usuarios autenticados. Muestra información básica del usuario.

```php+HTML
<?php
// dashboard.php
session_start(); // Iniciar la sesión para acceder a las variables de sesión

require_once 'includes/config.php'; // Incluir la configuración de la base de datos

// Verificar si el usuario está logueado
if (!isset($_SESSION["id_usuario"])) {
    // Redirigir al usuario a la página de inicio de sesión si no está logueado
    header("location: login.php");
    exit;
}

// Obtener los datos del usuario desde la base de datos
$id_usuario = $_SESSION["id_usuario"];
$sql = "SELECT nombre_usuario, email FROM Usuario WHERE id_usuario = ?";
if ($stmt = $conn->prepare($sql)) {
    $stmt->bind_param("i", $id_usuario); // Enlazar el ID del usuario a la consulta
    $stmt->execute();
    $stmt->bind_result($nombre_usuario, $email);
    $stmt->fetch();
    $stmt->close();
} else {
    echo "Error al preparar la consulta.";
    exit;
}

// Obtener las conexiones del usuario desde la base de datos
$sql_conexiones = "SELECT fecha_conexion, ip_conexion, tiempo_conexion FROM Conexión WHERE id_usuario = ? ORDER BY fecha_conexion DESC";
$conexiones = [];
if ($stmt = $conn->prepare($sql_conexiones)) {
    $stmt->bind_param("i", $id_usuario);
    $stmt->execute();
    $result = $stmt->get_result();
    while ($row = $result->fetch_assoc()) {
        $conexiones[] = $row;
    }
    $stmt->close();
} else {
    echo "Error al preparar la consulta de conexiones.";
    exit;
}

?>

<?php include 'includes/header.php'; ?>

<div class="container mt-5">
    <h2>Dashboard</h2>
    <p>Bienvenido, <strong><?php echo htmlspecialchars($nombre_usuario); ?></strong>!</p>
    <p>Tu correo electrónico es: <strong><?php echo htmlspecialchars($email); ?></strong></p>

    <h3>Historial de Conexiones</h3>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Fecha de Conexión</th>
                <th>IP de Conexión</th>
                <th>Duración de la Conexión (segundos)</th>
            </tr>
        </thead>
        <tbody>
            <?php if (!empty($conexiones)): ?>
                <?php foreach ($conexiones as $conexion): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($conexion['fecha_conexion']); ?></td>
                        <td><?php echo htmlspecialchars($conexion['ip_conexion']); ?></td>
                        <td><?php echo htmlspecialchars($conexion['tiempo_conexion']); ?></td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="3">No se encontraron registros de conexión.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

<?php include 'includes/footer.php'; ?>


```

### 8. `logout.php`

Script para cerrar sesión y redirigir al usuario a la página de inicio de sesión.

```php+HTML
<?php
// logout.php
session_start();

// Destruir todas las variables de sesión
$_SESSION = array();

// Destruir la sesión
session_destroy();

// Redirigir al usuario a la página de inicio de sesión
header("location: login.php");
exit;
?>
```