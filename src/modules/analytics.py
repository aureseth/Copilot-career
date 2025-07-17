# Module VI: Analyse des Performances

import plotly.express as px
from modules import database


def get_performance_metrics():
    """
    Calcule les métriques de performance à partir des données de Notion.
    """
    df = database.get_applications_as_dataframe()

    if df.empty:
        return None

    # Taux de réponse (Entretien / Appliqué)
    # Ceci est une simplification, il faudrait plus de statuts
    applied_count = df[df["Statut"] == "Appliqué"].shape[0]
    interview_count = df[df["Statut"] == "Entretien"].shape[0]

    response_rate = (
        (interview_count / (applied_count + interview_count)) * 100
        if (applied_count + interview_count) > 0
        else 0
    )

    metrics = {
        "total_applications": df.shape[0],
        "response_rate": round(response_rate, 2),
    }
    return metrics


def get_performance_visuals():
    """
    Génère des graphiques pour la visualisation des performances.
    """
    df = database.get_applications_as_dataframe()

    if df.empty:
        return {}

    # Graphique: Répartition des statuts
    status_counts = df["Statut"].value_counts().reset_index()
    status_counts.columns = ["Statut", "Nombre"]
    fig_status = px.pie(
        status_counts,
        names="Statut",
        values="Nombre",
        title="Répartition des Statuts de Candidature",
    )

    # D'autres graphiques pourraient être ajoutés ici
    # ex: Taux de réponse par source, etc.

    return {"status_distribution": fig_status}


if __name__ == "__main__":
    # Test du module
    metrics = get_performance_metrics()
    print("--- Métriques ---")
    print(metrics)

    visuals = get_performance_visuals()
    print("\n--- Visuels ---")
    if visuals:
        visuals["status_distribution"].show()
