# Outils pour l'API Gmail, à utiliser avec LangChain

from typing import List, Dict, Any
from langchain.tools import tool
from .google_auth import get_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email
from email.message import Message


@tool
def scan_emails_for_updates(
    query: str = "invitation entretien OR réponse candidature",
) -> List[Dict[str, Any]]:
    """
    Scanne la boîte de réception Gmail à la recherche d'emails correspondant à une requête.
    Utilise l'API Gmail pour trouver des mises à jour sur les candidatures.
    Retourne une liste de dictionnaires contenant les détails des emails pertinents.
    """
    creds = get_credentials()
    if not creds:
        print("Authentification Google échouée.")
        return []

    try:
        service = build("gmail", "v1", credentials=creds)

        # Rechercher les messages
        result = service.users().messages().list(userId="me", q=query).execute()
        messages = result.get("messages", [])

        if not messages:
            print("Aucun email trouvé pour cette requête.")
            return []

        email_updates = []
        for msg in messages[:5]:  # Limiter à 5 pour l'exemple
            txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
            payload = txt["payload"]
            headers = payload["headers"]

            subject = next(h["value"] for h in headers if h["name"] == "Subject")
            sender = next(h["value"] for h in headers if h["name"] == "From")

            # Extraire le corps de l'email
            data: str
            if "parts" in payload:
                part = payload["parts"][0]
                data = part["body"]["data"]
            else:
                data = payload["body"]["data"]

            data = data.replace("-", "+").replace("_", "/")
            decoded_data: bytes = base64.b64decode(data)

            mime_msg: Message = email.message_from_bytes(decoded_data)
            body: str = ""
            if mime_msg.is_multipart():
                for part in mime_msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload_decoded = part.get_payload(decode=True)
                        if payload_decoded:
                            body = payload_decoded.decode()
                            break
            else:
                payload_decoded = mime_msg.get_payload(decode=True)
                if payload_decoded:
                    body = payload_decoded.decode()

            email_updates.append(
                {
                    "from": sender,
                    "subject": subject,
                    "snippet": txt["snippet"],
                    "body": body[:500],  # Tronquer pour la lisibilité
                }
            )
        return email_updates

    except HttpError as error:
        print(f"Une erreur API Google est survenue: {error}")
        return []
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
        return []
