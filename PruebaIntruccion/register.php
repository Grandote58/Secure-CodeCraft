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
