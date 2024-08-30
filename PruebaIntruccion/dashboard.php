<?php
// dashboard.php
session_start();

// Verificar si el usuario está logueado, si no, redirigir a la página de inicio de sesión
if (!isset($_SESSION["id_usuario"]) || $_SESSION["id_usuario"] !== true) {
    header("location: login.php");
    exit;
}
?>

<?php include 'includes/header.php'; ?>

<h2>Dashboard</h2>
<p>Bienvenido, <strong><?php echo htmlspecialchars($_SESSION["nombre_usuario"]); ?></strong>!</p>
<p>Tu correo electrónico es: <strong><?php echo htmlspecialchars($_SESSION["email"]); ?></strong></p>

<?php include 'includes/footer.php'; ?>
