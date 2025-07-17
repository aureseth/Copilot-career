# Outils pour l'API Google Calendar, à utiliser avec LangChain

from langchain.tools import tool
from .google_auth import get_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from typing import Optional, List


@tool
def schedule_interview(
    summary: str,
    start_time: str,
    end_time: str,
    location: Optional[str] = None,
    description: Optional[str] = None,
    attendees: Optional[List[str]] = None,
) -> str:
    """
    Planifie un événement dans Google Calendar.
    Prend en entrée le titre (summary), l'heure de début et de fin (format ISO 8601: '2024-09-30T10:00:00'),
    et optionnellement le lieu, la description et les participants (liste d'emails).
    Retourne l'ID de l'événement créé ou un message d'erreur.
    """
    creds = get_credentials()
    if not creds:
        return "Authentification Google échouée."

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "Europe/Paris"},
            "end": {"dateTime": end_time, "timeZone": "Europe/Paris"},
            "attendees": [{"email": email} for email in attendees] if attendees else [],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 30},
                ],
            },
        }

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
        return f"Événement créé avec succès. ID: {created_event.get('id')}"

    except HttpError as error:
        return f"Une erreur API Google est survenue: {error}"
    except Exception as e:
        return f"Une erreur inattendue est survenue: {e}"
