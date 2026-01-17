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

# Obtener el directorio raíz del proyecto
project_root = Path(__file__).parent.absolute()
project_root_str = str(project_root)

# Cambiar al directorio del proyecto (importante para imports relativos)
os.chdir(project_root_str)

# Agregar el directorio raíz del proyecto al PYTHONPATH
# Esto permite que los imports absolutos con 'src.' funcionen
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)
elif sys.path[0] != project_root_str:
    # Si está pero no al principio, moverlo al principio
    sys.path.remove(project_root_str)
    sys.path.insert(0, project_root_str)

# Configurar el entorno del sistema (picamera2, libcamera)
# Importar desde src.config_env después de agregar project_root al path
from src.config_env import configure_system_paths
configure_system_paths()

# Ejecutar el módulo principal
if __name__ == "__main__":
    from src.main import main
    main()
