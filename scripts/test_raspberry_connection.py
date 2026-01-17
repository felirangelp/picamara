#!/usr/bin/env python3
"""Script de prueba para verificar conectividad con Raspberry Pi y cámara.

Este script verifica:
1. Conexión SSH a Raspberry Pi
2. Detección de cámara IMX219
3. Funcionamiento básico de picamera2
4. Captura de frames de prueba
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_ssh_connection(host: str, user: str = "pi") -> bool:
    """Prueba conexión SSH a Raspberry Pi.
    
    Args:
        host: IP o hostname de la Raspberry Pi.
        user: Usuario SSH (default: pi).
        
    Returns:
        True si la conexión es exitosa.
    """
    print(f"\n{'='*60}")
    print("🔌 Probando conexión SSH...")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no",
             f"{user}@{host}", "echo 'SSH connection successful'"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ Conexión SSH exitosa a {user}@{host}")
            print(f"   Respuesta: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error en conexión SSH: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout al conectar a {host}")
        return False
    except FileNotFoundError:
        print("❌ Comando 'ssh' no encontrado. ¿Está instalado?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_camera_detection(host: str, user: str = "pi") -> bool:
    """Prueba detección de cámara en Raspberry Pi.
    
    Args:
        host: IP o hostname de la Raspberry Pi.
        user: Usuario SSH.
        
    Returns:
        True si la cámara es detectada.
    """
    print(f"\n{'='*60}")
    print("📷 Probando detección de cámara...")
    print(f"{'='*60}")
    
    try:
        # Verificar que libcamera esté disponible
        result = subprocess.run(
            ["ssh", f"{user}@{host}", "libcamera-hello --list-cameras"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            output = result.stdout
            if "imx219" in output.lower() or "camera" in output.lower():
                print("✅ Cámara detectada:")
                print(output)
                return True
            else:
                print("⚠️  libcamera responde pero no se detecta IMX219")
                print(f"   Salida: {output}")
                return False
        else:
            print(f"❌ Error al detectar cámara: {result.stderr}")
            print("\n💡 Sugerencias:")
            print("   1. Verificar que la cámara esté conectada físicamente")
            print("   2. Ejecutar: sudo raspi-config → Interface Options → Camera → Enable")
            print("   3. Reiniciar la Raspberry Pi después de habilitar la cámara")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_picamera2_import(host: str, user: str = "pi", project_path: str = "~/Pi_camara") -> bool:
    """Prueba importación de picamera2 en Raspberry Pi.
    
    Args:
        host: IP o hostname de la Raspberry Pi.
        user: Usuario SSH.
        project_path: Ruta al proyecto en la Raspberry Pi.
        
    Returns:
        True si picamera2 puede importarse.
    """
    print(f"\n{'='*60}")
    print("🐍 Probando importación de picamera2...")
    print(f"{'='*60}")
    
    try:
        # Activar venv y probar import
        command = f"""
        cd {project_path} && \
        source venv/bin/activate 2>/dev/null && \
        python3 -c "import picamera2; print('picamera2 OK')" 2>&1
        """
        
        result = subprocess.run(
            ["ssh", f"{user}@{host}", command],
            capture_output=True,
            text=True,
            timeout=15,
            shell=False
        )
        
        if "picamera2 OK" in result.stdout:
            print("✅ picamera2 importado correctamente")
            return True
        else:
            print(f"❌ Error al importar picamera2:")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            print("\n💡 Sugerencias:")
            print("   1. Instalar: sudo apt install python3-picamera2")
            print("   2. Verificar que el venv esté activado")
            print("   3. Verificar que el proyecto esté en la ruta correcta")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_camera_capture(host: str, user: str = "pi", project_path: str = "~/Pi_camara") -> bool:
    """Prueba captura de frame de la cámara.
    
    Args:
        host: IP o hostname de la Raspberry Pi.
        user: Usuario SSH.
        project_path: Ruta al proyecto en la Raspberry Pi.
        
    Returns:
        True si la captura es exitosa.
    """
    print(f"\n{'='*60}")
    print("📸 Probando captura de frame...")
    print(f"{'='*60}")
    
    try:
        # Script de prueba simple
        test_script = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / 'Pi_camara' / 'src'))

try:
    from camera.imx219_handler import IMX219Handler
    import time
    
    print("Inicializando cámara...")
    camera = IMX219Handler()
    camera.start()
    time.sleep(2)  # Calentamiento
    
    print("Capturando frame...")
    frame = camera.capture_frame()
    
    if frame is not None:
        print(f"✅ Frame capturado: shape={frame.shape}, dtype={frame.dtype}")
        camera.stop()
        return True
    else:
        print("❌ No se pudo capturar frame")
        camera.stop()
        return False
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    return False
"""
        
        command = f"""
        cd {project_path} && \
        source venv/bin/activate 2>/dev/null && \
        python3 << 'PYTHON_SCRIPT'
{test_script}
PYTHON_SCRIPT
        """
        
        result = subprocess.run(
            ["ssh", f"{user}@{host}", command],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )
        
        output = result.stdout + result.stderr
        
        if "Frame capturado" in output and "shape" in output:
            print("✅ Captura de frame exitosa")
            print(f"   Detalles: {[line for line in output.split(chr(10)) if 'Frame capturado' in line or 'shape' in line]}")
            return True
        else:
            print(f"❌ Error en captura de frame:")
            print(output)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_web_server(host: str, port: int = 5000) -> bool:
    """Prueba si el servidor web está corriendo.
    
    Args:
        host: IP o hostname de la Raspberry Pi.
        port: Puerto del servidor web.
        
    Returns:
        True si el servidor responde.
    """
    print(f"\n{'='*60}")
    print("🌐 Probando servidor web...")
    print(f"{'='*60}")
    
    try:
        import urllib.request
        import urllib.error
        
        url = f"http://{host}:{port}/api/status"
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ Servidor web respondiendo en http://{host}:{port}")
                    return True
                else:
                    print(f"⚠️  Servidor responde con código: {response.status}")
                    return False
        except urllib.error.URLError as e:
            print(f"❌ No se puede conectar al servidor web: {e}")
            print(f"   URL probada: {url}")
            print("\n💡 Sugerencias:")
            print("   1. Verificar que el servidor esté corriendo: python src/main.py")
            print("   2. Verificar que el puerto no esté bloqueado por firewall")
            print("   3. Verificar que la IP sea correcta")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Función principal del script de prueba."""
    parser = argparse.ArgumentParser(
        description="Prueba conectividad con Raspberry Pi y cámara"
    )
    parser.add_argument(
        "--host",
        type=str,
        required=True,
        help="IP o hostname de la Raspberry Pi"
    )
    parser.add_argument(
        "--user",
        type=str,
        default="pi",
        help="Usuario SSH (default: pi)"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default="~/Pi_camara",
        help="Ruta al proyecto en Raspberry Pi (default: ~/Pi_camara)"
    )
    parser.add_argument(
        "--skip-ssh",
        action="store_true",
        help="Saltar prueba de SSH (si ya estás en la Pi)"
    )
    parser.add_argument(
        "--skip-web",
        action="store_true",
        help="Saltar prueba de servidor web"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧪 PRUEBAS DE CONECTIVIDAD - RASPBERRY PI Y CÁMARA")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Usuario: {args.user}")
    print(f"Ruta proyecto: {args.project_path}")
    print("=" * 60)
    
    results = {}
    
    # Prueba 1: SSH
    if not args.skip_ssh:
        results['ssh'] = test_ssh_connection(args.host, args.user)
        if not results['ssh']:
            print("\n⚠️  Sin conexión SSH, no se pueden ejecutar más pruebas remotas.")
            print("   Usa --skip-ssh si estás ejecutando esto directamente en la Raspberry Pi.")
            return
    else:
        results['ssh'] = True
        print("\n⏭️  Saltando prueba SSH (--skip-ssh)")
    
    # Prueba 2: Detección de cámara
    if not args.skip_ssh:
        results['camera_detection'] = test_camera_detection(args.host, args.user)
    else:
        # Si estamos en la Pi, probar localmente
        try:
            result = subprocess.run(
                ["libcamera-hello", "--list-cameras"],
                capture_output=True,
                text=True,
                timeout=15
            )
            results['camera_detection'] = result.returncode == 0 and "imx219" in result.stdout.lower()
            if results['camera_detection']:
                print("✅ Cámara detectada localmente")
            else:
                print("❌ Cámara no detectada localmente")
        except:
            results['camera_detection'] = False
    
    # Prueba 3: picamera2
    if not args.skip_ssh:
        results['picamera2'] = test_picamera2_import(args.host, args.user, args.project_path)
    else:
        try:
            import picamera2
            results['picamera2'] = True
            print("✅ picamera2 disponible localmente")
        except ImportError:
            results['picamera2'] = False
            print("❌ picamera2 no disponible localmente")
    
    # Prueba 4: Captura de frame
    if results.get('picamera2'):
        if not args.skip_ssh:
            results['capture'] = test_camera_capture(args.host, args.user, args.project_path)
        else:
            # Probar localmente
            try:
                from src.camera.imx219_handler import IMX219Handler
                import time
                camera = IMX219Handler()
                camera.start()
                time.sleep(2)
                frame = camera.capture_frame()
                if frame is not None:
                    print(f"✅ Frame capturado localmente: shape={frame.shape}")
                    results['capture'] = True
                else:
                    results['capture'] = False
                camera.stop()
            except Exception as e:
                print(f"❌ Error en captura local: {e}")
                results['capture'] = False
    
    # Prueba 5: Servidor web
    if not args.skip_web:
        results['web'] = test_web_server(args.host)
    else:
        print("\n⏭️  Saltando prueba de servidor web (--skip-web)")
    
    # Resumen
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE PRUEBAS")
    print(f"{'='*60}")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print(f"\n🎉 ¡Todas las pruebas pasaron!")
    else:
        print(f"\n⚠️  Algunas pruebas fallaron. Revisa los mensajes arriba.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
