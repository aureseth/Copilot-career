# Outils pour l'API Gmail, à utiliser avec LangChain

from langchain.tools import tool
from .google_auth import get_credentials
from googleapiclient.discovery import build  # type: ignore[import-untyped]
from googleapiclient.errors import HttpError  # type: ignore[import-untyped]
import base64
import email
from email.message import Message


def scan_emails_for_updates_pure(
    query: str = "invitation entretien OR réponse candidature",
) -> list:
    creds = get_credentials()
    if not creds:
        print("Authentification Google échouée.")
        return []
    try:
        service = build("gmail", "v1", credentials=creds)
        result = service.users().messages().list(userId="me", q=query).execute()
        messages = result.get("messages", [])
        if not messages:
            print("Aucun email trouvé pour cette requête.")
            return []
        email_updates = []
        for msg in messages[:5]:
            txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
            payload = txt["payload"]
            headers = payload["headers"]
            subject = next(h["value"] for h in headers if h["name"] == "Subject")
            sender = next(h["value"] for h in headers if h["name"] == "From")
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
                            if isinstance(payload_decoded, bytes):
                                body = payload_decoded.decode()
                            else:
                                body = str(payload_decoded)
                            break
            else:
                payload_decoded = mime_msg.get_payload(decode=True)
                if payload_decoded:
                    if isinstance(payload_decoded, bytes):
                        body = payload_decoded.decode()
                    else:
                        body = str(payload_decoded)
            email_updates.append(
                {
                    "from": sender,
                    "subject": subject,
                    "snippet": txt["snippet"],
                    "body": body[:500],
                }
            )
        return email_updates
    except HttpError as error:
        print(f"Une erreur API Google est survenue: {error}")
        return []
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
        return []


@tool
def scan_emails_for_updates(
    query: str = "invitation entretien OR réponse candidature",
) -> list:
    """
    Scanne les emails pour détecter les mises à jour de candidatures (statuts, invitations, etc.).
    """
    return scan_emails_for_updates_pure(query)
