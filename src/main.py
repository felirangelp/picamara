"""Punto de entrada principal del sistema de seguridad.

Este módulo inicializa y ejecuta el servidor FastAPI con todos los componentes
integrados (cámara, detección, base de datos, almacenamiento).

Siguiendo los principios de AI-DLC:
- Configuración de entorno antes de cualquier import
- Validación de dependencias del sistema
- Logging estructurado para diagnóstico
"""

# IMPORTANTE: Configurar el entorno ANTES de cualquier otro import
# Esto permite acceso a picamera2 y libcamera del sistema
from src.config_env import configure_system_paths, verify_system_dependencies, print_system_info
configure_system_paths()

import argparse
import logging
import signal
import sys
from pathlib import Path

from src.web.camera_server import CameraServer


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/system.log')
    ]
)

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """Configura el nivel de logging.
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    logging.getLogger().setLevel(numeric_level)
    logger.info(f"Logging configurado en nivel: {log_level}")


def create_directories() -> None:
    """Crea los directorios necesarios si no existen."""
    directories = [
        'data/videos',
        'data/episodes',
        'data/models',
        'logs',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.debug("Directorios creados/verificados")


def signal_handler(sig: int, frame) -> None:
    """Maneja señales de terminación.
    
    Args:
        sig: Número de señal.
        frame: Frame actual.
    """
    logger.info(f"Señal {sig} recibida, deteniendo sistema...")
    sys.exit(0)


def main() -> None:
    """Función principal del sistema."""
    parser = argparse.ArgumentParser(
        description='Sistema de Seguridad Inteligente con Raspberry Pi'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host del servidor (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Puerto del servidor (default: 5000)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/camera_config.yaml',
        help='Ruta al archivo de configuración (default: config/camera_config.yaml)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Nivel de logging (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    setup_logging(args.log_level)
    
    # Crear directorios
    create_directories()
    
    # Configurar manejadores de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("=" * 60)
    logger.info("Sistema de Seguridad Inteligente - Iniciando")
    logger.info("=" * 60)
    logger.info(f"Host: {args.host}")
    logger.info(f"Puerto: {args.port}")
    logger.info(f"Configuración: {args.config}")
    
    try:
        # Crear e iniciar servidor
        server = CameraServer(
            config_path=args.config,
            host=args.host,
            port=args.port
        )
        
        # Ejecutar servidor
        server.run()
    
    except KeyboardInterrupt:
        logger.info("Interrupción por teclado recibida")
    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Sistema detenido")


if __name__ == "__main__":
    main()
