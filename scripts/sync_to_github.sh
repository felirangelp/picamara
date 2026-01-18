#!/bin/bash
# Script para sincronizar cambios locales con GitHub

set -e

echo "============================================================"
echo "📤 SINCRONIZANDO CON GITHUB"
echo "============================================================"
echo ""

# Verificar que estamos en el directorio del proyecto
if [ ! -f "README.md" ] || [ ! -d ".git" ]; then
    echo "❌ Error: Debes ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar estado de Git
echo "1. Verificando estado de Git..."
git status --short

echo ""
read -p "¿Deseas continuar con el commit y push? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operación cancelada"
    exit 1
fi

# Agregar todos los cambios
echo ""
echo "2. Agregando cambios..."
git add .

# Hacer commit
echo ""
echo "3. Creando commit..."
read -p "Mensaje del commit (o Enter para mensaje automático): " commit_message

if [ -z "$commit_message" ]; then
    commit_message="chore: Actualización automática - $(date '+%Y-%m-%d %H:%M:%S')"
fi

git commit -m "$commit_message" || {
    echo "⚠️  No hay cambios para commitear"
    exit 0
}

# Push a GitHub
echo ""
echo "4. Subiendo cambios a GitHub..."
git push origin main

echo ""
echo "============================================================"
echo "✅ Cambios sincronizados con GitHub"
echo "============================================================"
echo ""
echo "Para actualizar en Raspberry Pi, ejecuta:"
echo "  ssh picamara@picamara.local 'cd ~/Pi_camara && git pull'"
echo "============================================================"
