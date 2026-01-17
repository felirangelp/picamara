// Estado de la aplicación
let statusUpdateInterval = null;
let episodesUpdateInterval = null;

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('Pi Camera Security System - Frontend iniciado');
    
    // Iniciar actualizaciones automáticas
    startStatusUpdates();
    startEpisodesUpdates();
    
    // Configurar formulario
    setupConfigForm();
    
    // Manejar reconexión del stream
    setupVideoStreamReconnect();
});

// Actualizar estado del sistema
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        // Actualizar indicadores
        updateMotionStatus(data.motion_detected);
        document.getElementById('motion-count').textContent = data.total_episodes || 0;
        document.getElementById('fps').textContent = data.fps.toFixed(1);
        document.getElementById('uptime').textContent = formatUptime(data.uptime_seconds);
        
        // Actualizar indicador de estado
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        
        if (data.camera_active) {
            statusDot.className = 'status-dot active';
            statusText.textContent = 'Activo';
        } else {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Inactivo';
        }
    } catch (error) {
        console.error('Error actualizando estado:', error);
        document.getElementById('status-dot').className = 'status-dot error';
        document.getElementById('status-text').textContent = 'Error de conexión';
    }
}

// Actualizar estado de movimiento
function updateMotionStatus(motionDetected) {
    const motionStatus = document.getElementById('motion-status');
    if (motionDetected) {
        motionStatus.textContent = '⚠️ Movimiento Detectado';
        motionStatus.className = 'motion-detected';
    } else {
        motionStatus.textContent = '✅ Calmado';
        motionStatus.className = 'motion-calm';
    }
}

// Formatear uptime
function formatUptime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

// Actualizar lista de episodios
async function updateEpisodes() {
    try {
        const response = await fetch('/api/episodes?limit=5&motion_only=true');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const episodes = await response.json();
        
        const episodesList = document.getElementById('episodes-list');
        
        if (episodes.length === 0) {
            episodesList.innerHTML = '<p class="loading">No hay episodios aún</p>';
            return;
        }
        
        episodesList.innerHTML = episodes.map(episode => `
            <div class="episode-item">
                <h4>${episode.episode_id}</h4>
                <p>Inicio: ${formatDate(episode.start_time)}</p>
                <p>Duración: ${episode.duration_seconds ? episode.duration_seconds.toFixed(1) + 's' : 'En curso'}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error actualizando episodios:', error);
        document.getElementById('episodes-list').innerHTML = 
            '<p class="loading">Error cargando episodios</p>';
    }
}

// Formatear fecha
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('es-ES');
}

// Configurar formulario de configuración
function setupConfigForm() {
    const form = document.getElementById('config-form');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            motion_threshold: parseInt(document.getElementById('motion-threshold').value),
            min_area: parseInt(document.getElementById('min-area').value)
        };
        
        try {
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            alert('Configuración actualizada correctamente');
            console.log('Configuración actualizada:', result);
        } catch (error) {
            console.error('Error actualizando configuración:', error);
            alert('Error al actualizar configuración: ' + error.message);
        }
    });
}

// Configurar reconexión del stream de video
function setupVideoStreamReconnect() {
    const videoStream = document.getElementById('video-stream');
    
    videoStream.addEventListener('error', function() {
        console.warn('Error en stream de video, intentando reconectar...');
        setTimeout(function() {
            videoStream.src = '/video_feed?t=' + new Date().getTime();
        }, 2000);
    });
    
    videoStream.addEventListener('load', function() {
        console.log('Stream de video conectado');
    });
}

// Iniciar actualizaciones de estado
function startStatusUpdates() {
    updateStatus(); // Actualizar inmediatamente
    statusUpdateInterval = setInterval(updateStatus, 1000); // Cada segundo
}

// Iniciar actualizaciones de episodios
function startEpisodesUpdates() {
    updateEpisodes(); // Actualizar inmediatamente
    episodesUpdateInterval = setInterval(updateEpisodes, 5000); // Cada 5 segundos
}

// Limpiar intervalos al salir
window.addEventListener('beforeunload', function() {
    if (statusUpdateInterval) {
        clearInterval(statusUpdateInterval);
    }
    if (episodesUpdateInterval) {
        clearInterval(episodesUpdateInterval);
    }
});
