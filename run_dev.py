#!/usr/bin/env python
"""
Script para ejecutar los servidores de desarrollo de Django y Vue.js simultáneamente.
Uso: python run_dev.py
"""

import subprocess
import sys
import os
import signal
import threading

# Colores para la terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.END}")

# Obtener el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

processes = []

def run_command(name, cmd, cwd, color):
    """Ejecuta un comando y muestra su salida con prefijo de color"""
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        text=True,
        bufsize=1
    )
    processes.append(process)
    
    for line in iter(process.stdout.readline, ''):
        print(f"{color}[{name}]{Colors.END} {line}", end='')
    
    process.stdout.close()
    process.wait()

def signal_handler(sig, frame):
    """Maneja la señal de interrupción (Ctrl+C)"""
    print_colored("\n\nDeteniendo servidores...", Colors.YELLOW)
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)
        except:
            p.kill()
    print_colored("¡Servidores detenidos!", Colors.GREEN)
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print_colored("\n" + "="*60, Colors.BLUE)
    print_colored("     EWiki - Servidor de Desarrollo", Colors.BOLD)
    print_colored("="*60 + "\n", Colors.BLUE)
    
    print_colored("🚀 Iniciando servidores...\n", Colors.GREEN)
    print_colored(f"📦 Backend (Django):   http://localhost:8000/api/", Colors.BLUE)
    print_colored(f"🎨 Frontend (Vue.js):  http://localhost:5173/", Colors.GREEN)
    print_colored(f"🔧 Admin Panel:        http://localhost:5173/admin\n", Colors.YELLOW)
    print_colored("Presiona Ctrl+C para detener los servidores\n", Colors.YELLOW)
    print_colored("-"*60 + "\n", Colors.BLUE)
    
    # Iniciar backend
    backend_thread = threading.Thread(
        target=run_command,
        args=("Django", "python manage.py runserver 8000", BACKEND_DIR, Colors.BLUE)
    )
    backend_thread.daemon = True
    backend_thread.start()
    
    # Iniciar frontend
    frontend_thread = threading.Thread(
        target=run_command,
        args=("Vue", "npm run dev", FRONTEND_DIR, Colors.GREEN)
    )
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # Mantener el script corriendo
    try:
        while True:
            backend_thread.join(1)
            frontend_thread.join(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == '__main__':
    main()
