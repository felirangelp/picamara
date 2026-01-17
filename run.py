#!/usr/bin/env python3
"""
Script de inicio para el Sistema de Seguridad con Cámara.

Este script configura el entorno correctamente y ejecuta el sistema
como un módulo Python, resolviendo problemas de imports relativos.

Siguiendo los principios de AI-DLC:
- Punto de entrada único y claro
- Configuración de entorno centralizada
- Manejo robusto de errores
"""

import sys
from pathlib import Path

# Agregar el directorio src al PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Configurar el entorno del sistema (picamera2, libcamera)
from config_env import configure_system_paths
configure_system_paths()

# Ejecutar el módulo principal
if __name__ == "__main__":
    from main import main
    main()
