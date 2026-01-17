"""
Configuración de entorno para el proyecto Pi Camera Security System.

Este módulo maneja la configuración del PYTHONPATH necesaria para acceder
a módulos del sistema como picamera2 y libcamera que no están disponibles
en pip pero son requeridos en Raspberry Pi.

Siguiendo los principios de AI-DLC:
- Gobernanza: Centraliza la configuración de paths del sistema
- Reproducibilidad: Funciona en cualquier Raspberry Pi con los paquetes del sistema
- Mantenibilidad: Documentado y fácil de modificar
"""

import sys
import os
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)

# Paths del sistema donde se encuentran los módulos de Raspberry Pi
# IMPORTANTE: Los paths del sistema deben ir AL FINAL para no interferir
# con las dependencias del venv, EXCEPTO para módulos específicos de hardware
SYSTEM_PYTHON_PATHS = [
    "/usr/lib/python3/dist-packages",  # Debian/Raspbian estándar
    "/usr/local/lib/python3/dist-packages",  # Instalaciones locales
]


def configure_system_paths() -> None:
    """
    Configura el PYTHONPATH para incluir módulos del sistema necesarios.
    
    Esta función debe ser llamada al inicio de la aplicación antes de
    importar picamera2 u otros módulos específicos de Raspberry Pi.
    
    IMPORTANTE: Los paths del sistema se agregan AL FINAL del sys.path
    para evitar conflictos con las dependencias del venv. Solo se usan
    para módulos que no están disponibles en pip (picamera2, libcamera).
    
    Returns:
        None
    
    Raises:
        None (falla silenciosamente si los paths no existen)
    """
    paths_added = []
    
    for system_path in SYSTEM_PYTHON_PATHS:
        if os.path.exists(system_path) and system_path not in sys.path:
            # Agregar AL FINAL para no interferir con el venv
            sys.path.append(system_path)
            paths_added.append(system_path)
            logger.debug(f"Added system path: {system_path}")
    
    if paths_added:
        logger.info(f"Configured {len(paths_added)} system Python paths")
    else:
        logger.warning("No system Python paths were added (may not be running on Raspberry Pi)")


def verify_system_dependencies() -> dict:
    """
    Verifica la disponibilidad de dependencias críticas del sistema.
    
    Returns:
        dict: Diccionario con el estado de cada dependencia
              {"module_name": {"available": bool, "version": str, "error": str}}
    """
    dependencies = {}
    
    # Verificar picamera2
    try:
        import picamera2
        dependencies["picamera2"] = {
            "available": True,
            "version": getattr(picamera2, "__version__", "unknown"),
            "error": None
        }
    except ImportError as e:
        dependencies["picamera2"] = {
            "available": False,
            "version": None,
            "error": str(e)
        }
    
    # Verificar libcamera
    try:
        import libcamera
        dependencies["libcamera"] = {
            "available": True,
            "version": "OK",
            "error": None
        }
    except ImportError as e:
        dependencies["libcamera"] = {
            "available": False,
            "version": None,
            "error": str(e)
        }
    
    # Verificar numpy
    try:
        import numpy
        dependencies["numpy"] = {
            "available": True,
            "version": numpy.__version__,
            "error": None
        }
    except ImportError as e:
        dependencies["numpy"] = {
            "available": False,
            "version": None,
            "error": str(e)
        }
    
    # Verificar opencv
    try:
        import cv2
        dependencies["opencv"] = {
            "available": True,
            "version": cv2.__version__,
            "error": None
        }
    except ImportError as e:
        dependencies["opencv"] = {
            "available": False,
            "version": None,
            "error": str(e)
        }
    
    return dependencies


def print_system_info() -> None:
    """
    Imprime información del sistema y dependencias para diagnóstico.
    """
    print("\n" + "="*70)
    print("SISTEMA DE CÁMARA - INFORMACIÓN DE DIAGNÓSTICO")
    print("="*70)
    
    print(f"\nPython Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    print(f"\nPython Path (primeros 5):")
    for i, path in enumerate(sys.path[:5], 1):
        print(f"  {i}. {path}")
    
    print(f"\nDependencias del Sistema:")
    deps = verify_system_dependencies()
    for name, info in deps.items():
        status = "✅" if info["available"] else "❌"
        version = f"v{info['version']}" if info['version'] else "N/A"
        print(f"  {status} {name}: {version}")
        if info["error"]:
            print(f"      Error: {info['error']}")
    
    print("="*70 + "\n")


# Auto-configuración al importar el módulo
configure_system_paths()

if __name__ == "__main__":
    # Para pruebas y diagnóstico
    logging.basicConfig(level=logging.INFO)
    print_system_info()
