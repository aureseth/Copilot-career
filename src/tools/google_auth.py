# google_auth.py
# Gère l'authentification OAuth2 pour les APIs Google

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import config


def get_credentials():
    """
    Gère le flux d'authentification Google OAuth2.
    - Cherche un token.json valide.
    - Si non trouvé ou invalide, lance le flux d'autorisation.
    - Requiert un fichier credentials.json dans le répertoire /config.
    Retourne les credentials valides ou None en cas d'échec.
    """
    creds = None
    # Le fichier token.json stocke les jetons d'accès et de rafraîchissement de l'utilisateur.
    if os.path.exists(config.GOOGLE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            config.GOOGLE_TOKEN_PATH, config.GOOGLE_SCOPES
        )

    # S'il n'y a pas de credentials valides, laisser l'utilisateur se connecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Erreur lors du rafraîchissement du token: {e}")
                # En cas d'échec du refresh, on relance le flux complet
                creds = _run_oauth_flow()
        else:
            creds = _run_oauth_flow()

        # Sauvegarder les credentials pour la prochaine exécution
        if creds:
            with open(config.GOOGLE_TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
    return creds


def _run_oauth_flow():
    """Exécute le flux d'autorisation interactif."""
    if not os.path.exists(config.GOOGLE_CREDENTIALS_PATH):
        print(
            f"ERREUR: Le fichier 'credentials.json' est introuvable dans {config.CONFIG_DIR}"
        )
        print(
            "Veuillez le télécharger depuis votre Google Cloud Console et le placer dans le bon répertoire."
        )
        return None

    flow = InstalledAppFlow.from_client_secrets_file(
        config.GOOGLE_CREDENTIALS_PATH, config.GOOGLE_SCOPES
    )
    # L'argument port=0 trouve un port local disponible aléatoirement.
    creds = flow.run_local_server(port=0)
    return creds


if __name__ == "__main__":
    # Test du module d'authentification
    print("Tentative d'obtention des credentials Google...")
    credentials = get_credentials()
    if credentials:
        print("Authentification réussie !")
        print(f"Token valide jusqu'à: {credentials.expiry}")
    else:
        print("Échec de l'authentification.")
