# Module V: Intégration avec Google Calendar

from tools.calendar_tools import schedule_interview as schedule_interview_tool


def schedule_interview_in_calendar(event_details: dict):
    """
    Crée un événement dans Google Calendar pour un entretien.

    event_details = {
        "summary": "Entretien - Développeur IA chez Google",
        "location": "Lien Google Meet ou adresse",
        "description": "Lien vers le dossier de préparation...",
        "start_time": "2024-09-01T10:00:00",
        "end_time": "2024-09-01T11:00:00",
        "attendees": ["email_candidat@example.com", "email_recruteur@example.com"]
    }
    """
    print(f"Planification de l'événement: {event_details['summary']}")

    # Appel direct à la fonction décorée (le décorateur @tool ne gêne pas l'appel direct)
    event_id = schedule_interview_tool(
        summary=event_details["summary"],
        start_time=event_details["start_time"],
        end_time=event_details["end_time"],
        description=event_details.get("description"),
        location=event_details.get("location"),
        attendees=event_details.get("attendees"),
    )

    if event_id:
        print(f"Événement créé avec succès. ID: {event_id}")
        return event_id
    else:
        print("Échec de la création de l'événement.")
        return None


if __name__ == "__main__":
    # Test du module
    test_event = {
        "summary": "Test Entretien - Co-pilote de Carrière",
        "location": "En ligne",
        "description": "Ceci est un test de planification.",
        "start_time": "2025-08-15T14:00:00",
        "end_time": "2025-08-15T15:00:00",
    }
    schedule_interview_in_calendar(test_event)
