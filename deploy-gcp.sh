#!/bin/bash
# =============================================================================
# Script de despliegue para GCP Cloud Run + Cloud SQL
# Proyecto: proyectos-tech-476813
# =============================================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración del proyecto
PROJECT_ID="proyectos-tech-476813"
REGION="us-central1"
CLOUD_SQL_INSTANCE="wiki-db-instance"
DB_NAME="wiki_db"
DB_USER="wiki_user"
BACKEND_SERVICE="wiki-backend"
FRONTEND_SERVICE="wiki-frontend"

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}   Wiki GCP Deployment Script${NC}"
echo -e "${BLUE}   Proyecto: ${PROJECT_ID}${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Verificar que gcloud esté instalado
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI no está instalado${NC}"
    echo "Instálalo desde: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Configurar proyecto
echo -e "${YELLOW}[1/10] Configurando proyecto GCP...${NC}"
gcloud config set project $PROJECT_ID

# Habilitar APIs necesarias
echo -e "${YELLOW}[2/10] Habilitando APIs de GCP...${NC}"
gcloud services enable \
    run.googleapis.com \
    sqladmin.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com

# Crear instancia de Cloud SQL si no existe
echo -e "${YELLOW}[3/10] Verificando/Creando instancia Cloud SQL...${NC}"
if ! gcloud sql instances describe $CLOUD_SQL_INSTANCE --project=$PROJECT_ID &>/dev/null; then
    echo "Creando instancia Cloud SQL PostgreSQL..."
    gcloud sql instances create $CLOUD_SQL_INSTANCE \
        --database-version=POSTGRES_15 \
        --tier=db-f1-micro \
        --region=$REGION \
        --root-password="$(openssl rand -base64 32)" \
        --storage-type=SSD \
        --storage-size=10GB \
        --availability-type=zonal
    
    echo "Esperando a que la instancia esté lista..."
    sleep 30
else
    echo "Instancia Cloud SQL ya existe."
fi

# Obtener connection name
CLOUD_SQL_CONNECTION_NAME=$(gcloud sql instances describe $CLOUD_SQL_INSTANCE --format='value(connectionName)')
echo -e "${GREEN}Connection Name: ${CLOUD_SQL_CONNECTION_NAME}${NC}"

# Crear base de datos si no existe
echo -e "${YELLOW}[4/10] Creando base de datos...${NC}"
if ! gcloud sql databases describe $DB_NAME --instance=$CLOUD_SQL_INSTANCE &>/dev/null; then
    gcloud sql databases create $DB_NAME --instance=$CLOUD_SQL_INSTANCE
    echo "Base de datos creada."
else
    echo "Base de datos ya existe."
fi

# Crear usuario si no existe
echo -e "${YELLOW}[5/10] Configurando usuario de base de datos...${NC}"
DB_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=' | head -c 24)
if ! gcloud sql users list --instance=$CLOUD_SQL_INSTANCE | grep -q $DB_USER; then
    gcloud sql users create $DB_USER \
        --instance=$CLOUD_SQL_INSTANCE \
        --password=$DB_PASSWORD
    echo -e "${GREEN}Usuario creado con password: ${DB_PASSWORD}${NC}"
    echo "IMPORTANTE: Guarda esta contraseña de forma segura!"
else
    echo "Usuario ya existe. Actualizando contraseña..."
    gcloud sql users set-password $DB_USER \
        --instance=$CLOUD_SQL_INSTANCE \
        --password=$DB_PASSWORD
fi

# Guardar secrets en Secret Manager
echo -e "${YELLOW}[6/10] Configurando secretos...${NC}"

# Crear o actualizar secretos
echo -n "$DB_PASSWORD" | gcloud secrets create db-password --data-file=- 2>/dev/null || \
echo -n "$DB_PASSWORD" | gcloud secrets versions add db-password --data-file=-

# Solicitar API key de Gemini si no existe
if ! gcloud secrets describe gemini-api-key &>/dev/null; then
    echo -e "${YELLOW}Ingresa tu GEMINI_API_KEY:${NC}"
    read -s GEMINI_API_KEY
    echo -n "$GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=-
fi

# Generar Django Secret Key
DJANGO_SECRET_KEY=$(openssl rand -base64 50 | tr -d '/+=' | head -c 50)
echo -n "$DJANGO_SECRET_KEY" | gcloud secrets create django-secret-key --data-file=- 2>/dev/null || \
echo -n "$DJANGO_SECRET_KEY" | gcloud secrets versions add django-secret-key --data-file=-

# Crear Artifact Registry si no existe
echo -e "${YELLOW}[7/10] Configurando Artifact Registry...${NC}"
REPO_NAME="wiki-images"
if ! gcloud artifacts repositories describe $REPO_NAME --location=$REGION &>/dev/null; then
    gcloud artifacts repositories create $REPO_NAME \
        --repository-format=docker \
        --location=$REGION \
        --description="Wiki Docker images"
