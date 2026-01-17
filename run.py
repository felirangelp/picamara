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
import os
from pathlib import Path

# Obtener el directorio raíz del proyecto de forma absoluta
project_root = Path(__file__).resolve().parent
project_root_str = str(project_root)

# CRÍTICO: Cambiar al directorio del proyecto ANTES de cualquier import
# Esto asegura que los imports relativos funcionen correctamente
os.chdir(project_root_str)

# CRÍTICO: Agregar el directorio raíz al principio de sys.path
# Esto permite que los imports absolutos con 'src.' funcionen
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
sys.path.insert(0, project_root_str)

# Verificar que el path esté configurado correctamente
if sys.path[0] != project_root_str:
    # Forzar que esté al principio
    if project_root_str in sys.path:
        sys.path.remove(project_root_str)
    sys.path.insert(0, project_root_str)

# Configurar el entorno del sistema (picamera2, libcamera)
# Importar desde src.config_env después de agregar project_root al path
try:
    from src.config_env import configure_system_paths
    configure_system_paths()
except ImportError as e:
    print(f"Warning: No se pudo importar config_env: {e}", file=sys.stderr)

# Verificar que src.data existe antes de importar main
src_data_path = project_root / "src" / "data"
if not src_data_path.exists():
    print(f"ERROR: No se encuentra src/data en {src_data_path}", file=sys.stderr)
    sys.exit(1)

# Verificar que src.data/__init__.py existe
if not (src_data_path / "__init__.py").exists():
    print(f"ERROR: No se encuentra src/data/__init__.py", file=sys.stderr)
    sys.exit(1)

# Ejecutar el módulo principal
if __name__ == "__main__":
    try:
        from src.main import main
        main()
    except ImportError as e:
        print(f"ERROR de importación: {e}", file=sys.stderr)
        print(f"sys.path[0]: {sys.path[0]}", file=sys.stderr)
        print(f"Directorio actual: {os.getcwd()}", file=sys.stderr)
        print(f"src/data existe: {src_data_path.exists()}", file=sys.stderr)
        raise
