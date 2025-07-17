#!/bin/bash

# Script de lancement pour Co-pilote de Carrière
# Usage : ./launch.sh

set -e

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Activation de l'environnement virtuel
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Création de l'environnement virtuel...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate

# 2. Installation des dépendances
if [ ! -f "venv/.deps_installed" ] || [ requirements.txt -nt venv/.deps_installed ]; then
    echo -e "${GREEN}Installation des dépendances...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

# 3. Lancement de l'application Streamlit
if [ -f "src/main.py" ]; then
    echo -e "${GREEN}Lancement de l'application Co-pilote de Carrière...${NC}"
    streamlit run src/main.py
else
    echo -e "${RED}Erreur : src/main.py introuvable.${NC}"
    exit 1
fi
