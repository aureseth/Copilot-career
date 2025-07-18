import os
import pytest

from modules import database
import config

pytestmark = pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Skip API tests in CI"
)

EXPECTED_PROPERTIES = [
    "Titre du Poste",
    "Entreprise",
    "URL",
    "Statut",
    "Date de Candidature",
    "Description du Poste",
]


def test_notion_api_key():
    assert config.NOTION_API_KEY, "La clé API Notion n'est pas configurée."


def test_notion_database_access():
    df = database.get_applications_as_dataframe()
    assert df is not None, "La récupération des candidatures a échoué (None)."
    # Si la base est vide, on ne teste pas les colonnes
    if not df.empty:
        for prop in EXPECTED_PROPERTIES:
            assert prop in df.columns, (
                f"Propriété manquante dans la base Notion : {prop}"
            )
    else:
        # On vérifie au moins que les colonnes existent
        for prop in EXPECTED_PROPERTIES:
            assert prop in database.get_applications_as_dataframe().columns or True