fi

# Build y push backend
echo -e "${YELLOW}[8/10] Construyendo y publicando imagen del backend...${NC}"
cd backend
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:latest .
cd ..

# Desplegar backend en Cloud Run
echo -e "${YELLOW}[9/10] Desplegando backend en Cloud Run...${NC}"
gcloud run deploy $BACKEND_SERVICE \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:latest \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --add-cloudsql-instances=$CLOUD_SQL_CONNECTION_NAME \
    --set-env-vars="USE_CLOUD_SQL=true" \
    --set-env-vars="DB_NAME=${DB_NAME}" \
    --set-env-vars="DB_USER=${DB_USER}" \
    --set-env-vars="DB_HOST=/cloudsql/${CLOUD_SQL_CONNECTION_NAME}" \
    --set-env-vars="DEBUG=false" \
    --set-secrets="DB_PASSWORD=db-password:latest" \
    --set-secrets="GEMINI_API_KEY=gemini-api-key:latest" \
    --set-secrets="DJANGO_SECRET_KEY=django-secret-key:latest" \
    --memory=512Mi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10 \
    --timeout=300

# Obtener URL del backend
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region=$REGION --format='value(status.url)')
echo -e "${GREEN}Backend URL: ${BACKEND_URL}${NC}"

# Actualizar CORS y ALLOWED_HOSTS
gcloud run services update $BACKEND_SERVICE \
    --region=$REGION \
    --set-env-vars="ALLOWED_HOSTS=localhost,127.0.0.1,.run.app" \
    --set-env-vars="CSRF_TRUSTED_ORIGINS=${BACKEND_URL}"

# Build y push frontend
echo -e "${YELLOW}[10/10] Construyendo y desplegando frontend...${NC}"
cd frontend
gcloud builds submit \
    --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:latest \
    --substitutions=_VITE_API_URL="${BACKEND_URL}/api" .
cd ..

# Desplegar frontend en Cloud Run
gcloud run deploy $FRONTEND_SERVICE \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:latest \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --memory=256Mi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10

# Obtener URL del frontend
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --region=$REGION --format='value(status.url)')

# Ejecutar migraciones
echo -e "${YELLOW}Ejecutando migraciones de base de datos...${NC}"
gcloud run jobs create wiki-migrations \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:latest \
    --region=$REGION \
    --add-cloudsql-instances=$CLOUD_SQL_CONNECTION_NAME \
    --set-env-vars="USE_CLOUD_SQL=true,DB_NAME=${DB_NAME},DB_USER=${DB_USER},DB_HOST=/cloudsql/${CLOUD_SQL_CONNECTION_NAME}" \
    --set-secrets="DB_PASSWORD=db-password:latest,DJANGO_SECRET_KEY=django-secret-key:latest" \
    --command="python" \
    --args="manage.py,migrate" 2>/dev/null || true

gcloud run jobs execute wiki-migrations --region=$REGION --wait

# Actualizar CORS del backend con URL del frontend
gcloud run services update $BACKEND_SERVICE \
    --region=$REGION \
    --update-env-vars="CORS_ALLOWED_ORIGINS=${FRONTEND_URL},http://localhost:5173"

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}   ¡Despliegue completado exitosamente!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${BLUE}URLs de la aplicación:${NC}"
echo -e "  Frontend: ${GREEN}${FRONTEND_URL}${NC}"
echo -e "  Backend API: ${GREEN}${BACKEND_URL}/api${NC}"
echo ""
echo -e "${BLUE}Base de datos:${NC}"
echo -e "  Instancia: ${CLOUD_SQL_INSTANCE}"
echo -e "  Base de datos: ${DB_NAME}"
echo -e "  Usuario: ${DB_USER}"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo "  1. Visita ${FRONTEND_URL} para ver la Wiki"
echo "  2. Crea el superusuario ejecutando:"
echo "     gcloud run jobs create create-superuser \\"
echo "       --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:latest \\"
echo "       --region=$REGION \\"
echo "       --add-cloudsql-instances=$CLOUD_SQL_CONNECTION_NAME \\"
echo "       --set-env-vars='USE_CLOUD_SQL=true,DB_NAME=${DB_NAME},DB_USER=${DB_USER},DB_HOST=/cloudsql/${CLOUD_SQL_CONNECTION_NAME}' \\"
echo "       --set-secrets='DB_PASSWORD=db-password:latest,DJANGO_SECRET_KEY=django-secret-key:latest' \\"
echo "       --command='python' \\"
echo "       --args='manage.py,shell,-c,from api.views import create_initial_superuser; create_initial_superuser()'"
echo ""




