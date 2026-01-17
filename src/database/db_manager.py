"""Gestor de base de datos SQLite para metadatos del sistema.

Este módulo proporciona una interfaz para gestionar metadatos de episodios,
eventos, modelos y entrenamientos en una base de datos SQLite.
"""

import logging
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gestor de base de datos SQLite.
    
    Esta clase maneja todas las operaciones de base de datos para el sistema,
    incluyendo episodios, eventos, modelos y entrenamientos.
    
    Attributes:
        db_path: Ruta al archivo de base de datos SQLite.
    """
    
    def __init__(self, db_path: str = "data/database.db") -> None:
        """Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info(f"DatabaseManager inicializado: {self.db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos.
        
        Returns:
            Conexión SQLite configurada.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        return conn
    
    def _init_database(self) -> None:
        """Crea las tablas si no existen."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabla de episodios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS episodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    episode_id TEXT UNIQUE NOT NULL,
                    file_path TEXT NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    duration_seconds REAL,
                    motion_detected BOOLEAN DEFAULT 0,
                    object_detected TEXT,
                    confidence_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata_json TEXT
                )
            """)
            
            # Tabla de modelos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    trained_at TIMESTAMP NOT NULL,
                    dataset_used TEXT,
                    accuracy REAL,
                    precision_score REAL,
                    recall_score REAL,
                    training_params_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(model_name, version)
                )
            """)
            
            # Tabla de entrenamientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id INTEGER,
                    started_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    status TEXT,
                    epochs INTEGER,
                    loss REAL,
                    validation_loss REAL,
                    notes TEXT,
                    FOREIGN KEY (model_id) REFERENCES models(id)
                )
            """)
            
            # Tabla de eventos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    episode_id INTEGER,
                    message TEXT,
                    severity TEXT,
                    FOREIGN KEY (episode_id) REFERENCES episodes(id)
                )
            """)
            
            # Índices para mejorar rendimiento
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_episodes_time 
                ON episodes(start_time)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_episodes_motion 
                ON episodes(motion_detected)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_events_time 
                ON events(timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_events_type 
                ON events(event_type)
            """)
            
            conn.commit()
            logger.debug("Base de datos inicializada correctamente")
        except sqlite3.Error as e:
            logger.error(f"Error inicializando base de datos: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add_episode(
        self,
        episode_id: str,
        file_path: str,
        start_time: datetime,
        motion_detected: bool = False,
        object_detected: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Añade un nuevo episodio a la base de datos.
        
        Args:
            episode_id: ID único del episodio.
            file_path: Ruta al archivo/episodio.
            start_time: Timestamp de inicio.
            motion_detected: Si se detectó movimiento.
            object_detected: Lista de objetos detectados (opcional).
            metadata: Metadatos adicionales en formato dict (opcional).
            
        Returns:
            ID del episodio insertado.
            
        Raises:
            sqlite3.IntegrityError: Si el episode_id ya existe.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            object_json = json.dumps(object_detected) if object_detected else None
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute("""
                INSERT INTO episodes 
                (episode_id, file_path, start_time, motion_detected, 
                 object_detected, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                episode_id,
                file_path,
                start_time.isoformat(),
                motion_detected,
                object_json,
                metadata_json
            ))
            
            episode_db_id = cursor.lastrowid
            conn.commit()
            logger.debug(f"Episodio añadido: {episode_id} (DB ID: {episode_db_id})")
            return episode_db_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Error de integridad añadiendo episodio: {e}")
            conn.rollback()
            raise
        except sqlite3.Error as e:
            logger.error(f"Error añadiendo episodio: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def update_episode(
        self,
        episode_id: str,
        end_time: datetime,
        duration: float
    ) -> None:
        """Actualiza un episodio cuando termina.
        
        Args:
            episode_id: ID del episodio a actualizar.
            end_time: Timestamp de fin.
            duration: Duración en segundos.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE episodes 
                SET end_time = ?, duration_seconds = ?
                WHERE episode_id = ?
            """, (end_time.isoformat(), duration, episode_id))
            
            if cursor.rowcount == 0:
                logger.warning(f"Episodio no encontrado para actualizar: {episode_id}")
            else:
                conn.commit()
                logger.debug(f"Episodio actualizado: {episode_id}")
        except sqlite3.Error as e:
            logger.error(f"Error actualizando episodio: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_episodes(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        motion_only: bool = False,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Obtiene episodios con filtros.
        
        Args:
            start_date: Fecha de inicio para filtrar (opcional).
            end_date: Fecha de fin para filtrar (opcional).
            motion_only: Si True, solo episodios con movimiento.
            limit: Número máximo de resultados.
            
        Returns:
            Lista de diccionarios con información de episodios.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT * FROM episodes WHERE 1=1"
            params: List[Any] = []
            
            if start_date:
                query += " AND start_time >= ?"
                params.append(start_date.isoformat())
            
            if end_date:
                query += " AND start_time <= ?"
                params.append(end_date.isoformat())
            
            if motion_only:
                query += " AND motion_detected = 1"
            
            query += " ORDER BY start_time DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convertir rows a diccionarios
            episodes = []
            for row in rows:
                episode_dict = dict(row)
                # Parsear JSON fields
                if episode_dict.get('object_detected'):
                    try:
                        episode_dict['object_detected'] = json.loads(
                            episode_dict['object_detected']
                        )
                    except json.JSONDecodeError:
                        episode_dict['object_detected'] = None
                if episode_dict.get('metadata_json'):
                    try:
                        episode_dict['metadata_json'] = json.loads(
                            episode_dict['metadata_json']
                        )
                    except json.JSONDecodeError:
                        episode_dict['metadata_json'] = None
                episodes.append(episode_dict)
            
            return episodes
        except sqlite3.Error as e:
            logger.error(f"Error obteniendo episodios: {e}")
            return []
        finally:
            conn.close()
    
    def add_event(
        self,
        event_type: str,
        message: str,
        severity: str = "info",
        episode_id: Optional[int] = None
    ) -> int:
        """Registra un evento en la base de datos.
        
        Args:
            event_type: Tipo de evento (motion, episode_started, etc.).
            message: Mensaje descriptivo.
            severity: Nivel de severidad (info, warning, error, critical).
            episode_id: ID del episodio relacionado (opcional).
            
        Returns:
            ID del evento insertado.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO events (event_type, message, severity, episode_id)
                VALUES (?, ?, ?, ?)
            """, (event_type, message, severity, episode_id))
            
            event_id = cursor.lastrowid
            conn.commit()
            logger.debug(f"Evento registrado: {event_type} - {message}")
            return event_id
        except sqlite3.Error as e:
            logger.error(f"Error añadiendo evento: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_events(
        self,
        limit: int = 50,
        event_type: Optional[str] = None,
        severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene eventos recientes.
        
        Args:
            limit: Número máximo de resultados.
            event_type: Filtrar por tipo de evento (opcional).
            severity: Filtrar por severidad (opcional).
            
        Returns:
            Lista de diccionarios con información de eventos.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT * FROM events WHERE 1=1"
            params: List[Any] = []
            
            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)
            
            if severity:
                query += " AND severity = ?"
                params.append(severity)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Error obteniendo eventos: {e}")
            return []
        finally:
            conn.close()
    
    def add_model(
        self,
        model_name: str,
        version: str,
        file_path: str,
        accuracy: Optional[float] = None,
        training_params: Optional[Dict[str, Any]] = None
    ) -> int:
        """Registra un modelo entrenado.
        
        Args:
            model_name: Nombre del modelo.
            version: Versión del modelo (semver).
            file_path: Ruta al archivo del modelo.
            accuracy: Precisión del modelo (0-1, opcional).
            training_params: Parámetros de entrenamiento (opcional).
            
        Returns:
            ID del modelo insertado.
            
        Raises:
            sqlite3.IntegrityError: Si el modelo con esa versión ya existe.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            params_json = json.dumps(training_params) if training_params else None
            
            cursor.execute("""
                INSERT INTO models 
                (model_name, version, file_path, trained_at, accuracy, training_params_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                model_name,
                version,
                file_path,
                datetime.now().isoformat(),
                accuracy,
                params_json
            ))
            
            model_id = cursor.lastrowid
            conn.commit()
            logger.info(f"Modelo registrado: {model_name} v{version} (ID: {model_id})")
            return model_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Modelo ya existe: {model_name} v{version}")
            conn.rollback()
            raise
        except sqlite3.Error as e:
            logger.error(f"Error añadiendo modelo: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema.
        
        Returns:
            Diccionario con estadísticas (total_episodes, total_events, etc.).
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            stats: Dict[str, Any] = {}
            
            # Total de episodios
            cursor.execute("SELECT COUNT(*) FROM episodes")
            stats['total_episodes'] = cursor.fetchone()[0]
            
            # Episodios con movimiento
            cursor.execute("SELECT COUNT(*) FROM episodes WHERE motion_detected = 1")
            stats['episodes_with_motion'] = cursor.fetchone()[0]
            
            # Total de eventos
            cursor.execute("SELECT COUNT(*) FROM events")
            stats['total_events'] = cursor.fetchone()[0]
            
            # Total de modelos
            cursor.execute("SELECT COUNT(*) FROM models")
            stats['total_models'] = cursor.fetchone()[0]
            
            return stats
        except sqlite3.Error as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
        finally:
            conn.close()
