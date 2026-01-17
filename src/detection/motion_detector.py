"""Detector de movimiento usando algoritmo de diferencia de frames.

Este módulo implementa detección de movimiento basada en diferencia
de frames con actualización adaptativa del fondo.
"""

import logging
from typing import Tuple, Optional
import numpy as np
import cv2


logger = logging.getLogger(__name__)


class MotionDetector:
    """Detector de movimiento usando diferencia de frames.
    
    Este detector compara frames consecutivos con un fondo de referencia
    para identificar áreas de movimiento. El fondo se actualiza adaptativamente
    para manejar cambios graduales en la iluminación.
    
    Attributes:
        threshold: Umbral de diferencia de píxeles para considerar movimiento.
        min_area: Área mínima de contorno para considerar movimiento válido.
        blur_kernel: Tamaño del kernel para blur gaussiano.
        background_update_rate: Tasa de actualización del fondo (0-1).
        background: Frame de fondo actual.
        background_set: Indica si el fondo ha sido establecido.
    """
    
    def __init__(
        self,
        threshold: int = 30,
        min_area: int = 500,
        blur_kernel: int = 5,
        background_update_rate: float = 0.1
    ) -> None:
        """Inicializa el detector de movimiento.
        
        Args:
            threshold: Umbral de diferencia (0-255). Valores más bajos = más sensible.
            min_area: Área mínima en píxeles para considerar movimiento.
            blur_kernel: Tamaño del kernel para blur (debe ser impar).
            background_update_rate: Tasa de actualización del fondo (0-1).
                Valores más altos = fondo se actualiza más rápido.
        """
        if blur_kernel % 2 == 0:
            blur_kernel += 1  # Asegurar que sea impar
            logger.warning(f"blur_kernel ajustado a {blur_kernel} (debe ser impar)")
        
        self.threshold: int = threshold
        self.min_area: int = min_area
        self.blur_kernel: int = blur_kernel
        self.background_update_rate: float = background_update_rate
        self.background: Optional[np.ndarray] = None
        self.background_set: bool = False
        
        logger.info(
            f"MotionDetector inicializado: threshold={threshold}, "
            f"min_area={min_area}, blur_kernel={blur_kernel}"
        )
    
    def set_background(self, frame: np.ndarray) -> None:
        """Establece el frame de fondo inicial.
        
        Args:
            frame: Frame RGB para usar como fondo.
            
        Raises:
            ValueError: Si el frame no es válido.
        """
        if frame is None or frame.size == 0:
            raise ValueError("Frame inválido para establecer fondo")
        
        # Convertir a escala de grises
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        else:
            gray = frame.copy()
        
        # Aplicar blur gaussiano
        self.background = cv2.GaussianBlur(
            gray,
            (self.blur_kernel, self.blur_kernel),
            0
        )
        self.background_set = True
        logger.info("Fondo establecido")
    
    def update_background(self, frame: np.ndarray) -> None:
        """Actualiza el fondo adaptativamente.
        
        El fondo se actualiza usando una media móvil exponencial para
        adaptarse a cambios graduales en iluminación.
        
        Args:
            frame: Frame RGB actual.
        """
        if not self.background_set:
            self.set_background(frame)
            return
        
        # Convertir a escala de grises y aplicar blur
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        else:
            gray = frame.copy()
        
        gray_blurred = cv2.GaussianBlur(
            gray,
            (self.blur_kernel, self.blur_kernel),
            0
        )
        
        # Actualización adaptativa: media móvil exponencial
        if self.background is not None:
            self.background = (
                (1 - self.background_update_rate) * self.background +
                self.background_update_rate * gray_blurred
            ).astype(np.uint8)
    
    def detect(self, frame: np.ndarray) -> Tuple[bool, np.ndarray]:
        """Detecta movimiento en el frame.
        
        Args:
            frame: Frame RGB para analizar.
            
        Returns:
            Tupla (motion_detected, annotated_frame):
                - motion_detected: True si se detectó movimiento.
                - annotated_frame: Frame con rectángulos dibujados en áreas de movimiento.
                
        Raises:
            ValueError: Si el frame no es válido.
        """
        if frame is None or frame.size == 0:
            raise ValueError("Frame inválido para detección")
        
        # Si el fondo no está establecido, establecerlo y retornar sin movimiento
        if not self.background_set:
            self.set_background(frame)
            return False, frame.copy()
        
        # Convertir a escala de grises
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        else:
            gray = frame.copy()
        
        # Aplicar blur gaussiano para reducir ruido
        gray_blurred = cv2.GaussianBlur(
            gray,
            (self.blur_kernel, self.blur_kernel),
            0
        )
        
        # Calcular diferencia absoluta con el fondo
        frame_delta = cv2.absdiff(self.background, gray_blurred)
        
        # Aplicar threshold para binarizar
        _, thresh = cv2.threshold(
            frame_delta,
            self.threshold,
            255,
            cv2.THRESH_BINARY
        )
        
        # Dilatación para conectar áreas cercanas
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(
            thresh.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Crear copia del frame para anotar
        annotated_frame = frame.copy()
        motion_detected = False
        
        # Procesar contornos
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar por área mínima
            if area < self.min_area:
                continue
            
            motion_detected = True
            
            # Obtener bounding box
            (x, y, w, h) = cv2.boundingRect(contour)
            
            # Dibujar rectángulo verde en el frame anotado
            cv2.rectangle(
                annotated_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),  # Verde en RGB
                2
            )
        
        # Actualizar fondo adaptativamente (solo si no hay movimiento)
        # para evitar que el objeto en movimiento se convierta en fondo
        if not motion_detected:
            self.update_background(frame)
        
        return motion_detected, annotated_frame
    
    def reset_background(self) -> None:
        """Resetea el fondo, forzando recalibración en el próximo frame."""
        self.background = None
        self.background_set = False
        logger.info("Fondo reseteado")
    
    def update_config(
        self,
        threshold: Optional[int] = None,
        min_area: Optional[int] = None,
        background_update_rate: Optional[float] = None
    ) -> None:
        """Actualiza parámetros de configuración.
        
        Args:
            threshold: Nuevo umbral (None para no cambiar).
            min_area: Nueva área mínima (None para no cambiar).
            background_update_rate: Nueva tasa de actualización (None para no cambiar).
        """
        if threshold is not None:
            if 0 <= threshold <= 255:
                self.threshold = threshold
                logger.info(f"Threshold actualizado a {threshold}")
            else:
                logger.warning(f"Threshold inválido: {threshold} (debe estar entre 0-255)")
        
        if min_area is not None:
            if min_area > 0:
                self.min_area = min_area
                logger.info(f"Min area actualizado a {min_area}")
            else:
                logger.warning(f"Min area inválido: {min_area} (debe ser > 0)")
        
        if background_update_rate is not None:
            if 0.0 <= background_update_rate <= 1.0:
                self.background_update_rate = background_update_rate
                logger.info(f"Background update rate actualizado a {background_update_rate}")
            else:
                logger.warning(
                    f"Background update rate inválido: {background_update_rate} "
                    "(debe estar entre 0.0-1.0)"
                )
