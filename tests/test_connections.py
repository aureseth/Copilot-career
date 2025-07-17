import config
from modules import database

# Test Notion


def test_notion_connection():
    assert config.NOTION_API_KEY, "Clé API Notion manquante."
    df = database.get_applications_as_dataframe()
    assert df is not None, "Impossible de récupérer les candidatures Notion."


# Test OpenAI


def test_openai_key():
    assert config.OPENAI_API_KEY, "Clé API OpenAI manquante."


# Test Google


def test_google_credentials():
    from tools import google_auth

    creds = google_auth.get_credentials()
    assert (
        creds is not None
    ), "Impossible d'obtenir les credentials Google. Vérifiez le fichier credentials.json et le token."
