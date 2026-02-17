# EWiki - Corporate Knowledge Base

Sistema Wiki corporativo construido con Vue.js (frontend) y Django (backend).

## 🚀 Características

- **Dashboard interactivo** con departamentos y actualizaciones recientes
- **Sistema de navegación dinámico** con menús colapsables
- **Páginas Wiki** con secciones organizadas
- **Módulo de Administración completo**:
  - Gestión de departamentos
  - Editor de texto enriquecido para crear contenido
  - CRUD de páginas wiki
  - Configuración del sitio

## 📁 Estructura del Proyecto

```
Wiki/
├── backend/                 # Django REST API
│   ├── api/                # App principal
│   │   ├── models.py       # Modelos de datos
│   │   ├── views.py        # Vistas API
│   │   ├── serializers.py  # Serializadores
│   │   └── urls.py         # Rutas API
│   ├── wiki_api/           # Configuración Django
│   └── manage.py
│
├── frontend/               # Vue.js SPA
│   ├── src/
│   │   ├── api/           # Cliente API
│   │   ├── components/    # Componentes Vue
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── RichTextEditor.vue
│   │   ├── views/         # Vistas principales
│   │   │   ├── Home.vue
│   │   │   ├── WikiPage.vue
│   │   │   └── admin/     # Vistas de administración
│   │   │       ├── AdminDashboard.vue
│   │   │       ├── AdminDepartments.vue
│   │   │       ├── AdminDepartmentForm.vue
│   │   │       ├── AdminPages.vue
│   │   │       ├── AdminPageForm.vue
│   │   │       └── AdminSettings.vue
│   │   └── router/        # Configuración de rutas
│   └── package.json
│
├── run_dev.py             # Script para ejecutar ambos servidores
└── README.md
```

## ⚙️ Instalación

### Requisitos previos
- Python 3.9+
- Node.js 18+
- npm o yarn

### Backend (Django)

```bash
cd backend

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Cargar datos iniciales
python manage.py seed_data

# Iniciar servidor
python manage.py runserver 8000
```

### Frontend (Vue.js)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

## 🏃 Ejecutar Ambos Servidores

### Opción 1: Script Python

```bash
python run_dev.py
```

### Opción 2: Manualmente

Terminal 1:
```bash
cd backend && python manage.py runserver 8000
```

Terminal 2:
```bash
cd frontend && npm run dev
```

## 🌐 URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Panel de Admin**: http://localhost:5173/admin

## 📋 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/ | Información de la API |
| GET | /api/dashboard/ | Datos del dashboard |
| GET | /api/sidebar/ | Menú lateral |
| GET/POST | /api/departments/ | Listar/Crear departamentos |
| GET/PUT/DELETE | /api/departments/{id}/ | Detalle departamento |
| GET/POST | /api/pages/ | Listar/Crear páginas |
| GET/PUT/DELETE | /api/pages/{slug}/ | Detalle página |
| GET/POST | /api/sections/ | Gestionar secciones |
| GET/PUT | /api/settings/ | Configuración del sitio |
| GET | /api/admin/stats/ | Estadísticas de admin |

## 🎨 Acceso al Panel de Administración

1. Abre http://localhost:5173
2. Haz clic en tu perfil (esquina superior derecha)
3. Selecciona "Administrar"

### Funcionalidades del Admin:
- **Dashboard**: Estadísticas generales
- **Departamentos**: CRUD de departamentos
- **Páginas**: Crear/editar páginas con editor de texto enriquecido
- **Configuración**: Personalizar mensaje de bienvenida y datos del sitio

## 🔧 Editor de Texto Enriquecido

El editor soporta:
- Formato de texto (negrita, cursiva, subrayado)
- Encabezados (H2, H3, H4)
- Listas ordenadas y no ordenadas
- Alineación de texto
- Insertar imágenes por URL
- Insertar enlaces
- Bloques de código
- Citas
- Líneas horizontales

## 📦 Tecnologías

### Backend
- Django 4.2
- Django REST Framework
- django-cors-headers
- SQLite (desarrollo)

### Frontend
- Vue.js 3
- Vue Router
- Vite
- Tailwind CSS
- TipTap (editor de texto)
- Axios

## 🤝 Contribución

1. Haz fork del repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

MIT
