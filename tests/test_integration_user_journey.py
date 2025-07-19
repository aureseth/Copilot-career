from unittest.mock import patch, MagicMock
import config
import modules.discovery as discovery
import modules.generator as generator
import modules.interview as interview
import modules.scheduler as scheduler


def test_onboarding_and_user_journey(tmp_path):
    # 1. Onboarding complet : configuration API et préférences
    # Mock les clés API
    config.OPENAI_API_KEY = "sk-test"
    config.NOTION_API_KEY = "secret-test"
    # Mock préférences utilisateur
    prefs = {
        "keywords": ["Data Scientist", "Product Owner"],
        "location": "Paris",
        "sources": {
            "linkedin": True,
            "indeed": True,
            "apec": True,
            "pole_emploi": False,
            "gmail_alerts": False,
        },
        "gmail": {"only_unread": True, "mark_as_read": True},
    }
    config.save_preferences(prefs)
    loaded = config.load_preferences()
    assert loaded["keywords"] == ["Data Scientist", "Product Owner"]
    assert loaded["location"] == "Paris"

    # 2. Découverte multi-sources (mock scraping)
    with patch(
        "modules.discovery.scrape_linkedin_pure",
        return_value=[
            {"title": "Test", "company": "X", "url": "", "description": "..."}
        ],
    ):
        with patch("modules.discovery.scrape_indeed_pure", return_value=[]):
            with patch("modules.discovery.scrape_apec_pure", return_value=[]):
                feedback = discovery.find_and_process_job_offers(prefs)
                assert "LinkedIn" in feedback
                assert int(feedback["LinkedIn"]) >= 1

    # 3. Génération de documents (mock PDF)
    with patch("modules.generator.PyPDFLoader") as mock_loader:
        mock_doc = MagicMock()
        mock_doc.page_content = "Ceci est un texte de test pour le PDF."
        mock_doc.metadata = {}
        mock_loader.return_value.load.return_value = [mock_doc]
        with patch("modules.generator.OpenAIEmbeddings") as mock_embed:
            mock_embed.return_value.embed_documents.return_value = [[0.1] * 1536]
            vector_db = generator.create_vector_db_from_resume("fake.pdf")
            cv, lm = generator.generate_personalized_documents(
                vector_db, "Description de poste"
            )
            assert cv
            assert lm

    # 4. Préparation à l'entretien (mock LLM)
    with patch("modules.interview.OpenAI") as mock_llm:
        llm_outputs = iter(["Q1\nQ2\nQ3", "Briefing..."])
        mock_llm.return_value.side_effect = lambda *a, **k: next(llm_outputs)
        job_details = {
            "description": "desc",
            "tailored_resume": "cv",
            "company": "TestCorp",
        }
        questions, briefing = interview.prepare_for_interview(job_details)
        assert "Q1" in questions
        assert "Briefing" in briefing

    # 5. Planification d'entretien (mock Google Calendar)
    with patch("modules.scheduler.schedule_interview_tool", return_value="event123"):
        event_details = {
            "summary": "Entretien Test",
            "location": "En ligne",
            "description": "Test...",
            "start_time": "2025-08-15T14:00:00",
            "end_time": "2025-08-15T15:00:00",
            "attendees": ["test@example.com"],
        }
        event_id = scheduler.schedule_interview_in_calendar(event_details)
        assert event_id == "event123"
