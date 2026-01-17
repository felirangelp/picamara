"""Tests para el módulo de base de datos."""

import pytest
import tempfile
import os
from datetime import datetime
from src.database.db_manager import DatabaseManager


@pytest.fixture
def temp_db():
    """Fixture para crear una BD temporal."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    db = DatabaseManager(db_path=db_path)
    yield db
    
    # Limpiar
    os.unlink(db_path)


def test_database_initialization(temp_db):
    """Test de inicialización de BD."""
    assert os.path.exists(temp_db.db_path)


def test_add_episode(temp_db):
    """Test de añadir episodio."""
    episode_id = "test_episode_001"
    file_path = "data/episodes/test_episode_001"
    start_time = datetime.now()
    
    db_id = temp_db.add_episode(
        episode_id=episode_id,
        file_path=file_path,
        start_time=start_time,
        motion_detected=True
    )
    
    assert db_id > 0


def test_get_episodes(temp_db):
    """Test de obtener episodios."""
    # Añadir algunos episodios
    for i in range(3):
        temp_db.add_episode(
            episode_id=f"ep_{i}",
            file_path=f"path_{i}",
            start_time=datetime.now(),
            motion_detected=(i % 2 == 0)
        )
    
    episodes = temp_db.get_episodes(limit=10)
    assert len(episodes) == 3


def test_add_event(temp_db):
    """Test de añadir evento."""
    event_id = temp_db.add_event(
        event_type="test_event",
        message="Test message",
        severity="info"
    )
    assert event_id > 0


def test_get_stats(temp_db):
    """Test de obtener estadísticas."""
    # Añadir algunos datos
    temp_db.add_episode(
        episode_id="ep_1",
        file_path="path_1",
        start_time=datetime.now(),
        motion_detected=True
    )
    temp_db.add_event("test", "message", "info")
    
    stats = temp_db.get_stats()
    assert stats['total_episodes'] == 1
    assert stats['total_events'] == 1
