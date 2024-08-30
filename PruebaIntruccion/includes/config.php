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
