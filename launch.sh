#!/bin/bash

# Script de lancement pour Co-pilote de Carrière
# Usage : ./launch.sh

set -e

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: ./launch.sh [port]"
    exit 0
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Erreur : python3 n'est pas installé.${NC}"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo -e "${RED}Erreur : pip n'est pas installé.${NC}"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo -e "${GREEN}Création de l'environnement virtuel...${NC}"
    python3 -m venv venv
fi

if ! source venv/bin/activate; then
    echo -e "${RED}Erreur lors de l'activation de l'environnement virtuel.${NC}"
    exit 1
fi

if ! python -m streamlit --version &> /dev/null; then
    echo -e "${GREEN}Installation de Streamlit...${NC}"
    pip install streamlit
fi

if [ ! -f "venv/.deps_installed" ] || [ requirements.txt -nt venv/.deps_installed ]; then
    echo -e "${GREEN}Installation des dépendances...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

PORT=${1:-8501}

if [ -f "src/main.py" ]; then
    echo -e "${GREEN}Lancement de l'application Co-pilote de Carrière...${NC}"
    streamlit run src/main.py --server.port $PORT
else
    echo -e "${RED}Erreur : src/main.py introuvable.${NC}"
    exit 1
fi
