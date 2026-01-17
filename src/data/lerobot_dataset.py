"""Integración con LeRobotDataset para almacenamiento de episodios.

Este módulo proporciona una interfaz para guardar episodios de video
en formato compatible con LeRobotDataset v3.
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
import cv2


logger = logging.getLogger(__name__)


class EpisodeRecorder:
    """Grabador de episodios en formato LeRobotDataset.
    
    Esta clase maneja la creación y almacenamiento de episodios de video
    en una estructura compatible con LeRobotDataset v3.
    
    Attributes:
        episode_path: Directorio base para guardar episodios.
        current_episode: Lista de frames del episodio actual.
        episode_metadata: Metadatos del episodio actual.
        episode_id: ID del episodio actual.
    """
    
    def __init__(self, episode_path: str = "./data/episodes") -> None:
        """Inicializa el grabador de episodios.
        
        Args:
            episode_path: Ruta al directorio donde se guardan los episodios.
        """
        self.episode_path = Path(episode_path)
        self.episode_path.mkdir(parents=True, exist_ok=True)
        self.current_episode: List[Dict[str, Any]] = []
        self.episode_metadata: Dict[str, Any] = {}
        self.episode_id: Optional[str] = None
        self.is_recording: bool = False
        
        logger.info(f"EpisodeRecorder inicializado: {self.episode_path}")
    
    def start_episode(self, episode_id: Optional[str] = None) -> str:
        """Inicia un nuevo episodio.
        
        Args:
            episode_id: ID del episodio (se genera automáticamente si None).
            
        Returns:
            ID del episodio.
        """
        if self.is_recording:
            logger.warning("Ya hay un episodio en grabación, finalizando el anterior")
            self.save_episode()
        
        if episode_id is None:
            episode_id = f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.episode_id = episode_id
        self.current_episode = []
        self.episode_metadata = {
            "episode_id": episode_id,
            "start_time": datetime.now().isoformat(),
            "fps": 30,  # Se actualizará al guardar
            "resolution": None,  # Se establecerá con el primer frame
            "motion_detected": True,
            "total_frames": 0
        }
        self.is_recording = True
        
        logger.info(f"Episodio iniciado: {episode_id}")
        return episode_id
    
    def add_frame(
        self,
        frame: np.ndarray,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Añade un frame al episodio actual.
        
        Args:
            frame: Frame de video (numpy array RGB).
            metadata: Metadatos adicionales del frame (opcional).
        """
        if not self.is_recording:
            logger.warning("No hay episodio activo, iniciando uno nuevo")
            self.start_episode()
        
        frame_data: Dict[str, Any] = {
            "frame_index": len(self.current_episode),
            "timestamp": datetime.now().isoformat(),
            "frame": frame.copy()  # Copia para evitar modificaciones
        }
        
        if metadata:
            frame_data.update(metadata)
        
        self.current_episode.append(frame_data)
        
        # Actualizar resolución en metadata si es el primer frame
        if self.episode_metadata.get("resolution") is None and len(frame.shape) >= 2:
            self.episode_metadata["resolution"] = {
                "width": frame.shape[1],
                "height": frame.shape[0]
            }
    
    def save_episode(self) -> Optional[str]:
        """Guarda el episodio actual en formato LeRobotDataset.
        
        Returns:
            Ruta al episodio guardado o None si no hay episodio.
        """
        if not self.is_recording or len(self.current_episode) == 0:
            logger.warning("No hay episodio para guardar")
            return None
        
        if self.episode_id is None:
            logger.error("Episode ID no establecido")
            return None
        
        # Crear directorio del episodio
        episode_dir = self.episode_path / self.episode_id
        episode_dir.mkdir(parents=True, exist_ok=True)
        images_dir = episode_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Guardar frames como imágenes
        frame_paths: List[str] = []
        for frame_data in self.current_episode:
            frame = frame_data["frame"]
            frame_index = frame_data["frame_index"]
            
            # Guardar frame como JPEG
            frame_filename = f"frame_{frame_index:06d}.jpg"
            frame_path = images_dir / frame_filename
            frame_paths.append(str(frame_path.relative_to(episode_dir)))
            
            # Convertir RGB a BGR para OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(frame_path), frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
        
        # Actualizar metadata
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.episode_metadata["start_time"])
        duration = (end_time - start_time).total_seconds()
        
        self.episode_metadata.update({
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "total_frames": len(self.current_episode),
            "frame_paths": frame_paths
        })
        
        # Guardar metadata.json
        metadata_path = episode_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(self.episode_metadata, f, indent=2)
        
        # Guardar info.json (formato LeRobotDataset)
        info_data = {
            "episode_id": self.episode_id,
            "start_time": self.episode_metadata["start_time"],
            "end_time": self.episode_metadata["end_time"],
            "duration_seconds": duration,
            "fps": self.episode_metadata["fps"],
            "total_frames": len(self.current_episode),
            "resolution": self.episode_metadata["resolution"],
            "motion_detected": self.episode_metadata.get("motion_detected", False)
        }
        
        info_path = episode_dir / "info.json"
        with open(info_path, 'w') as f:
            json.dump(info_data, f, indent=2)
        
        episode_file_path = str(episode_dir)
        logger.info(
            f"Episodio guardado: {self.episode_id} "
            f"({len(self.current_episode)} frames, {duration:.2f}s) "
            f"en {episode_file_path}"
        )
        
        # Resetear para próximo episodio
        self.current_episode = []
        self.episode_metadata = {}
        self.episode_id = None
        self.is_recording = False
        
        return episode_file_path
    
    def stop_episode(self) -> Optional[str]:
        """Detiene y guarda el episodio actual.
        
        Returns:
            Ruta al episodio guardado o None.
        """
        if not self.is_recording:
            return None
        return self.save_episode()
    
    def get_current_episode_info(self) -> Optional[Dict[str, Any]]:
        """Obtiene información del episodio actual.
        
        Returns:
            Diccionario con información del episodio o None si no hay episodio activo.
        """
        if not self.is_recording:
            return None
        
        return {
            "episode_id": self.episode_id,
            "frame_count": len(self.current_episode),
            "metadata": self.episode_metadata.copy()
        }
