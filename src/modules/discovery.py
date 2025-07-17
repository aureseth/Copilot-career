# Module I: Moteur de Découverte d'Emplois Omni-Source

from tools import gmail_tools
from modules import database
from tools.scraping_tools import (
    scrape_linkedin_pure,
    scrape_indeed_pure,
    scrape_apec_pure,
    scrape_pole_emploi_pure,
)
from tools.gmail_tools import scan_emails_for_updates_pure

# Charger le modèle spaCy
# nlp = spacy.load("fr_core_news_sm")


def find_and_process_job_offers(search_preferences: dict):
    """
    Orchestre la recherche d'offres depuis plusieurs sources
    et les ajoute à la base de données.
    """
    sources = search_preferences.get("sources", {})
    keywords = search_preferences.get("keywords") or ""
    location = search_preferences.get("location") or ""
    feedback = {}
    # LinkedIn
    if sources.get("linkedin", False):
        try:
            scraped_offers = scrape_linkedin_pure(keywords=keywords, location=location)
            for offer in scraped_offers:
                database.add_new_offer(offer)
            feedback["LinkedIn"] = str(len(scraped_offers))
        except Exception as e:
            feedback["LinkedIn"] = f"Erreur : {e}"
    # Indeed
    if sources.get("indeed", False):
        try:
            scraped_offers = scrape_indeed_pure(keywords=keywords, location=location)
            for offer in scraped_offers:
                database.add_new_offer(offer)
            feedback["Indeed"] = str(len(scraped_offers))
        except Exception as e:
            feedback["Indeed"] = f"Erreur : {e}"
    # Apec
    if sources.get("apec", False):
        try:
            scraped_offers = scrape_apec_pure(keywords=keywords, location=location)
            for offer in scraped_offers:
                database.add_new_offer(offer)
            feedback["Apec"] = str(len(scraped_offers))
        except Exception as e:
            feedback["Apec"] = f"Erreur : {e}"
    # Pôle Emploi
    if sources.get("pole_emploi", False):
        try:
            scraped_offers = scrape_pole_emploi_pure(
                keywords=keywords, location=location
            )
            for offer in scraped_offers:
                database.add_new_offer(offer)
            feedback["Pôle Emploi"] = str(len(scraped_offers))
        except Exception as e:
            feedback["Pôle Emploi"] = f"Erreur : {e}"
    # Gmail Alerts
    if sources.get("gmail_alerts", False):
        try:
            email_offers = scan_emails_for_updates_pure(
                query="offre emploi OR nouvelle opportunité"
            )
            for offer in email_offers:
                database.add_new_offer(
                    {
                        "title": offer.get("subject", "Offre via Gmail"),
                        "company": offer.get("from", "?"),
                        "url": "",
                        "description": offer.get("snippet", ""),
                    }
                )
            feedback["Alertes Gmail"] = str(len(email_offers))
        except Exception as e:
            feedback["Alertes Gmail"] = f"Erreur : {e}"
    return feedback


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
