#!/usr/bin/env python3
"""Script de prueba local para cámara (ejecutar directamente en Raspberry Pi).

Este script verifica el funcionamiento de la cámara cuando se ejecuta
directamente en la Raspberry Pi.
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import time
import cv2
import numpy as np


def test_camera_basic():
    """Prueba básica de la cámara."""
    print("=" * 60)
    print("📷 PRUEBA BÁSICA DE CÁMARA")
    print("=" * 60)
    
    try:
        from camera.imx219_handler import IMX219Handler
        
        print("\n1. Inicializando cámara...")
        camera = IMX219Handler()
        print("   ✅ Cámara inicializada")
        
        print("\n2. Iniciando captura...")
        camera.start()
        print("   ✅ Captura iniciada")
        
        print("\n3. Esperando calentamiento (2 segundos)...")
        time.sleep(2)
        
        print("\n4. Capturando 5 frames de prueba...")
        for i in range(5):
            frame = camera.capture_frame()
            if frame is not None:
                print(f"   ✅ Frame {i+1}: shape={frame.shape}, dtype={frame.dtype}, "
                      f"min={frame.min()}, max={frame.max()}")
            else:
                print(f"   ❌ Frame {i+1}: Error al capturar")
                break
            time.sleep(0.5)
        
        print("\n5. Deteniendo cámara...")
        camera.stop()
        print("   ✅ Cámara detenida")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\n💡 Asegúrate de estar en el entorno virtual:")
        print("   source venv/bin/activate")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_motion_detection():
    """Prueba de detección de movimiento."""
    print("\n" + "=" * 60)
    print("🔍 PRUEBA DE DETECCIÓN DE MOVIMIENTO")
    print("=" * 60)
    
    try:
        from camera.imx219_handler import IMX219Handler
        from detection.motion_detector import MotionDetector
        
        print("\n1. Inicializando componentes...")
        camera = IMX219Handler()
        detector = MotionDetector(threshold=30, min_area=500)
        
        camera.start()
        time.sleep(2)
        
        print("\n2. Estableciendo fondo...")
        frame = camera.capture_frame()
        if frame is None:
            print("   ❌ No se pudo capturar frame para fondo")
            camera.stop()
            return False
        
        detector.set_background(frame)
        print("   ✅ Fondo establecido")
        
        print("\n3. Probando detección (10 frames)...")
        print("   💡 Mueve algo delante de la cámara para probar detección")
        
        motion_count = 0
        for i in range(10):
            frame = camera.capture_frame()
            if frame is None:
                continue
            
            motion, annotated = detector.detect(frame)
            if motion:
                motion_count += 1
                print(f"   ⚠️  Frame {i+1}: Movimiento detectado!")
            else:
                print(f"   ✅ Frame {i+1}: Sin movimiento")
            
            time.sleep(0.5)
        
        print(f"\n   📊 Movimiento detectado en {motion_count}/10 frames")
        
        camera.stop()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBAS LOCALES - CÁMARA IMX219")
    print("=" * 60)
    print("\n⚠️  Este script debe ejecutarse directamente en la Raspberry Pi")
    print("   con la cámara conectada.\n")
    
    results = {}
    
    # Prueba básica
    results['basic'] = test_camera_basic()
    
    # Prueba de detección
    if results['basic']:
        results['detection'] = test_motion_detection()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ¡Todas las pruebas pasaron!")
    else:
        print("\n⚠️  Algunas pruebas fallaron.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
