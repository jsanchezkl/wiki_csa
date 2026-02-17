#!/bin/bash
# Script para ejecutar el backend y frontend simultáneamente

echo "=============================================="
echo "🌐 EWiki Development Server"
echo "=============================================="

# Función para matar procesos hijos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturar señales de interrupción
trap cleanup SIGINT SIGTERM

# Directorio base
DIR="$(cd "$(dirname "$0")" && pwd)"

# Iniciar backend Django
echo "🚀 Iniciando Django backend..."
cd "$DIR/backend"
python manage.py runserver 8001 &
BACKEND_PID=$!

# Esperar a que Django inicie
sleep 2

# Iniciar frontend Vue.js
echo "🚀 Iniciando Vue.js frontend..."
cd "$DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=============================================="
echo "✅ Servidores iniciados!"
echo ""
echo "   Backend (Django):  http://localhost:8001"
echo "   Frontend (Vue.js): http://localhost:5173"
echo ""
echo "   Presiona Ctrl+C para detener"
echo "=============================================="
echo ""

# Esperar a que los procesos terminen
wait



