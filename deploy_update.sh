#!/bin/bash
set -e

echo "=== Desplegando Backend ==="
cd /Users/jefersoncamilosanchezlopez/Documents/Codex/Wiki/backend
gcloud builds submit --tag us-central1-docker.pkg.dev/proyectos-tech-476813/wiki-images/wiki-backend:latest .
gcloud run deploy wiki-backend --image=us-central1-docker.pkg.dev/proyectos-tech-476813/wiki-images/wiki-backend:latest --region=us-central1

echo "=== Desplegando Frontend ==="
cd /Users/jefersoncamilosanchezlopez/Documents/Codex/Wiki/frontend
gcloud builds submit --config cloudbuild.yaml --substitutions="_VITE_API_URL=https://wiki-backend-76764982675.us-central1.run.app/api,_IMAGE_NAME=us-central1-docker.pkg.dev/proyectos-tech-476813/wiki-images/wiki-frontend:latest"
gcloud run deploy wiki-frontend --image=us-central1-docker.pkg.dev/proyectos-tech-476813/wiki-images/wiki-frontend:latest --region=us-central1

echo "=== Despliegue completado ==="
echo "Frontend: https://wiki.csa-latam.com"
echo "Backend: https://wiki-backend-76764982675.us-central1.run.app"



