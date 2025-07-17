# Module II: Connecteur pour la base de données Notion

from notion_client import Client, APIResponseError
import pandas as pd
import config  # Utiliser le module de configuration centralisé

# Initialisation du client Notion
notion = None
if config.NOTION_API_KEY:
    notion = Client(auth=config.NOTION_API_KEY)
else:
    print("Warning: NOTION_API_KEY not found. Notion integration will be disabled.")


def _get_property_value(props, prop_name, prop_type):
    """Helper pour extraire la valeur d'une propriété Notion."""
    prop = props.get(prop_name, {})
    if not prop or prop_type not in prop:
        return None

    item = prop[prop_type]
    if not item:
        return None

    if prop_type == "title":
        return item[0].get("plain_text")
    if prop_type == "rich_text":
        return item[0].get("plain_text")
    if prop_type == "select":
        return item.get("name")
    if prop_type == "url":
        return item
    if prop_type == "date":
        return item.get("start")
    if prop_type == "files":
        return item[0].get("name")
    return None


def add_new_offer(offer_details: dict):
    """
    Ajoute une nouvelle offre d'emploi comme une nouvelle page dans la base de données Notion.
    """
    if not notion:
        print("Cannot add offer, Notion client not initialized.")
        return

    print(f"Ajout de l'offre '{offer_details['title']}' à Notion.")
    try:
        properties = {
            "Titre du Poste": {
                "title": [{"text": {"content": offer_details["title"]}}]
            },
            "Entreprise": {
                "rich_text": [{"text": {"content": offer_details["company"]}}]
            },
            "URL": {"url": offer_details["url"]},
            "Statut": {"select": {"name": "Découvert"}},
            "Date de Candidature": {
                "date": {"start": pd.Timestamp.now().strftime("%Y-%m-%d")}
            },
            # L'API Notion a une limite de 2000 caractères pour les blocs de texte.
            "Description du Poste": {
                "rich_text": [
                    {"text": {"content": offer_details.get("description", "")[:2000]}}
                ]
            },
        }
        notion.pages.create(
            parent={"database_id": config.NOTION_DATABASE_ID}, properties=properties
        )
    except APIResponseError as e:
        print(f"Erreur API Notion: {e}")


def update_application_status(page_id: str, status: str):
    """
    Met à jour le statut d'une candidature existante.
    Status peut être: Découvert, Appliqué, Entretien, Offre, Rejeté
    """
    if not notion:
        print("Cannot update status, Notion client not initialized.")
        return

    print(f"Mise à jour de la page {page_id} avec le statut '{status}'.")
    try:
        notion.pages.update(
            page_id=page_id, properties={"Statut": {"select": {"name": status}}}
        )
    except APIResponseError as e:
        print(f"Erreur API Notion: {e}")


def get_applications_as_dataframe():
    """
    Récupère toutes les candidatures de Notion et les retourne sous forme de DataFrame pandas.
    """
    if not notion:
        print("Cannot get applications, Notion client not initialized.")
        return pd.DataFrame()

    print("Récupération des candidatures depuis Notion.")
    try:
        response = notion.databases.query(database_id=config.NOTION_DATABASE_ID)
        results = response.get("results", [])

        parsed_data = []
        for page in results:
            props = page.get("properties", {})
            parsed_page = {
                "page_id": page.get("id"),
                "Titre du Poste": _get_property_value(props, "Titre du Poste", "title"),
                "Entreprise": _get_property_value(props, "Entreprise", "rich_text"),
                "Statut": _get_property_value(props, "Statut", "select"),
                "Date de Candidature": _get_property_value(
                    props, "Date de Candidature", "date"
                ),
                "URL": _get_property_value(props, "URL", "url"),
            }
            parsed_data.append(parsed_page)

        return pd.DataFrame(parsed_data)

    except APIResponseError as e:
        print(f"Erreur API Notion: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    # Test du module
    print("--- Test du module de base de données Notion ---")

    # Pour tester, assurez-vous que votre .env est configuré
    if not all([config.NOTION_API_KEY, config.NOTION_DATABASE_ID]):
        print(
            "Veuillez configurer NOTION_API_KEY et NOTION_DATABASE_ID dans votre .env pour tester."
        )
    else:
        print(
            """
1. Récupération des candidatures existantes..."""
        )
        df = get_applications_as_dataframe()
        print(df.head())

        print(
            """
2. Ajout d'une nouvelle offre de test..."""
        )
        test_offer = {
            "title": "Ingénieur Test (via script)",
            "company": "CorpTest",
            "url": "https://www.example.com",
            "description": "Ceci est une description de test générée par le script.",
        }
        add_new_offer(test_offer)
        print("Offre de test ajoutée (vérifiez votre Notion).")

        print(
            """
3. Mise à jour du statut (exemple sur la première ligne)..."""
        )
        if not df.empty:
            page_to_update = df.iloc[0]["page_id"]
            update_application_status(page_to_update, "Entretien")
            print(f"Statut de la page {page_to_update} mis à jour.")
        else:
            print("Aucune candidature à mettre à jour.")
