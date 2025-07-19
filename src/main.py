# Fichier principal de l'application Streamlit

import streamlit as st
import os
from modules import database, generator, interview, analytics, discovery, scheduler
import config
from logger import logger
from openai import OpenAI

STATUTS = ["Découvert", "Appliqué", "Entretien", "Offre", "Rejeté"]
STATUT_COLORS = {
    "Découvert": "#95a5a6",
    "Appliqué": "#2980b9",
    "Entretien": "#27ae60",
    "Offre": "#f1c40f",
    "Rejeté": "#e74c3c",
}


def colored_status(status):
    color = STATUT_COLORS.get(status, "#7f8c8d")
    return f"<span style='background-color:{color};color:white;padding:4px 10px;border-radius:8px'>{status}</span>"


def show_error(msg, help_url=None):
    st.error(msg)
    logger.error(msg)
    if help_url:
        st.markdown(f"[Aide]({help_url})")


def onboarding():
    st.title("👋 Bienvenue sur Co-pilote de Carrière !")
    st.markdown(
        """
Bienvenue dans votre assistant IA pour la recherche d'emploi.

Voici comment bien démarrer :

1. **Configurer vos clés API** (OpenAI, Notion, Google)
2. **Définir vos préférences de recherche** (mots-clés, localisation, sources)
3. **Découvrir les fonctionnalités principales**

---
"""
    )
    st.info(
        "Vous pourrez retrouver ce guide à tout moment dans l'onglet '🧑‍💼 Guide Utilisateur'."
    )
    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = 1
    step = st.session_state["onboarding_step"]
    steps = {
        1: "Configuration des connexions",
        2: "Préférences de recherche",
        3: "Découverte des fonctionnalités",
    }
    st.progress(step / len(steps))
    if step == 1:
        st.subheader("1️⃣ Configuration des connexions API")
        services = ["OpenAI", "Notion", "Google"]
        # Statut et messages en session
        for s in services:
            st.session_state.setdefault(f"{s.lower()}_status", "❌")
            st.session_state.setdefault(f"{s.lower()}_msg", "Non testé")
        # Tableau de statut
        st.table(
            {
                "Service": services,
                "Statut": [st.session_state[f"{s.lower()}_status"] for s in services],
                "Message": [st.session_state[f"{s.lower()}_msg"] for s in services],
            }
        )
        # Affichage/masquage des clés (checkbox hors du form)
        st.session_state.setdefault("show_openai", False)
        st.session_state.setdefault("show_notion", False)
        st.session_state.setdefault("show_google", False)
        show_openai = st.checkbox(
            "Afficher la clé OpenAI", value=st.session_state["show_openai"]
        )
        st.session_state["show_openai"] = show_openai
        show_notion = st.checkbox(
            "Afficher la clé Notion", value=st.session_state["show_notion"]
        )
        st.session_state["show_notion"] = show_notion
        show_google = st.checkbox(
            "Afficher la clé Google", value=st.session_state["show_google"]
        )
        st.session_state["show_google"] = show_google
        with st.form("api_form_onboarding"):
            openai_key = st.text_input(
                "Clé API OpenAI",
                value=st.session_state.get("openai_key", ""),
                type="default" if show_openai else "password",
                help="Clé API OpenAI. Obtenez-la ici : https://platform.openai.com/api-keys",
            )
            if st.session_state["openai_status"] == "❌":
                st.error(st.session_state["openai_msg"])
                st.markdown("[Aide OpenAI](https://platform.openai.com/api-keys)")
            notion_key = st.text_input(
                "Clé API Notion",
                value=st.session_state.get("notion_key", ""),
                type="default" if show_notion else "password",
                help="Clé d'intégration Notion. Créez-la ici : https://www.notion.com/my-integrations (puis partagez votre base avec l'intégration)",
            )
            if st.session_state["notion_status"] == "❌":
                st.error(st.session_state["notion_msg"])
                st.markdown("[Aide Notion](https://www.notion.com/my-integrations)")
            st.text_input(
                "Google (credentials.json/token.json dans config/)",
                value=st.session_state.get("google_info", ""),
                type="default" if show_google else "password",
                help="Générez credentials.json/token.json via Google Cloud Console : https://console.cloud.google.com/apis/credentials. Placez-les dans le dossier config/.",
            )
            # Upload direct Google
            st.markdown("**Upload direct des fichiers Google (optionnel)**")
            cred_file = st.file_uploader(
                "Uploader credentials.json", type=["json"], key="cred_upload"
            )
            token_file = st.file_uploader(
                "Uploader token.json", type=["json"], key="token_upload"
            )
            if cred_file:
                with open("config/credentials.json", "wb") as f:
                    f.write(cred_file.read())
                st.success("credentials.json uploadé !")
            if token_file:
                with open("config/token.json", "wb") as f:
                    f.write(token_file.read())
                st.success("token.json uploadé !")
            submitted = st.form_submit_button("Tester et enregistrer")
            if submitted:
                with st.spinner("Vérification en cours..."):
                    # Test OpenAI
                    try:
                        client = OpenAI(api_key=openai_key)
                        _ = client.models.list()
                        st.session_state["openai_status"] = "✅"
                        st.session_state["openai_msg"] = "Connexion réussie."
                        st.session_state["openai_key"] = openai_key
                    except Exception as e:
                        st.session_state["openai_status"] = "❌"
                        st.session_state["openai_msg"] = f"Erreur : {e}"
                    # Test Notion
                    try:
                        from notion_client import Client

                        notion = Client(auth=notion_key)
                        notion.users.list()
                        st.session_state["notion_status"] = "✅"
                        st.session_state["notion_msg"] = "Connexion réussie."
                        st.session_state["notion_key"] = notion_key
                    except Exception as e:
                        st.session_state["notion_status"] = "❌"
                        st.session_state["notion_msg"] = f"Erreur : {e}"
                    # Test Google
                    import os

                    cred_path = os.path.join("config", "credentials.json")
                    token_path = os.path.join("config", "token.json")
                    if os.path.exists(cred_path) and os.path.exists(token_path):
                        try:
                            from google.oauth2.credentials import Credentials

                            Credentials.from_authorized_user_file(token_path)
                            st.session_state["google_status"] = "✅"
                            st.session_state["google_msg"] = (
                                "Fichiers trouvés et token lisible."
                            )
                            st.session_state["google_info"] = "OK"
                        except Exception as e:
                            st.session_state["google_status"] = "❌"
                            st.session_state["google_msg"] = (
                                f"Erreur de lecture du token : {e}"
                            )
                    else:
                        st.session_state["google_status"] = "❌"
                        st.session_state["google_msg"] = (
                            "credentials.json ou token.json manquant dans config/"
                        )
        # Encart d'aide groupé
        with st.expander("❓ Besoin d'aide ?"):
            st.markdown(
                """
- [Créer une clé OpenAI](https://platform.openai.com/api-keys)
- [Créer une intégration Notion](https://www.notion.com/my-integrations)
- [Générer credentials Google](https://console.cloud.google.com/apis/credentials)
- [Guide utilisateur détaillé](#)
            """
            )
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            if all(st.session_state[f"{s.lower()}_status"] == "✅" for s in services):
                if st.button("Suivant ➡️"):
                    st.session_state["onboarding_step"] += 1
        with col2:
            if st.button("Sauter cette étape", key="skip_connexions"):
                st.session_state["onboarding_step"] += 1
    elif step == 2:
        st.subheader("2️⃣ Préférences de recherche")
        st.write(
            "Dans la barre latérale, renseignez vos mots-clés, localisation et sources d'offres, puis cliquez sur 'Enregistrer les préférences'."
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Précédent"):
                st.session_state["onboarding_step"] -= 1
        with col2:
            if st.button("Suivant ➡️"):
                st.session_state["onboarding_step"] += 1
            if st.button("Sauter cette étape", key="skip_prefs"):
                st.session_state["onboarding_step"] += 1
    elif step == 3:
        st.subheader("3️⃣ Découverte des fonctionnalités")
        st.markdown(
            "- **Tableau de bord** : Suivi de vos candidatures\n- **Générateur de CV/LM** : Documents personnalisés\n- **Préparation entretien** : Questions IA et briefing\n- **Analyse** : Statistiques et graphiques\n- **Planification** : Entretien dans Google Calendar\n- **Logs** : Suivi technique\n- **Guide utilisateur** : Aide pas à pas"
        )
        st.markdown("---")
        if st.button("🎉 Lancer l'application 🚀", type="primary"):
            st.session_state["onboarding_done"] = True
            st.rerun()
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Précédent", key="back_features"):
                st.session_state["onboarding_step"] -= 1
        with col2:
            if st.button("Sauter cette étape", key="skip_features"):
                st.session_state["onboarding_done"] = True
                st.rerun()
    st.stop()


def main():
    """Point d'entrée principal de l'application Streamlit Co-pilote de Carrière."""
    st.set_page_config(page_title="Co-pilote de Carrière", layout="wide")
    menu = [
        "Accueil",
        "Configuration & Connexions",
        "Gestion des Statuts",
        "Planifier un entretien",
        "Logs",
        "🧑‍💼 Guide Utilisateur",
    ]
    choix = st.sidebar.selectbox("Navigation", menu)

    if (
        "onboarding_done" not in st.session_state
        or not st.session_state["onboarding_done"]
    ):
        onboarding()

    # --- Ajout en haut du main() : badge/alerte API manquante ---
    def show_api_alert():
        missing = []
        if not st.session_state.get("openai_key"):
            missing.append("OpenAI")
        if not st.session_state.get("notion_key"):
            missing.append("Notion")
        import os

        cred_path = os.path.join("config", "credentials.json")
        token_path = os.path.join("config", "token.json")
        if not (os.path.exists(cred_path) and os.path.exists(token_path)):
            missing.append("Google")
        # Vérification préférences
        from config import load_preferences

        prefs = load_preferences()
        if not prefs.get("keywords") or not prefs.get("location"):
            missing.append("Préférences de recherche")
        if missing:
            st.warning(
                f"⚠️ API(s)/Préférences non configurée(s) : {', '.join(missing)}. "
                "<a href='#' target='_blank'>Besoin d'aide ?</a>",
                unsafe_allow_html=True,
            )

    # --- Page LOGS ---
    if choix == "Logs":
        st.title("📋 Logs de l'application")
        log_path = "logs/app.log"
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = f.readlines()
            st.text_area("Logs récents", value="".join(logs[-100:]), height=500)
        else:
            st.info("Aucun log disponible pour le moment.")
        return

    if choix == "🧑‍💼 Guide Utilisateur":
        st.title("🧑‍💼 Guide Utilisateur – Co-pilote de Carrière")
        st.markdown(
            """
## 1. Lancement de l’application

1. Ouvre un terminal dans le dossier du projet.
2. Lance la commande suivante :
   ```bash
   ./launch.sh
   ```
3. Une page web s’ouvre automatiquement (sinon, va sur http://localhost:8501).

---

## 2. Configuration initiale

### a) Clés API et accès
- Va dans le menu latéral, onglet **« Configuration & Connexions »**.
- Saisis tes clés API :
  - **OpenAI** : [Créer une clé](https://platform.openai.com/api-keys)
  - **Notion** : [Créer une intégration](https://www.notion.com/my-integrations) et partager ta base
  - **Google** : Place les fichiers `credentials.json` et `token.json` dans le dossier `config/`
- Clique sur **Enregistrer**.
- Vérifie que chaque service affiche « ✅ Connecté ».

---

## 3. Paramétrer tes préférences de recherche

- Dans la barre latérale, section **« Préférences de recherche »** :
  - Renseigne tes mots-clés (un par ligne)
  - Indique ta localisation (ou laisse vide pour du remote)
  - Active/désactive les sources d’offres (LinkedIn, Indeed, Apec, etc.)
  - Configure les options Gmail si besoin
- Clique sur **Enregistrer les préférences**.

---

## 4. Découvrir et ajouter des offres

- Clique sur **« 🚀 Lancer une nouvelle recherche d’offres »**.
- Patiente pendant la recherche.
- Un résumé s’affiche : nombre d’offres trouvées par source, éventuelles erreurs.
- Les offres sont ajoutées automatiquement à ton tableau de bord Notion.

---

## 5. Gérer tes candidatures

- Va dans l’onglet **« Accueil » > « Tableau de Bord »**.
- Visualise toutes tes candidatures, leurs statuts, dates, entreprises.
- Modifie le statut d’une candidature (Découvert, Appliqué, Entretien, Offre, Rejeté) via le menu dédié ou la page « Gestion des Statuts ».

---

## 6. Générer un CV/Lettre de motivation personnalisés

- Va dans l’onglet **« Générer CV/LM »**.
- Téléverse ton CV au format PDF.
- Colle la description du poste visé.
- Clique sur **« Générer les documents »**.
- Récupère ton CV et ta lettre de motivation personnalisés.

---

## 7. Préparer un entretien

- Va dans l’onglet **« Préparer Entretien »**.
- Sélectionne une candidature.
- Clique sur **« Générer le dossier de préparation »**.
- Découvre :
  - Les questions d’entretien personnalisées
  - Un briefing sur l’entreprise

---

## 8. Analyser tes performances

- Va dans l’onglet **« Analyse »**.
- Consulte :
  - Le nombre total de candidatures
  - Le taux de réponse (entretiens obtenus)
  - Les graphiques de répartition des statuts

---

## 9. Planifier un entretien

- Va dans l’onglet **« Planifier un entretien »**.
- Sélectionne une candidature.
- Renseigne la date, l’heure, le lieu, les participants.
- Clique sur **« Créer l’événement dans Google Calendar »**.
- Un message de confirmation s’affiche.

---

## 10. Suivre l’activité et les erreurs

- Va dans l’onglet **« Logs »** pour consulter les derniers événements et erreurs techniques.

---

## 11. FAQ et aide

- Consulte la page **« Configuration & Connexions »** pour des liens d’aide et des instructions détaillées.
- En cas de problème, vérifie les logs ou relance l’application.

---

**Bonne recherche d’emploi avec Co-pilote de Carrière !**
        """
        )
        return

    # --- Page CONFIGURATION ---
    if choix == "Configuration & Connexions":
        st.title("🔑 Configuration & Connexions")
        status = check_connections()
        st.subheader("Statut des connexions :")
        for service, ok in status.items():
            st.write(
                f"{service} : {'✅ Connecté' if ok else '❌ Manquant ou incorrect'}"
            )
        st.markdown("---")
        st.subheader("Saisir ou corriger vos clés/API :")
        with st.form("api_form"):
            notion_key = st.text_input(
                "Clé API Notion", value=os.getenv("NOTION_API_KEY", "")
            )
            openai_key = st.text_input(
                "Clé API OpenAI", value=os.getenv("OPENAI_API_KEY", "")
            )
            submitted = st.form_submit_button("Enregistrer")
            if submitted:
                save_api_keys(notion_key, openai_key)
                st.success(
                    "Clés sauvegardées. Veuillez relancer l'application pour prise en compte."
                )
        st.markdown("---")
        st.subheader("❓ Comment faire ?")
        st.markdown(
            """
        **Notion** :
        - Créez une intégration sur https://www.notion.com/my-integrations
        - Partagez votre base avec l'intégration
        - Copiez la clé secrète dans le champ ci-dessus

        **OpenAI** :
        - Générez une clé API sur https://platform.openai.com/api-keys
        - Collez-la dans le champ ci-dessus

        **Google** :
        - Suivez la documentation pour générer credentials.json et token.json
        - Placez-les dans le dossier `config/`

        Redémarrez l'application après modification.
        """
        )
        return

    # --- Page GESTION DES STATUTS ---
    if choix == "Gestion des Statuts":
        st.title("📝 Gestion des Statuts de Candidature")
        df = database.get_applications_as_dataframe()
        if not df.empty:
            for idx, row in df.iterrows():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.write(f"{row['Titre du Poste']} chez {row['Entreprise']}")
                with col2:
                    st.write(f"Date : {row['Date de Candidature']}")
                with col3:
                    new_status = st.selectbox(
                        "Statut",
                        STATUTS,
                        index=(
                            STATUTS.index(row["Statut"])
                            if row["Statut"] in STATUTS
                            else 0
                        ),
                        key=f"statut_gestion_{row['page_id']}",
                    )
                with col4:
                    if st.button("Mettre à jour", key=f"maj_gestion_{row['page_id']}"):
                        try:
                            database.update_application_status(
                                row["page_id"], new_status
                            )
                            st.success(
                                f"Statut mis à jour pour {row['Titre du Poste']} !"
                            )
                        except Exception as e:
                            show_error(f"Erreur lors de la mise à jour : {e}")
        else:
            st.info(
                "Aucune candidature trouvée dans Notion ou connexion non configurée."
            )
        return

    # --- Page PLANIFIER ENTRETIEN ---
    if choix == "Planifier un entretien":
        st.title("📅 Planifier un entretien")
        df = database.get_applications_as_dataframe()
        if not df.empty:
            selected_idx = st.selectbox(
                "Choisissez une candidature",
                options=df.index,
                format_func=lambda i: f"{df.loc[i, 'Titre du Poste']} chez {df.loc[i, 'Entreprise']}",
            )
            selected_job = df.loc[selected_idx]
            with st.form("calendar_form"):
                summary = st.text_input(
                    "Titre de l'événement",
                    value=f"Entretien - {selected_job['Titre du Poste']} chez {selected_job['Entreprise']}",
                )
                location = st.text_input("Lieu ou lien visio", value="")
                description = st.text_area("Description", value="")
                date = st.date_input("Date de l'entretien")
                start_time = st.time_input("Heure de début")
                end_time = st.time_input("Heure de fin")
                attendees = st.text_area(
                    "Participants (emails, un par ligne)", value=""
                )
                submitted = st.form_submit_button(
                    "Créer l'événement dans Google Calendar"
                )
                if submitted:
                    from datetime import datetime
                    import pytz  # type: ignore[import-untyped]

                    tz = pytz.timezone("Europe/Paris")
                    start_dt = tz.localize(
                        datetime.combine(date, start_time)
                    ).isoformat()
                    end_dt = tz.localize(datetime.combine(date, end_time)).isoformat()
                    emails = [e.strip() for e in attendees.splitlines() if e.strip()]
                    event_details = {
                        "summary": summary,
                        "location": location,
                        "description": description,
                        "start_time": start_dt,
                        "end_time": end_dt,
                        "attendees": emails,
                    }
                    event_id = scheduler.schedule_interview_in_calendar(event_details)
                    if event_id:
                        st.success(f"Événement créé avec succès ! ID : {event_id}")
                    else:
                        show_error("Erreur lors de la création de l'événement.")
        else:
            st.info("Aucune candidature disponible pour planifier un entretien.")
        return

    # --- Page ACCUEIL ---
    if choix == "Accueil":
        st.title("🤖 Co-pilote de Carrière")
        st.caption("Votre agent IA pour une recherche d'emploi optimisée")
        with st.sidebar:
            st.header("⚙️ Préférences de recherche")
            st.markdown(
                "<span style='font-size:12px;color:#888'>Besoin d'aide ? <a href='#' target='_blank'>Voir la documentation sur les préférences</a></span>",
                unsafe_allow_html=True,
            )
            prefs = config.load_preferences()
            st.markdown(
                "#### <span style='color:#4F8BF9'>Résumé</span>", unsafe_allow_html=True
            )
            st.markdown(
                f"**Mots-clés** : <span style='color:#2ECC71'>{', '.join(prefs.get('keywords', []))}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Localisation** : <span style='color:#F39C12'>{prefs.get('location', '')}</span>",
                unsafe_allow_html=True,
            )
            sources = prefs.get("sources", {})
            sources_actives = [k for k, v in sources.items() if v]
            st.markdown(
                f"**Sources activées** : <span style='color:#8E44AD'>{', '.join(sources_actives) if sources_actives else 'Aucune'}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("---")
            with st.form("prefs_form"):
                keywords = st.text_area(
                    "Mots-clés (un par ligne)",
                    value="\n".join(prefs.get("keywords", [])),
                    height=100,
                    help="Exemple : Data Scientist, Product Owner, etc.",
                )
                location = st.text_input(
                    "Localisation",
                    value=prefs.get("location", ""),
                    help="Ville ou région. Laisser vide pour une recherche à distance.",
                )
                st.markdown("**Sources à utiliser :**")
                linkedin = st.checkbox("LinkedIn", value=sources.get("linkedin", True))
                indeed = st.checkbox("Indeed", value=sources.get("indeed", False))
                apec = st.checkbox("Apec", value=sources.get("apec", True))
                pole_emploi = st.checkbox(
                    "Pôle Emploi", value=sources.get("pole_emploi", False)
                )
                gmail_alerts = st.checkbox(
                    "Alertes Gmail", value=sources.get("gmail_alerts", True)
                )
                st.markdown("**Options Gmail :**")
                gmail = prefs.get("gmail", {})
                only_unread = st.checkbox(
                    "Analyser uniquement les emails non lus",
                    value=gmail.get("only_unread", True),
                )
                mark_as_read = st.checkbox(
                    "Marquer les emails comme lus après analyse",
                    value=gmail.get("mark_as_read", True),
                )
                submitted = st.form_submit_button("Enregistrer les préférences")
                if submitted:
                    new_prefs = {
                        "keywords": [
                            k.strip() for k in keywords.splitlines() if k.strip()
                        ],
                        "location": location,
                        "sources": {
                            "linkedin": linkedin,
                            "indeed": indeed,
                            "apec": apec,
                            "pole_emploi": pole_emploi,
                            "gmail_alerts": gmail_alerts,
                        },
                        "gmail": {
                            "only_unread": only_unread,
                            "mark_as_read": mark_as_read,
                        },
                    }
                    config.save_preferences(new_prefs)
                    st.success("Préférences sauvegardées !")
            # Exemple de préférences
            st.markdown(
                "<span style='font-size:12px;color:#888'>Exemple :<br>"
                "Mots-clés : Data Scientist, Product Owner<br>"
                "Localisation : Paris<br>"
                "Sources : LinkedIn, Apec, Gmail</span>",
                unsafe_allow_html=True,
            )
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📊 Tableau de Bord",
                "📄 Générer CV/LM",
                "🎙️ Préparer Entretien",
                "📈 Analyse",
            ]
        )

        # --- TAB 1 : Dashboard ---
        with tab1:
            st.markdown("## 📊 Tableau de Bord")
            st.markdown("---")
            st.header("Suivi des Candidatures (Notion)")
            df = database.get_applications_as_dataframe()
            if not df.empty:
                for idx, row in df.iterrows():
                    st.markdown(
                        f"{row['Titre du Poste']} chez {row['Entreprise']} {colored_status(row['Statut'])}",
                        unsafe_allow_html=True,
                    )
                st.dataframe(df, use_container_width=True)
                st.markdown("---")
                st.subheader("Modifier le statut d'une candidature :")
                for idx, row in df.iterrows():
                    col1, col2, col3 = st.columns([3, 2, 2])
                    with col1:
                        st.write(f"{row['Titre du Poste']} chez {row['Entreprise']}")
                    with col2:
                        new_status = st.selectbox(
                            "Statut",
                            STATUTS,
                            index=(
                                STATUTS.index(row["Statut"])
                                if row["Statut"] in STATUTS
                                else 0
                            ),
                            key=f"statut_{row['page_id']}",
                        )
                    with col3:
                        if st.button("Mettre à jour", key=f"maj_{row['page_id']}"):
                            try:
                                database.update_application_status(
                                    row["page_id"], new_status
                                )
                                st.success(
                                    f"Statut mis à jour pour {row['Titre du Poste']} !"
                                )
                            except Exception as e:
                                st.error(f"Erreur lors de la mise à jour : {e}")
            else:
                st.info(
                    "Aucune candidature trouvée dans Notion ou connexion non configurée."
                )

        # --- TAB 2 : Générateur de CV/LM ---
        with tab2:
            st.header("Générateur de Documents de Candidature")
            job_description = st.text_area(
                "Collez la description du poste ici", height=300
            )
            uploaded_file = st.file_uploader("Téléversez votre CV (PDF)", type=["pdf"])
            if st.button("Générer les documents"):
                if job_description and uploaded_file:
                    with st.spinner("Génération en cours..."):
                        try:
                            temp_path = "data/temp_resume.pdf"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.read())
                            vector_db = generator.create_vector_db_from_resume(
                                temp_path
                            )
                            cv, lm = generator.generate_personalized_documents(
                                vector_db, job_description
                            )
                            st.success("Documents générés !")
                            st.subheader("CV Personnalisé")
                            st.text(cv)
                            st.subheader("Lettre de Motivation")
                            st.text(lm)
                        except ValueError as ve:
                            show_error(f"Erreur lors de la génération : {ve}")
                        except Exception as e:
                            show_error(f"Erreur inattendue : {e}")
                else:
                    st.warning(
                        "Veuillez coller une description de poste et téléverser un CV au format PDF."
                    )

        # --- TAB 3 : Préparation aux Entretiens ---
        with tab3:
            st.header("Préparation aux Entretiens")
            df = database.get_applications_as_dataframe()
            if not df.empty:
                selected_idx = st.selectbox(
                    "Choisissez une candidature",
                    options=df.index,
                    format_func=lambda i: f"{df.loc[i, 'Titre du Poste']} chez {df.loc[i, 'Entreprise']}",
                )
                selected_job = df.loc[selected_idx]
                if st.button("Générer le dossier de préparation"):
                    with st.spinner("Préparation du dossier..."):
                        try:
                            job_details = {
                                "description": selected_job.get(
                                    "Description du Poste",
                                    "Pas de description disponible.",
                                ),
                                "tailored_resume": "Expériences principales du CV à intégrer ici (fonctionnalité à enrichir)",
                                "company": selected_job.get("Entreprise", ""),
                            }
                            questions, company_brief = interview.prepare_for_interview(
                                job_details
                            )
                            st.success("Dossier prêt !")
                            st.subheader("Questions d'entretien suggérées")
                            if isinstance(questions, str):
                                for q in questions.split("\n"):
                                    if q.strip():
                                        st.markdown(f"- {q.strip()}")
                            else:
                                st.write(questions)
                            st.subheader("Briefing sur l'entreprise")
                            st.markdown(company_brief)
                        except Exception as e:
                            show_error(
                                f"Erreur lors de la préparation de l'entretien : {e}"
                            )
            else:
                st.info(
                    "Aucune candidature disponible pour la préparation d'entretien."
                )

        # --- TAB 4 : Analyse des Performances ---
        with tab4:
            st.header("Analyse des Performances")
            metrics = analytics.get_performance_metrics()
            if metrics:
                st.metric("Nombre total de candidatures", metrics["total_applications"])
                st.metric(
                    "Taux de réponse (entretien)", f"{metrics['response_rate']} %"
                )
            else:
                st.info("Aucune donnée de performance disponible.")
            visuals = analytics.get_performance_visuals()
            if visuals and "status_distribution" in visuals:
                st.plotly_chart(visuals["status_distribution"])

        # --- ACTIONS RAPIDES ---
        st.header("Actions")
        if st.button("🚀 Lancer une nouvelle recherche d'offres"):
            with st.spinner("Recherche en cours..."):
                prefs = config.load_preferences()
                try:
                    feedback = discovery.find_and_process_job_offers(prefs)
                    st.success(
                        "Recherche terminée et offres ajoutées au tableau de bord !"
                    )
                    st.markdown("### Résultat par source :")
                    for source, result in feedback.items():
                        if isinstance(result, int):
                            st.markdown(
                                f"- **{source}** : {result} offre(s) trouvée(s)"
                            )
                        else:
                            st.warning(f"{source} : {result}")
                except Exception as e:
                    show_error(f"Erreur lors de la recherche d'offres : {e}")


# Fonctions utilitaires pour la config et les connexions


def check_connections():
    status = {}
    status["Notion"] = bool(config.NOTION_API_KEY)
    status["OpenAI"] = bool(config.OPENAI_API_KEY)
    status["Google"] = os.path.exists(
        config.GOOGLE_CREDENTIALS_PATH
    ) and os.path.exists(config.GOOGLE_TOKEN_PATH)
    return status


def save_api_keys(notion_key, openai_key):
    env_path = config.CONFIG_DIR / ".env"
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    keys = {"NOTION_API_KEY": notion_key, "OPENAI_API_KEY": openai_key}
    new_lines = []
    for line in lines:
        if any(k in line for k in keys):
            continue
        new_lines.append(line)
    for k, v in keys.items():
        if v:
            new_lines.append(f"{k}={v}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    main()
