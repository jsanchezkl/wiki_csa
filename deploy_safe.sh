#!/bin/bash
# =============================================================================
# Script de despliegue SEGURO para GCP Cloud Run
# Este script guarda la versión anterior antes de desplegar
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
BACKEND_SERVICE="wiki-backend"
FRONTEND_SERVICE="wiki-frontend"
REPO_NAME="wiki-images"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}   Wiki SAFE Deployment Script${NC}"
echo -e "${BLUE}   Timestamp: ${TIMESTAMP}${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Función para guardar versión actual como backup
backup_current_version() {
    local service=$1
    echo -e "${YELLOW}📦 Guardando backup de ${service}...${NC}"
    
    # Obtener el digest de la imagen actual
    CURRENT_DIGEST=$(gcloud run services describe $service --region=$REGION --format='value(spec.template.spec.containers[0].image)' 2>/dev/null || echo "")
    
    if [ -n "$CURRENT_DIGEST" ]; then
        echo -e "${GREEN}  Versión actual guardada: ${CURRENT_DIGEST}${NC}"
        echo "$CURRENT_DIGEST" > ".backup_${service}_${TIMESTAMP}.txt"
        
        # Taggear la imagen actual como backup
        gcloud artifacts docker tags add \
            "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${service}:latest" \
            "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${service}:backup-${TIMESTAMP}" 2>/dev/null || true
        echo -e "${GREEN}  ✅ Backup creado como: ${service}:backup-${TIMESTAMP}${NC}"
    else
        echo -e "${YELLOW}  ⚠️ No hay versión anterior para respaldar${NC}"
    fi
}

# Función para rollback
rollback() {
    echo -e "${RED}==========================================${NC}"
    echo -e "${RED}   INICIANDO ROLLBACK${NC}"
    echo -e "${RED}==========================================${NC}"
    
    for service in $BACKEND_SERVICE $FRONTEND_SERVICE; do
        BACKUP_FILE=".backup_${service}_${TIMESTAMP}.txt"
        if [ -f "$BACKUP_FILE" ]; then
            BACKUP_IMAGE=$(cat "$BACKUP_FILE")
            echo -e "${YELLOW}Restaurando ${service} a: ${BACKUP_IMAGE}${NC}"
            gcloud run deploy $service \
                --image="$BACKUP_IMAGE" \
                --region=$REGION
            echo -e "${GREEN}✅ ${service} restaurado${NC}"
        fi
    done
}

# Trap para rollback en caso de error
trap 'echo -e "${RED}❌ Error detectado. ¿Deseas hacer rollback? (s/n)${NC}"; read answer; if [ "$answer" = "s" ]; then rollback; fi' ERR

# Confirmar despliegue
echo -e "${YELLOW}⚠️  Este script desplegará cambios a PRODUCCIÓN en GCP${NC}"
echo -e "${YELLOW}   ¿Deseas continuar? (s/n)${NC}"
read -r CONFIRM
if [ "$CONFIRM" != "s" ]; then
    echo "Despliegue cancelado."
    exit 0
fi

# Paso 1: Backup de versiones actuales
echo -e "${BLUE}[1/5] Creando backups de versiones actuales...${NC}"
backup_current_version $BACKEND_SERVICE
backup_current_version $FRONTEND_SERVICE

# Paso 2: Build y push backend
echo -e "${BLUE}[2/5] Construyendo backend...${NC}"
cd /Users/jefersoncamilosanchezlopez/Documents/Codex/Wiki/backend
gcloud builds submit \
    --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:latest \
    --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:${TIMESTAMP} .

# Paso 3: Desplegar backend
echo -e "${BLUE}[3/5] Desplegando backend...${NC}"
gcloud run deploy $BACKEND_SERVICE \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:latest \
    --region=$REGION

# Paso 4: Build y push frontend
echo -e "${BLUE}[4/5] Construyendo frontend...${NC}"
cd /Users/jefersoncamilosanchezlopez/Documents/Codex/Wiki/frontend
BACKEND_URL="https://wiki-backend-76764982675.us-central1.run.app/api"
gcloud builds submit \
    --config cloudbuild.yaml \
    --substitutions="_VITE_API_URL=${BACKEND_URL},_IMAGE_NAME=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:latest"

# También crear tag con timestamp
gcloud artifacts docker tags add \
    "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:latest" \
    "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:${TIMESTAMP}" 2>/dev/null || true

# Paso 5: Desplegar frontend
echo -e "${BLUE}[5/5] Desplegando frontend...${NC}"
gcloud run deploy $FRONTEND_SERVICE \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:latest \
    --region=$REGION

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}   ✅ Despliegue completado exitosamente${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${BLUE}URLs:${NC}"
echo -e "  Frontend: ${GREEN}https://wiki.csa-latam.com${NC}"
echo -e "  Backend:  ${GREEN}https://wiki-backend-76764982675.us-central1.run.app${NC}"
echo ""
echo -e "${BLUE}Versiones desplegadas:${NC}"
echo -e "  Tag: ${TIMESTAMP}"
echo ""
echo -e "${YELLOW}Para ROLLBACK ejecuta:${NC}"
echo -e "  ./rollback.sh ${TIMESTAMP}"

