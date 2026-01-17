"""Sistema de notificaciones y logging estructurado.

Este módulo proporciona un sistema de logging estructurado para eventos
del sistema de seguridad.
"""

import logging
from typing import Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class NotificationManager:
    """Gestor de notificaciones y logging.
    
    Esta clase centraliza el logging de eventos del sistema,
    proporcionando una interfaz consistente para registrar eventos.
    
    Attributes:
        db_manager: Referencia opcional al gestor de base de datos
            para guardar eventos en BD.
    """
    
    def __init__(self, db_manager: Optional[Any] = None) -> None:
        """Inicializa el gestor de notificaciones.
        
        Args:
            db_manager: Instancia de DatabaseManager para guardar eventos (opcional).
        """
        self.db_manager = db_manager
        logger.info("NotificationManager inicializado")
    
    def log_event(
        self,
        event_type: str,
        message: str,
        severity: str = "info",
        episode_id: Optional[int] = None
    ) -> None:
        """Registra un evento en logs y opcionalmente en base de datos.
        
        Args:
            event_type: Tipo de evento (motion, episode_started, etc.).
            message: Mensaje descriptivo.
            severity: Nivel de severidad (info, warning, error, critical).
            episode_id: ID del episodio relacionado (opcional).
        """
        # Logging según severidad
        log_method = {
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
            "critical": logger.critical
        }.get(severity.lower(), logger.info)
        
        log_message = f"[{event_type}] {message}"
        if episode_id:
            log_message += f" (episode_id: {episode_id})"
        
        log_method(log_message)
        
        # Guardar en base de datos si está disponible
        if self.db_manager:
            try:
                self.db_manager.add_event(
                    event_type=event_type,
                    message=message,
                    severity=severity,
                    episode_id=episode_id
                )
            except Exception as e:
                logger.error(f"Error guardando evento en BD: {e}", exc_info=True)
    
    def motion_detected(self, area: float, episode_id: Optional[int] = None) -> None:
        """Registra detección de movimiento.
        
        Args:
            area: Área de movimiento detectada en píxeles.
            episode_id: ID del episodio relacionado (opcional).
        """
        self.log_event(
            event_type="motion_detected",
            message=f"Movimiento detectado (área: {area:.0f} px²)",
            severity="info",
            episode_id=episode_id
        )
    
    def episode_started(self, episode_id: str, db_id: Optional[int] = None) -> None:
        """Registra inicio de episodio.
        
        Args:
            episode_id: ID del episodio.
            db_id: ID en base de datos (opcional).
        """
        self.log_event(
            event_type="episode_started",
            message=f"Episodio iniciado: {episode_id}",
            severity="info",
            episode_id=db_id
        )
    
    def episode_saved(self, episode_id: str, duration: float, 
                     frame_count: int, db_id: Optional[int] = None) -> None:
        """Registra guardado de episodio.
        
        Args:
            episode_id: ID del episodio.
            duration: Duración en segundos.
            frame_count: Número de frames guardados.
            db_id: ID en base de datos (opcional).
        """
        self.log_event(
            event_type="episode_saved",
            message=f"Episodio guardado: {episode_id} ({frame_count} frames, {duration:.2f}s)",
            severity="info",
            episode_id=db_id
        )
    
    def error(self, error_type: str, message: str, 
             episode_id: Optional[int] = None) -> None:
        """Registra un error.
        
        Args:
            error_type: Tipo de error.
            message: Mensaje descriptivo.
            episode_id: ID del episodio relacionado (opcional).
        """
        self.log_event(
            event_type="error",
            message=f"{error_type}: {message}",
            severity="error",
            episode_id=episode_id
        )
    
    def warning(self, warning_type: str, message: str,
               episode_id: Optional[int] = None) -> None:
        """Registra una advertencia.
        
        Args:
            warning_type: Tipo de advertencia.
            message: Mensaje descriptivo.
            episode_id: ID del episodio relacionado (opcional).
        """
        self.log_event(
            event_type="warning",
            message=f"{warning_type}: {message}",
            severity="warning",
            episode_id=episode_id
        )
