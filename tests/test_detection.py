"""Tests para el módulo de detección de movimiento."""

import pytest
import numpy as np
from src.detection.motion_detector import MotionDetector


def test_motion_detector_initialization():
    """Test de inicialización del detector."""
    detector = MotionDetector(threshold=30, min_area=500)
    assert detector.threshold == 30
    assert detector.min_area == 500
    assert not detector.background_set


def test_set_background():
    """Test de establecimiento de fondo."""
    detector = MotionDetector()
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    detector.set_background(frame)
    assert detector.background_set
    assert detector.background is not None


def test_detect_no_motion():
    """Test de detección sin movimiento."""
    detector = MotionDetector(threshold=30, min_area=500)
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    detector.set_background(frame)
    
    # Mismo frame (no debería haber movimiento)
    motion, annotated = detector.detect(frame)
    assert not motion


def test_update_config():
    """Test de actualización de configuración."""
    detector = MotionDetector(threshold=30, min_area=500)
    detector.update_config(threshold=50, min_area=1000)
    assert detector.threshold == 50
    assert detector.min_area == 1000
