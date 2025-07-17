# 🤖 Co-pilote de Carrière

Votre assistant IA tout-en-un pour optimiser la recherche d'emploi, la gestion des candidatures, la génération de documents personnalisés, la préparation aux entretiens et l'analyse de vos performances.

---

## 🚀 Fonctionnalités principales

- **Tableau de bord Notion** : Suivi centralisé des candidatures
- **Générateur de CV/LM** : Création de documents personnalisés à partir de votre CV PDF et d'une description de poste
- **Préparation aux entretiens** : Génération de questions et briefing entreprise via IA
- **Analyse des performances** : Statistiques et graphiques interactifs
- **Découverte multi-sources** : Recherche d'offres sur LinkedIn, Indeed, Apec, Pôle Emploi, Gmail...
- **Gestion dynamique des préférences** : Interface de configuration intuitive
- **Planification d'entretien** : Création d'événements Google Calendar
- **Logs et configuration** : Suivi des actions, gestion des clés API, aide intégrée

---

## 🛠️ Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/aureseth/Copilot-career.git
   cd Copilot-career
   ```
2. **Lancer le script d'installation et de démarrage**
   ```bash
   ./launch.sh
   ```
   (Le script crée l'environnement virtuel, installe les dépendances et lance l'app)

---

## ⚙️ Configuration

- **Clés API à fournir** :
  - OpenAI (https://platform.openai.com/api-keys)
  - Notion (https://www.notion.com/my-integrations)
  - Google (credentials.json et token.json dans `config/`)
- **Fichier de préférences** :
  - `config/preferences.yaml` (modifiable via l'UI)
- **Page « Configuration & Connexions »** :
  - Permet de saisir/corriger les clés API et d'obtenir de l'aide

---

## 💡 Utilisation

1. **Configurer vos préférences** dans la barre latérale (mots-clés, localisation, sources...)
2. **Lancer une recherche d'offres** (bouton 🚀)
3. **Gérer vos candidatures** dans le tableau de bord (statuts, détails...)
4. **Générer un CV/LM personnalisé** à partir d'un PDF et d'une description de poste
5. **Préparer vos entretiens** (questions IA, briefing entreprise)
6. **Analyser vos performances** (statistiques, graphiques)
7. **Planifier vos entretiens** dans Google Calendar
8. **Consulter les logs** pour le suivi technique

---

## 📸 Captures d'écran

*À compléter avec des screenshots de l'interface Streamlit*

---

## 📚 Structure du projet

```
Co-pilote de Carrière/
├── src/
│   ├── main.py                # Interface Streamlit principale
│   ├── config.py              # Gestion centralisée de la config
│   ├── logger.py              # Logging global
│   ├── modules/               # Modules métiers (Notion, génération, entretien...)
│   └── tools/                 # Outils réutilisables (scraping, Google, Notion...)
├── config/                    # Fichiers de config et secrets
├── data/                      # Données utilisateur (CV, etc.)
├── logs/                      # Fichiers de logs
├── requirements.txt           # Dépendances Python
├── launch.sh                  # Script de lancement automatisé
└── README.md                  # Documentation
```

---

## ❓ FAQ

- **Comment obtenir mes clés API ?**
  > Voir la page « Configuration & Connexions » dans l'UI pour les liens et instructions détaillées.
- **Comment ajouter une nouvelle source d'offres ?**
  > Implémentez une fonction de scraping dans `tools/scraping_tools.py` et activez-la dans les préférences.
- **Comment réinitialiser mes préférences ?**
  > Modifiez ou supprimez le fichier `config/preferences.yaml`.
- **Où trouver les logs ?**
  > Dans le dossier `logs/` ou via la page « Logs » de l'interface.

---

## 🗺️ Roadmap & Idées d'amélioration

- Scraping réel pour Indeed, Apec, Pôle Emploi
- Export PDF/Word des documents générés
- Notifications email/Slack
- Mode multi-utilisateur
- Déploiement cloud (Streamlit Cloud, Heroku...)
- Amélioration continue de l'UX/UI

---

## 👨‍💻 Contribuer

Les PR et suggestions sont les bienvenues ! Merci de lire le code de conduite et d’ouvrir une issue pour toute demande.

---

## 📄 Licence

MIT
