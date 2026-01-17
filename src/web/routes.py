"""Endpoints REST API para el sistema de seguridad."""

import logging
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.database.db_manager import DatabaseManager


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["api"])


# Modelos Pydantic para respuestas
class EpisodeResponse(BaseModel):
    """Respuesta de episodio."""
    id: int
    episode_id: str
    file_path: str
    start_time: str
    end_time: Optional[str]
    duration_seconds: Optional[float]
    motion_detected: bool
    object_detected: Optional[List[str]]


class EventResponse(BaseModel):
    """Respuesta de evento."""
    id: int
    event_type: str
    timestamp: str
    episode_id: Optional[int]
    message: str
    severity: str


class StatusResponse(BaseModel):
    """Respuesta de estado del sistema."""
    camera_active: bool
    motion_detected: bool
    fps: float
    total_episodes: int
    total_events: int
    uptime_seconds: float


class ConfigUpdate(BaseModel):
    """Modelo para actualización de configuración."""
    motion_threshold: Optional[int] = None
    min_area: Optional[int] = None
    background_update_rate: Optional[float] = None


# Estado global del sistema (será actualizado por el thread de cámara)
system_status = {
    "camera_active": False,
    "motion_detected": False,
    "fps": 0.0,
    "start_time": datetime.now(),
    "motion_count": 0
}


@router.get("/episodes", response_model=List[EpisodeResponse])
async def get_episodes(
    start_date: Optional[str] = Query(None, description="Fecha inicio (ISO format)"),
    end_date: Optional[str] = Query(None, description="Fecha fin (ISO format)"),
    motion_only: bool = Query(False, description="Solo episodios con movimiento"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados")
) -> List[EpisodeResponse]:
    """Obtiene lista de episodios con filtros.
    
    Args:
        start_date: Fecha de inicio para filtrar (ISO format).
        end_date: Fecha de fin para filtrar (ISO format).
        motion_only: Si True, solo episodios con movimiento.
        limit: Número máximo de resultados.
        
    Returns:
        Lista de episodios.
    """
    try:
        db_manager = router.db_manager  # type: ignore
        
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        episodes = db_manager.get_episodes(
            start_date=start_dt,
            end_date=end_dt,
            motion_only=motion_only,
            limit=limit
        )
        
        return [EpisodeResponse(**ep) for ep in episodes]
    except Exception as e:
        logger.error(f"Error obteniendo episodios: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events", response_model=List[EventResponse])
async def get_events(
    limit: int = Query(50, ge=1, le=500, description="Límite de resultados"),
    event_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    severity: Optional[str] = Query(None, description="Filtrar por severidad")
) -> List[EventResponse]:
    """Obtiene eventos recientes.
    
    Args:
        limit: Número máximo de resultados.
        event_type: Filtrar por tipo de evento.
        severity: Filtrar por severidad.
        
    Returns:
        Lista de eventos.
    """
    try:
        db_manager = router.db_manager  # type: ignore
        events = db_manager.get_events(
            limit=limit,
            event_type=event_type,
            severity=severity
        )
        return [EventResponse(**ev) for ev in events]
    except Exception as e:
        logger.error(f"Error obteniendo eventos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=StatusResponse)
async def get_status() -> StatusResponse:
    """Obtiene estado actual del sistema.
    
    Returns:
        Estado del sistema.
    """
    try:
        db_manager = router.db_manager  # type: ignore
        stats = db_manager.get_stats()
        
        # Convertir start_time a datetime si es un timestamp
        start_time = system_status.get("start_time")
        if isinstance(start_time, (int, float)):
            start_time = datetime.fromtimestamp(start_time)
        elif not isinstance(start_time, datetime):
            start_time = datetime.now()
        
        uptime = (datetime.now() - start_time).total_seconds()
        
        return StatusResponse(
            camera_active=system_status["camera_active"],
            motion_detected=system_status["motion_detected"],
            fps=system_status["fps"],
            total_episodes=stats.get("total_episodes", 0),
            total_events=stats.get("total_events", 0),
            uptime_seconds=uptime
        )
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config")
async def update_config(config: ConfigUpdate) -> dict:
    """Actualiza configuración del sistema.
    
    Args:
        config: Configuración a actualizar.
        
    Returns:
        Confirmación de actualización.
    """
    try:
        # Obtener detector desde el router (será configurado por camera_server)
        detector = getattr(router, 'motion_detector', None)
        
        if detector is None:
            raise HTTPException(status_code=503, detail="Sistema no inicializado")
        
        # Actualizar configuración
        detector.update_config(
            threshold=config.motion_threshold,
            min_area=config.min_area,
            background_update_rate=config.background_update_rate
        )
        
        return {
            "status": "success",
            "message": "Configuración actualizada",
            "config": config.dict(exclude_none=True)
        }
    except Exception as e:
        logger.error(f"Error actualizando configuración: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
