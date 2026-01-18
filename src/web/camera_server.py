"""Servidor FastAPI principal para streaming y API REST."""

import logging
import asyncio
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
import cv2
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.camera.imx219_handler import IMX219Handler
from src.detection.motion_detector import MotionDetector
from src.database.db_manager import DatabaseManager
from src.data.lerobot_dataset import EpisodeRecorder
from src.alerts.notification import NotificationManager
from src.web.routes import router, system_status


logger = logging.getLogger(__name__)


class CameraServer:
    """Servidor FastAPI para streaming y API REST.
    
    Esta clase gestiona el servidor web, streaming MJPEG, captura de frames,
    detección de movimiento y almacenamiento de episodios.
    """
    
    def __init__(
        self,
        config_path: str = "config/camera_config.yaml",
        host: str = "0.0.0.0",
        port: int = 5000
    ) -> None:
        """Inicializa el servidor de cámara.
        
        Args:
            config_path: Ruta al archivo de configuración.
            host: Host del servidor.
            port: Puerto del servidor.
        """
        self.config_path = config_path
        self.host = host
        self.port = port
        
        # Inicializar componentes
        self.camera: Optional[IMX219Handler] = None
        self.detector: Optional[MotionDetector] = None
        self.db_manager: Optional[DatabaseManager] = None
        self.recorder: Optional[EpisodeRecorder] = None
        self.notifier: Optional[NotificationManager] = None
        
        # Estado del sistema
        self.current_frame: Optional[np.ndarray] = None
        self.frame_lock = threading.Lock()
        self.camera_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        # Estado de episodio
        self.episode_active = False
        self.episode_start_time: Optional[float] = None
        self.episode_id: Optional[str] = None
        self.episode_db_id: Optional[int] = None
        
        # FastAPI app
        self.app = FastAPI(
            title="Pi Camera Security System",
            description="Sistema de seguridad con detección de movimiento",
            version="1.0.0"
        )
        
        # Configurar rutas
        self._setup_routes()
        
        logger.info(f"CameraServer inicializado: {host}:{port}")
    
    def _setup_routes(self) -> None:
        """Configura las rutas de FastAPI."""
        # Montar archivos estáticos
        static_path = Path(__file__).parent / "static"
        if static_path.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
        
        # Templates
        templates_path = Path(__file__).parent / "templates"
        if templates_path.exists():
            self.templates = Jinja2Templates(directory=str(templates_path))
        else:
            self.templates = None
        
        # Ruta principal
        @self.app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            """Página principal con dashboard."""
            if self.templates:
                return self.templates.TemplateResponse("index.html", {"request": request})
            return HTMLResponse(content="<h1>Pi Camera Security System</h1><p>Frontend no disponible</p>")
        
        # Streaming MJPEG
        @self.app.get("/video_feed")
        async def video_feed():
            """Stream MJPEG de video en tiempo real."""
            return StreamingResponse(
                self._generate_frames(),
                media_type="multipart/x-mixed-replace; boundary=frame"
            )
        
        # Incluir rutas API
        self.app.include_router(router)
    
    async def _generate_frames(self):
        """Generador async de frames MJPEG."""
        while self.is_running:
            with self.frame_lock:
                frame = self.current_frame
            
            if frame is not None:
                # Convertir RGB a BGR para OpenCV
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Codificar como JPEG con calidad optimizada para Raspberry Pi
                # Calidad 70 es un buen balance entre calidad y tamaño
                ret, buffer = cv2.imencode('.jpg', frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Reducir FPS a 10 para mejor rendimiento en Raspberry Pi
            await asyncio.sleep(0.1)  # ~10 FPS (óptimo para Pi)
    
    def _camera_thread_func(self) -> None:
        """Thread que captura frames y detecta movimiento."""
        try:
            # Inicializar componentes
            import yaml
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Cámara
            self.camera = IMX219Handler(self.config_path)
            self.camera.start()
            time.sleep(2)  # Calentamiento
            
            # Detector
            det_config = config.get('detection', {})
            self.detector = MotionDetector(
                threshold=det_config.get('motion_threshold', 30),
                min_area=det_config.get('min_area', 500),
                blur_kernel=det_config.get('blur_kernel', 5),
                background_update_rate=det_config.get('background_update_rate', 0.1),
                consecutive_frames=det_config.get('consecutive_frames', 1),
                calibration_frames=det_config.get('calibration_frames', 30)
            )
            
            # Base de datos
            db_config = config.get('database', {})
            self.db_manager = DatabaseManager(db_path=db_config.get('db_path', 'data/database.db'))
            
            # Recorder
            storage_config = config.get('storage', {})
            self.recorder = EpisodeRecorder(
                episode_path=storage_config.get('episode_path', './data/episodes')
            )
            
            # Notifier
            self.notifier = NotificationManager(db_manager=self.db_manager)
            
            # Configurar router con referencias
            router.db_manager = self.db_manager  # type: ignore
            router.motion_detector = self.detector  # type: ignore
            
            # Actualizar estado
            system_status["camera_active"] = True
            system_status["start_time"] = time.time()
            
            logger.info("Thread de cámara iniciado")
            self.notifier.log_event("system_started", "Sistema iniciado correctamente")
            
            frame_count = 0
            last_fps_time = time.time()
            motion_active_frames = 0
            last_motion_time: Optional[float] = None  # Tiempo desde que dejó de haber movimiento
            last_motion_detected = False  # Estado anterior de movimiento
            frames_without_motion = 0  # Contador de frames consecutivos sin movimiento
            
            # Loop principal
            while self.is_running:
                frame_start = time.time()
                
                # Capturar frame
                frame = self.camera.capture_frame()
                if frame is None:
                    time.sleep(0.1)
                    continue
                
                frame_count += 1
                
                # Reducir carga: procesar detección solo cada 2 frames
                if frame_count % 2 == 0:
                    try:
                        # Detectar movimiento (con frame reducido para mejor rendimiento)
                        if frame.shape[0] > 720:
                            # Reducir a 640x360 para detección más rápida
                            small_frame = cv2.resize(frame, (640, 360))
                            motion_detected, annotated_small = self.detector.detect(small_frame)
                            # Escalar de vuelta al tamaño original
                            annotated_frame = cv2.resize(annotated_small, (frame.shape[1], frame.shape[0]))
                        else:
                            motion_detected, annotated_frame = self.detector.detect(frame)
                        
                        # Actualizar frame actual (thread-safe)
                        with self.frame_lock:
                            self.current_frame = annotated_frame
                    except Exception as e:
                        logger.error(f"Error en detección: {e}", exc_info=True)
                        # En caso de error, usar frame sin procesar
                        with self.frame_lock:
                            self.current_frame = frame
                        motion_detected = False
                else:
                    # Frame sin procesar - asumir NO movimiento para incrementar contador
                    # Esto ayuda a que el contador se incremente más rápido
                    motion_detected = False
                    # Frame sin procesar - solo actualizar para mantener fluidez
                    with self.frame_lock:
                        self.current_frame = frame
                    time.sleep(0.05)  # Sleep para reducir CPU
                    # NO hacer continue aquí - necesitamos procesar la lógica de episodios
                
                # Guardar estado actual para siguiente iteración (solo cuando procesamos)
                if frame_count % 2 == 0:
                    last_motion_detected = motion_detected
                
                # CRÍTICO: Sistema basado en TIEMPO, no solo en frames
                # Rastrear tiempo desde que se inició el episodio o desde último movimiento real
                current_time = time.time()
                
                # Contar frames consecutivos sin movimiento
                if not motion_detected:
                    frames_without_motion += 1
                else:
                    frames_without_motion = 0
                    # Cuando hay movimiento, actualizar tiempo de último movimiento
                    if self.episode_active:
                        last_motion_time = current_time
                
                # Leer timeout de configuración
                calm_timeout = det_config.get('calm_timeout', 2.0)
                
                # CRÍTICO: Forzar estado a False basándose en TIEMPO, no solo en frames
                # Si hay episodio activo y ha pasado más tiempo del timeout, forzar cierre
                force_calm = False
                if self.episode_active:
                    if last_motion_time is not None:
                        time_since_last_motion = current_time - last_motion_time
                        if time_since_last_motion > calm_timeout:
                            force_calm = True
                            logger.info(f"Forzando calmado: {time_since_last_motion:.2f}s sin movimiento (timeout: {calm_timeout}s)")
                    else:
                        # Si no hay last_motion_time pero hay episodio activo, usar tiempo del episodio
                        episode_duration = current_time - self.episode_start_time
                        if episode_duration > calm_timeout * 2:  # Doble del timeout como seguridad
                            force_calm = True
                            logger.info(f"Forzando calmado: episodio activo por {episode_duration:.2f}s sin movimiento real")
                
                # También forzar si hay muchos frames sin movimiento (backup)
                if frames_without_motion >= 3:  # ~0.2 segundos
                    force_calm = True
                
                if force_calm:
                    # Forzar estado a False y mantenerlo así, IGNORANDO lo que dice el detector
                    motion_detected = False
                    system_status["motion_detected"] = False
                    # Si hay episodio activo, forzar cierre también
                    if self.episode_active:
                        # Cerrar episodio inmediatamente
                        self._close_episode()
                        last_motion_time = None
                        frames_without_motion = 0
                        # Forzar reset del fondo del detector para que se recalibre
                        try:
                            self.detector.reset_background()
                            logger.info("Fondo del detector reseteado forzadamente")
                        except Exception as e:
                            logger.error(f"Error reseteando fondo: {e}")
                else:
                    # Actualizar estado del sistema solo si no estamos forzando a False
                    # Pero solo actualizar si realmente procesamos el frame
                    if frame_count % 2 == 0:
                        system_status["motion_detected"] = motion_detected
                    # Si no procesamos el frame y hay muchos sin movimiento, forzar False
                    elif frames_without_motion >= 2:
                        system_status["motion_detected"] = False
                
                # Manejar episodios
                try:
                    if motion_detected and not force_calm:
                        motion_active_frames += 1
                        # Resetear contadores de tiempo sin movimiento solo si realmente hay movimiento
                        last_motion_time = current_time
                        frames_without_motion = 0
                        
                        if not self.episode_active:
                            # Iniciar nuevo episodio
                            self.episode_id = self.recorder.start_episode()
                            self.episode_start_time = time.time()
                            self.episode_active = True
                            last_motion_time = current_time  # Inicializar tiempo de último movimiento
                            
                            # Registrar en BD
                            self.episode_db_id = self.db_manager.add_episode(
                                episode_id=self.episode_id,
                                file_path=f"{self.recorder.episode_path}/{self.episode_id}",
                                start_time=datetime.fromtimestamp(self.episode_start_time),
                                motion_detected=True
                            )
                            
                            self.notifier.episode_started(self.episode_id, self.episode_db_id)
                            system_status["motion_count"] += 1
                    else:
                        motion_active_frames = 0
                        
                        if self.episode_active:
                            # Inicializar contador si es la primera vez sin movimiento
                            if last_motion_time is None:
                                last_motion_time = self.episode_start_time
                            
                            # La lógica de timeout ya se maneja arriba en force_calm
                            # Aquí solo mantenemos el estado
                        else:
                            # No hay episodio activo y no hay movimiento - asegurar estado calmado
                            if system_status.get("motion_detected", False):
                                system_status["motion_detected"] = False
                                frames_without_motion = 0
                                last_motion_time = None
                    
                    # Añadir frame al episodio solo cada 5 frames para reducir memoria
                    if self.episode_active and self.recorder and frame_count % 5 == 0:
                        try:
                            # Reducir resolución del frame antes de guardar
                            small_frame = cv2.resize(frame, (640, 360)) if frame.shape[0] > 720 else frame
                            self.recorder.add_frame(small_frame, {"motion": motion_detected})
                        except Exception as e:
                            logger.error(f"Error añadiendo frame al episodio: {e}")
                except Exception as e:
                    logger.error(f"Error manejando episodios: {e}", exc_info=True)
                
                # Calcular FPS cada 30 frames
                if frame_count % 30 == 0:
                    try:
                        elapsed = time.time() - last_fps_time
                        fps = 30 / elapsed if elapsed > 0 else 0
                        system_status["fps"] = fps
                        last_fps_time = time.time()
                    except Exception as e:
                        logger.error(f"Error calculando FPS: {e}")
                
                # Control de framerate - ajustado para 15 FPS
                frame_time = time.time() - frame_start
                sleep_time = max(0, 0.067 - frame_time)  # ~15 FPS
                time.sleep(sleep_time)
        
        except Exception as e:
            logger.critical(f"Error en thread de cámara: {e}", exc_info=True)
            system_status["camera_active"] = False
            if self.notifier:
                self.notifier.error("camera_thread", str(e))
        finally:
            if self.camera:
                self.camera.stop()
            if self.episode_active:
                self._close_episode()
            system_status["camera_active"] = False
            logger.info("Thread de cámara terminado")
    
    def _close_episode(self) -> None:
        """Cierra el episodio actual."""
        if not self.episode_active or not self.recorder:
            # Asegurar estado calmado incluso si no hay episodio activo
            system_status["motion_detected"] = False
            return
        
        try:
            # Guardar referencias antes de resetear
            episode_id = self.episode_id
            episode_db_id = self.episode_db_id
            episode_start = self.episode_start_time
            
            end_time = time.time()
            duration = end_time - episode_start if episode_start else 0
            
            # Guardar episodio
            episode_path = self.recorder.save_episode()
            
            # Actualizar en BD
            if self.episode_db_id and self.db_manager:
                self.db_manager.update_episode(
                    episode_id=self.episode_id,
                    end_time=datetime.fromtimestamp(end_time),
                    duration=duration
                )
                
                episode_info = self.recorder.get_current_episode_info()
                frame_count = episode_info["frame_count"] if episode_info else 0
                
                self.notifier.episode_saved(
                    self.episode_id,
                    duration,
                    frame_count,
                    self.episode_db_id
                )
            
            self.episode_active = False
            self.episode_id = None
            self.episode_db_id = None
            self.episode_start_time = None
            
            # Asegurar que el estado se actualice a False INMEDIATAMENTE
            system_status["motion_detected"] = False
            
            logger.info(f"Episodio cerrado, estado actualizado a calmado")
        except Exception as e:
            logger.error(f"Error cerrando episodio: {e}", exc_info=True)
            # Asegurar estado incluso si hay error
            system_status["motion_detected"] = False
    
    def start(self) -> None:
        """Inicia el servidor."""
        if self.is_running:
            logger.warning("Servidor ya está corriendo")
            return
        
        self.is_running = True
        
        # Iniciar thread de cámara
        self.camera_thread = threading.Thread(target=self._camera_thread_func, daemon=True)
        self.camera_thread.start()
        
        logger.info(f"Servidor iniciado en http://{self.host}:{self.port}")
    
    def stop(self) -> None:
        """Detiene el servidor."""
        self.is_running = False
        
        if self.camera_thread:
            self.camera_thread.join(timeout=5)
        
        if self.episode_active:
            self._close_episode()
        
        if self.camera:
            self.camera.stop()
        
        logger.info("Servidor detenido")
    
    def run(self) -> None:
        """Ejecuta el servidor con uvicorn."""
        import uvicorn
        self.start()
        try:
            uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")
        except KeyboardInterrupt:
            logger.info("Interrupción recibida, deteniendo servidor...")
        finally:
            self.stop()
