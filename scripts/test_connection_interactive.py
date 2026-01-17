#!/usr/bin/env python3
"""Script interactivo para probar conectividad con Raspberry Pi."""

import sys
import subprocess
import socket
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_ssh_connection(host: str, user: str = "picamara") -> bool:
    """Prueba conexión SSH."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=3", "-o", "StrictHostKeyChecking=no",
             f"{user}@{host}", "echo 'OK'"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0 and "OK" in result.stdout
    except:
        return False


def find_common_ips() -> list:
    """Genera lista de IPs comunes para probar."""
    # Obtener IP local para determinar rango
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Extraer primeros 3 octetos
        base = ".".join(local_ip.split(".")[:-1])
        return [f"{base}.{i}" for i in range(1, 255) if i != int(local_ip.split(".")[-1])]
    except:
        return [f"192.168.1.{i}" for i in range(1, 255)]


def main():
    """Función principal interactiva."""
    print("=" * 60)
    print("🔍 BÚSQUEDA Y PRUEBA DE RASPBERRY PI")
    print("=" * 60)
    print()
    
    # Opción 1: IP manual
    print("Opción 1: Proporcionar IP manualmente")
    ip_manual = input("   Ingresa la IP de tu Raspberry Pi (o Enter para buscar): ").strip()
    
    if ip_manual:
        print(f"\n🧪 Probando con IP: {ip_manual}")
        if test_ssh_connection(ip_manual):
            print(f"✅ Conexión SSH exitosa a {ip_manual}")
            print(f"\n🚀 Ejecutando pruebas completas...")
            subprocess.run([
                sys.executable,
                "scripts/test_raspberry_connection.py",
                "--host", ip_manual,
                "--user", "picamara"
            ])
            return
        else:
            print(f"❌ No se pudo conectar a {ip_manual}")
            return
    
    # Opción 2: Buscar automáticamente
    print("\nOpción 2: Buscar automáticamente en la red local")
    print("   Esto puede tardar unos minutos...")
    respuesta = input("   ¿Deseas continuar? (s/n): ").strip().lower()
    
    if respuesta != 's':
        print("\n💡 Para probar manualmente:")
        print("   python scripts/test_raspberry_connection.py --host <IP> --user picamara")
        return
    
    print("\n🔍 Escaneando red local (esto puede tardar)...")
    print("   Probando IPs comunes...")
    
    # Probar algunas IPs comunes primero
    common_ips = [
        "192.168.1.100", "192.168.1.101", "192.168.1.102",
        "192.168.0.100", "192.168.0.101", "192.168.0.102",
        "raspberrypi.local"
    ]
    
    found = False
    for ip in common_ips:
        print(f"   Probando {ip}...", end="\r")
        if test_ssh_connection(ip):
            print(f"\n✅ ¡Encontrada! IP: {ip}")
            found = True
            print(f"\n🚀 Ejecutando pruebas completas...")
            subprocess.run([
                sys.executable,
                "scripts/test_raspberry_connection.py",
                "--host", ip,
                "--user", "picamara"
            ])
            break
    
    if not found:
        print("\n❌ No se encontró automáticamente.")
        print("\n💡 Opciones:")
        print("   1. Obtén la IP desde la Raspberry Pi: hostname -I")
        print("   2. O desde tu router (buscar dispositivo 'raspberrypi')")
        print("   3. Luego ejecuta:")
        print("      python scripts/test_raspberry_connection.py --host <IP> --user picamara")


if __name__ == "__main__":
    main()
