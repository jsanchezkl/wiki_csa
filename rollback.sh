#!/bin/bash
# =============================================================================
# Script de ROLLBACK para GCP Cloud Run
# Uso: ./rollback.sh [timestamp] 
# Ejemplo: ./rollback.sh 20260217_184500
# Sin timestamp: Lista las versiones disponibles
# =============================================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_ID="proyectos-tech-476813"
REGION="us-central1"
BACKEND_SERVICE="wiki-backend"
FRONTEND_SERVICE="wiki-frontend"
REPO_NAME="wiki-images"

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}   Wiki Rollback Script${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Si no se proporciona timestamp, listar versiones disponibles
if [ -z "$1" ]; then
    echo -e "${YELLOW}Versiones de BACKEND disponibles:${NC}"
    gcloud artifacts docker tags list \
        ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE} \
        --format="table(tag,version.createTime)" \
        --sort-by=~version.createTime \
        --limit=10
    
    echo ""
    echo -e "${YELLOW}Versiones de FRONTEND disponibles:${NC}"
    gcloud artifacts docker tags list \
        ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE} \
        --format="table(tag,version.createTime)" \
        --sort-by=~version.createTime \
        --limit=10
    
    echo ""
    echo -e "${BLUE}Para hacer rollback, ejecuta:${NC}"
    echo "  ./rollback.sh <timestamp>"
    echo "  Ejemplo: ./rollback.sh backup-20260217_184500"
    exit 0
fi

ROLLBACK_TAG=$1

echo -e "${YELLOW}⚠️  Vas a hacer ROLLBACK a la versión: ${ROLLBACK_TAG}${NC}"
echo -e "${YELLOW}   ¿Estás seguro? (s/n)${NC}"
read -r CONFIRM
if [ "$CONFIRM" != "s" ]; then
    echo "Rollback cancelado."
    exit 0
fi

# Rollback backend
echo -e "${BLUE}[1/2] Restaurando backend...${NC}"
BACKEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${BACKEND_SERVICE}:${ROLLBACK_TAG}"
if gcloud artifacts docker images describe "$BACKEND_IMAGE" &>/dev/null; then
    gcloud run deploy $BACKEND_SERVICE \
        --image="$BACKEND_IMAGE" \
        --region=$REGION
    echo -e "${GREEN}✅ Backend restaurado${NC}"
else
    echo -e "${RED}❌ No se encontró imagen de backend: ${BACKEND_IMAGE}${NC}"
fi

# Rollback frontend
echo -e "${BLUE}[2/2] Restaurando frontend...${NC}"
FRONTEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${FRONTEND_SERVICE}:${ROLLBACK_TAG}"
if gcloud artifacts docker images describe "$FRONTEND_IMAGE" &>/dev/null; then
    gcloud run deploy $FRONTEND_SERVICE \
        --image="$FRONTEND_IMAGE" \
        --region=$REGION
    echo -e "${GREEN}✅ Frontend restaurado${NC}"
else
    echo -e "${RED}❌ No se encontró imagen de frontend: ${FRONTEND_IMAGE}${NC}"
fi

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}   ✅ Rollback completado${NC}"
echo -e "${GREEN}==========================================${NC}"

