# Outils pour l'API Notion, à utiliser avec LangChain

from langchain.tools import tool
from modules import database


@tool
def add_application(title: str, company: str, url: str, description: str) -> str:
    """
    Ajoute une nouvelle candidature à la base de données Notion.
    Prend en entrée le titre, l'entreprise, l'URL et la description.
    """
    offer_details = {
        "title": title,
        "company": company,
        "url": url,
        "description": description,
    }
    database.add_new_offer(offer_details)
    return f"L'offre '{title}' chez '{company}' a été ajoutée à Notion."


@tool
def update_application_status(page_id: str, status: str) -> str:
    """
    Met à jour le statut d'une candidature dans Notion en utilisant son ID de page.
    Les statuts valides sont: Découvert, Appliqué, Entretien, Offre, Rejeté.
    """
    database.update_application_status(page_id, status)
    return f"Le statut de la page {page_id} a été mis à jour à '{status}'."
