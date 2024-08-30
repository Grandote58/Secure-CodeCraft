<?php
// login.php
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
        $sql = "SELECT id_usuario, nombre_usuario, email, contraseña, estado FROM Usuario WHERE nombre_usuario = ?";

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
                    $stmt->bind_result($id_usuario, $nombre_usuario_db, $email, $hashed_password, $estado);
                    if ($stmt->fetch()) {
                        if ($estado != 'activo') {
                            $login_err = "Tu cuenta está inactiva. Por favor, contacta al administrador.";
                        } elseif (password_verify($password, $hashed_password)) {
                            // La contraseña es correcta, así que iniciar una nueva sesión
                            session_start();

                            // Almacenar datos en variables de sesión
                            $_SESSION["id_usuario"] = $id_usuario;
                            $_SESSION["nombre_usuario"] = $nombre_usuario_db;
                            $_SESSION["email"] = $email;

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
