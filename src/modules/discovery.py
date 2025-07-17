# Module I: Moteur de Découverte d'Emplois Omni-Source

from tools import scraping_tools, gmail_tools
from modules import database

# Charger le modèle spaCy
# nlp = spacy.load("fr_core_news_sm")


def find_and_process_job_offers(search_preferences: dict):
    """
    Orchestre la recherche d'offres depuis plusieurs sources
    et les ajoute à la base de données.
    """
    # 1. Scraping des sites web
    # TODO: Gérer plusieurs sites à partir des préférences
    scraped_offers = scraping_tools.scrape_linkedin(
        keywords=search_preferences.get("keywords"),
        location=search_preferences.get("location"),
    )
    for offer in scraped_offers:
        database.add_new_offer(offer)

    # 2. Intégration des API (exemple)
    # api_offers = apec_api.search_offers(...)
    # for offer in api_offers:
    #     database.add_new_offer(offer)

    print(f"{len(scraped_offers)} offres scrapées et ajoutées.")


def scan_and_update_from_emails():
    """
    Scanne les emails, extrait les statuts de candidature et met à jour Notion.
    """
    updates = gmail_tools.scan_emails_for_updates()

    for update in updates:
        # Utiliser spaCy ou des regex pour extraire les infos
        # Exemple simplifié
        company_name = update.get("company")
        status = "Entretien"  # Supposons que l'email est une invitation

        if company_name:
            database.update_application_status_by_company(company_name, status)

            # Si une date est détectée, planifier l'entretien
            if update.get("interview_date"):
                # ... appeler scheduler.py
                pass


if __name__ == "__main__":
    # Test du module
    prefs = {"keywords": "Ingénieur logiciel", "location": "Lyon"}
    find_and_process_job_offers(prefs)
    scan_and_update_from_emails()
