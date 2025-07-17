# Fichier principal de l'application Streamlit

import streamlit as st

# from agent_core import CareerAgent


def main():
    st.set_page_config(page_title="Co-pilote de Carrière", layout="wide")

    st.title("🤖 Co-pilote de Carrière")
    st.caption("Votre agent IA pour une recherche d'emploi optimisée")

    # Initialisation de l'agent
    # L'agent pourrait être stocké dans st.session_state pour persistance
    if "agent" not in st.session_state:
        # st.session_state.agent = CareerAgent()
        pass

    # Barre latérale pour la configuration et les actions
    with st.sidebar:
        st.header("Configuration")
        # Charger les préférences (à implémenter)
        st.text_area(
            "Préférences de recherche (YAML)",
            value="poste: 'Data Scientist'\nlocalisation: 'Paris'\n...",
            height=150,
        )

        st.header("Actions")
        if st.button("🚀 Lancer une nouvelle recherche d'offres"):
            with st.spinner("Recherche en cours..."):
                # Logique de recherche
                st.success("Recherche terminée !")

    # Définition des onglets de l'interface
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Tableau de Bord", "📄 Générer CV/LM", "🎙️ Préparer Entretien", "📈 Analyse"]
    )

    with tab1:
        st.header("Suivi des Candidatures (Notion)")
        # Afficher le tableau de bord des candidatures
        # df = database.get_applications_as_dataframe()
        # st.dataframe(df, use_container_width=True)
        st.info("Le tableau de bord des candidatures sera affiché ici.")

    with tab2:
        st.header("Générateur de Documents de Candidature")
        job_description = st.text_area("Collez la description du poste ici", height=300)
        if st.button("Générer les documents"):
            if job_description:
                with st.spinner("Génération en cours..."):
                    # cv, lm = generator.create_documents(job_description)
                    st.success("Documents générés !")
                    st.subheader("CV Personnalisé")
                    # st.text(cv)
                    st.subheader("Lettre de Motivation")
                    # st.text(lm)
            else:
                st.warning("Veuillez coller une description de poste.")

    with tab3:
        st.header("Préparation aux Entretiens")
        # Sélectionner une candidature pour préparer l'entretien
        # selected_job = st.selectbox("Choisissez une candidature", options=df['Titre du Poste'])
        if st.button("Générer le dossier de préparation"):
            with st.spinner("Préparation du dossier..."):
                # questions, company_brief = interview.prepare_for_interview(selected_job)
                st.success("Dossier prêt !")
                st.subheader("Questions d'entretien suggérées")
                # st.write(questions)
                st.subheader("Briefing sur l'entreprise")
                # st.markdown(company_brief)

    with tab4:
        st.header("Analyse des Performances")
        # figures = analytics.get_performance_visuals()
        # st.plotly_chart(figures['response_rate_by_source'])
        st.info("Les graphiques d'analyse des performances seront affichés ici.")


if __name__ == "__main__":
    main()
