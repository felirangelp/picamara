"""Manejador para cámara IMX219 en Raspberry Pi 4.

Este módulo proporciona una interfaz para capturar frames de video
desde la cámara IMX219 usando picamera2.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import yaml
import numpy as np

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None
    logging.warning("picamera2 no disponible. El sistema no funcionará sin hardware Raspberry Pi.")


logger = logging.getLogger(__name__)


class IMX219Handler:
    """Manejador de cámara IMX219 usando picamera2.
    
    Esta clase encapsula la configuración y operación de la cámara IMX219,
    proporcionando una interfaz simple para capturar frames de video.
    
    Attributes:
        camera: Instancia de Picamera2.
        config: Diccionario con configuración cargada desde YAML.
        is_running: Indica si la cámara está activa.
    """
    
    def __init__(self, config_path: str = "config/camera_config.yaml") -> None:
        """Inicializa el manejador de cámara.
        
        Args:
            config_path: Ruta al archivo de configuración YAML.
            
        Raises:
            FileNotFoundError: Si el archivo de configuración no existe.
            ValueError: Si picamera2 no está disponible.
        """
        if Picamera2 is None:
            raise ValueError(
                "picamera2 no está disponible. "
                "Este módulo requiere hardware Raspberry Pi con cámara."
            )
        
        self.config = self._load_config(config_path)
        self.camera: Optional[Picamera2] = None
        self.is_running: bool = False
        
        logger.info("IMX219Handler inicializado")
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """Carga configuración desde archivo YAML.
        
        Args:
            path: Ruta al archivo YAML.
            
        Returns:
            Diccionario con configuración.
            
        Raises:
            FileNotFoundError: Si el archivo no existe.
            yaml.YAMLError: Si el archivo YAML es inválido.
        """
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {path}")
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.debug(f"Configuración cargada desde {path}")
            return config
        except yaml.YAMLError as e:
            logger.error(f"Error parseando YAML: {e}")
            raise
    
    def _configure_camera(self) -> None:
        """Configura la cámara según los parámetros del archivo de configuración.
        
        Raises:
            RuntimeError: Si hay error configurando la cámara.
        """
        if self.camera is None:
            raise RuntimeError("Cámara no inicializada")
        
        cam_config = self.config.get('camera', {})
        resolution = cam_config.get('resolution', {})
        width = resolution.get('width', 1920)
        height = resolution.get('height', 1080)
        framerate = cam_config.get('framerate', 30)
        format_str = cam_config.get('format', 'RGB888')
        
        try:
            self.camera.configure(
                self.camera.create_preview_configuration(
                    main={
                        "size": (width, height),
                        "format": format_str
                    },
                    controls={"FrameRate": framerate}
                )
            )
            logger.info(
                f"Cámara configurada: {width}x{height} @ {framerate}fps, formato: {format_str}"
            )
        except Exception as e:
            logger.error(f"Error configurando cámara: {e}")
            raise RuntimeError(f"No se pudo configurar la cámara: {e}") from e
    
    def start(self) -> None:
        """Inicia la captura de video.
        
        Raises:
            RuntimeError: Si hay error iniciando la cámara.
        """
        if self.camera is not None and self.is_running:
            logger.warning("Cámara ya está corriendo")
            return
        
        try:
            if self.camera is None:
                self.camera = Picamera2()
            
            self._configure_camera()
            self.camera.start()
            self.is_running = True
            logger.info("Cámara iniciada correctamente")
        except Exception as e:
            logger.error(f"Error iniciando cámara: {e}")
            self.is_running = False
            raise RuntimeError(f"No se pudo iniciar la cámara: {e}") from e
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Captura un frame de video.
        
        Returns:
            Array numpy con el frame (RGB) o None si hay error.
            
        Note:
            El frame retornado está en formato RGB888 con shape (height, width, 3).
        """
        if not self.is_running or self.camera is None:
            logger.warning("Cámara no está corriendo")
            return None
        
        try:
            frame = self.camera.capture_array()
            return frame
        except Exception as e:
            logger.error(f"Error capturando frame: {e}", exc_info=True)
            return None
    
    def stop(self) -> None:
        """Detiene la captura de video."""
        if self.camera is not None and self.is_running:
            try:
                self.camera.stop()
                self.is_running = False
                logger.info("Cámara detenida")
            except Exception as e:
                logger.error(f"Error deteniendo cámara: {e}")
        else:
            logger.debug("Cámara ya estaba detenida")
    
    def get_resolution(self) -> Tuple[int, int]:
        """Obtiene la resolución configurada de la cámara.
        
        Returns:
            Tupla (width, height).
        """
        cam_config = self.config.get('camera', {})
        resolution = cam_config.get('resolution', {})
        width = resolution.get('width', 1920)
        height = resolution.get('height', 1080)
        return (width, height)
    
    def get_framerate(self) -> int:
        """Obtiene el framerate configurado.
        
        Returns:
            Framerate en FPS.
        """
        cam_config = self.config.get('camera', {})
        return cam_config.get('framerate', 30)
    
    def __enter__(self) -> 'IMX219Handler':
        """Context manager entry.
        
        Returns:
            Self.
        """
        self.start()
        return self
    
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], 
                 exc_tb: Optional[Any]) -> None:
        """Context manager exit.
        
        Args:
            exc_type: Tipo de excepción si la hay.
            exc_val: Valor de excepción si la hay.
            exc_tb: Traceback si la hay.
        """
        self.stop()
    
    def __del__(self) -> None:
        """Destructor - asegura que la cámara se detenga."""
        self.stop()
