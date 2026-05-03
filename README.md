# **FTP Brute Force Pro - Documentación y Uso**

---

## **📌 Descripción General**
Este script en Python realiza **ataques de fuerza bruta** contra servidores FTP de manera **multihilo**, optimizando el proceso para evitar tiempos de espera excesivos. Utiliza la librería estándar `ftplib` junto con `concurrent.futures` para manejar **múltiples conexiones simultáneas**, lo que lo hace **eficiente y profesional** para pruebas de penetración éticas.

⚠️ **⚠️ Advertencia:**
Este script **solo debe usarse en entornos donde tengas permiso explícito** para realizar pruebas de seguridad. El acceso no autorizado a sistemas FTP es **ilegal** y puede tener consecuencias legales graves.

---

## **⚙️ Características Clave (¿Por qué es un script "Nivel Pro"?)**

### **1️⃣ Multihilo (`ThreadPoolExecutor`)**
- **Problema:** El protocolo FTP es lento debido a su naturaleza secuencial (cada conexión requiere un "handshake").
- **Solución:** El script usa **hilos concurrentes** (por defecto, 10) para probar múltiples contraseñas **simultáneamente**.
  - Ejemplo: Probar **1,000 contraseñas** con **10 hilos** es **10 veces más rápido** que hacerlo secuencialmente.

### **2️⃣ Manejo Avanzado de Excepciones**
- **`ftplib.error_perm`:** Detecta errores de autenticación (usuario/contraseña incorrectos) y los ignora para continuar con el siguiente intento.
- **Excepciones genéricas:** Captura errores de red (como timeouts o conexiones caídas) para evitar que el script se detenga inesperadamente.

### **3️⃣ Control de Timeouts**
- **`timeout=5`:** Evita que el script se quede "colgado" esperando una respuesta del servidor FTP.
- **Beneficio:** Si el servidor no responde en 5 segundos, el script **libera la conexión** y sigue con el siguiente intento.

### **4️⃣ Interfaz de Progreso (`tqdm`)**
- **`tqdm`:** Muestra una **barra de progreso** en tiempo real, actualizando el estado de los intentos.
- **Salida limpia:** Usa `progress_bar.write()` para que los mensajes de éxito **no rompan la visualización** de la barra de progreso.

### **5️⃣ Argumentos Personalizables**
- **`--threads`:** Permite ajustar el número de hilos concurrentes (útil para servidores con restricciones).
- **Soporte para listas de contraseñas:** Lee un archivo de diccionario (`wordlist`) con contraseñas a probar.

---

## **🚀 Instalación y Requisitos**

### **1️⃣ Dependencias**
Instala las librerías necesarias con:
```bash
pip install ftplib tqdm
```
*(Nota: `ftplib` ya viene incluido en Python estándar, pero `tqdm` es opcional para la barra de progreso.)*

---

## **📝 Uso del Script**

### **1️⃣ Sintaxis Básica**
```bash
python ftp_brute_force.py <host> <usuario> <wordlist> [--threads <número>]
```

### **2️⃣ Parámetros**
| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `host` | IP o dominio del servidor FTP | `192.168.1.100` |
| `user` | Nombre de usuario a atacar | `admin` |
| `wordlist` | Ruta al archivo de contraseñas | `passwords.txt` |
| `--threads` | Número de hilos concurrentes (opcional) | `--threads 20` |

### **3️⃣ Ejemplo de Ejecución**
```bash
python ftp_brute_force.py 10.0.0.5 admin rockyou.txt --threads 15
```
- **Resultado:**
  ```
  [*] Iniciando ataque contra 10.0.0.5 para el usuario 'admin'
  [*] Probando 14344396 contraseñas con 15 hilos...
  Progreso: 100%|████████████████████| 14344396/14344396 [01:23<00:00, 172234.56pwd/s]
  [+] ¡ÉXITO! Usuario: admin | Contraseña: password123
  ```

---

## **⚠️ Consideraciones de Seguridad**

### **1️⃣ Bloqueo de IP (Fail2Ban)**
- **Problema:** La mayoría de servidores FTP modernos (como **vsftpd** o **ProFTPD**) usan **Fail2Ban** para bloquear IPs tras **3-5 intentos fallidos**.
- **Solución:**
  - Usa **proxies** o **VPNs** para rotar tu IP.
  - Configura un **delay entre intentos** (ej: `time.sleep(1)`).

### **2️⃣ Uso Ético**
- **✅ Legal:** Solo para **pruebas autorizadas** (ej: auditorías de seguridad, CTFs).
- **❌ Ilegal:** Acceder a servidores sin permiso puede ser considerado **delito informático** (ej: Art. 197 del Código Penal en España, **Computer Fraud and Abuse Act** en EE.UU.).

### **3️⃣ Alternativas Más Efectivas**
Si el servidor FTP tiene protecciones, considera:
- **Ataques de diccionario con credenciales conocidas** (ej: contraseñas por defecto como `admin:admin`).
- **Explotación de vulnerabilidades** (ej: **CVE-2021-41773** en Apache).

---

## **📂 Estructura del Proyecto**

```
ftp_brute_force/
│── ftp_brute_force.py   # Script principal
│── passwords.txt        # Ejemplo de wordlist (puedes usar rockyou.txt)
│── README.md            # Este archivo
```

---

## **🔧 Personalización Avanzada**

### **1️⃣ Detener el Script al Encontrar una Contraseña**
Modifica el bucle en `main()` para detener el `ThreadPoolExecutor` al primer éxito:
```python
for pwd in passwords:
    future = executor.submit(connect_ftp, args.host, args.user, pwd, bar)
    if connect_ftp(args.host, args.user, pwd, bar):  # Si hay éxito
        executor.shutdown(wait=False)  # Detiene todos los hilos
        break
```

### **2️⃣ Añadir un Delay Entre Intentos**
Evita bloqueos por Fail2Ban:
```python
import time

def connect_ftp(host, user, password, progress_bar):
    time.sleep(1)  # Espera 1 segundo entre intentos
    # ... (resto del código)
```

### **3️⃣ Guardar Resultados en un Archivo**
```python
with open("resultados.txt", "a") as f:
    f.write(f"[+] Éxito: {user}:{password}\n")
```

---

## **📚 Recursos Útiles**
- **Wordlists:**
  - [rockyou.txt](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Leaked-Databases/rockyou.txt) (común en pruebas de penetración).
  - [SecLists](https://github.com/danielmiessler/SecLists) (colección de diccionarios).
- **Herramientas Alternativas:**
  - **Hydra** (`hydra -l admin -P passwords.txt ftp://192.168.1.100`).
  - **Medusa** (`medusa -h 192.168.1.100 -u admin -P passwords.txt -M ftp`).


---
## **📜 Licencia**
Este script se proporciona **solo para fines educativos**. No nos hacemos responsables del uso indebido del código.

---
**🔐 Recuerda:** La seguridad informática es un **juego limpio**. Siempre obtén **permiso explícito** antes de probar sistemas ajenos. 🚀
