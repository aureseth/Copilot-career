# Module IV: Suite de Préparation aux Entretiens

from langchain_openai import OpenAI
import config
from pydantic import SecretStr


def generate_interview_questions(job_description: str, resume_content: str):
    """
    Génère des questions d'entretien pertinentes.
    """
    print("Génération des questions d'entretien...")
    llm = OpenAI(
        api_key=(
            SecretStr(config.OPENAI_API_KEY)
            if config.OPENAI_API_KEY is not None
            else None
        ),
        temperature=0.7,
    )
    prompt = f"""
    En te basant sur la description de poste ci-dessous et des extraits du CV du candidat,
    génère une liste de 10 questions d'entretien pertinentes (comportementales, techniques, situationnelles).

    Description de poste:
    {job_description}

    CV du candidat:
    {resume_content}

    Liste de questions:
    """
    questions = llm(prompt)
    return questions


def create_company_brief(company_name: str):
    """
    Crée un briefing sur l'entreprise en se basant sur des recherches (simulées ici).
    """
    print(f"Création du briefing pour l'entreprise {company_name}...")
    # Dans une vraie implémentation, scraper le site de l'entreprise, les actualités, etc.
    # Ici, on utilise un LLM pour générer un exemple de synthèse.
    llm = OpenAI(
        api_key=(
            SecretStr(config.OPENAI_API_KEY)
            if config.OPENAI_API_KEY is not None
            else None
        ),
        temperature=0.5,
    )
    prompt = f"""
    Rédige un bref rapport de synthèse sur l'entreprise "{company_name}".
    Inclus sa mission, ses produits principaux, ses concurrents et des actualités récentes.
    Le ton doit être informatif et concis.
    """
    brief = llm(prompt)
    return brief


def prepare_for_interview(job_details: dict):
    """
    Orchestre la préparation complète pour un entretien.
    """
    job_description = job_details.get("description", "")
    resume_content = job_details.get("tailored_resume", "")  # Le CV adapté
    company_name = job_details.get("company", "")

    questions = generate_interview_questions(job_description, resume_content)
    company_brief = create_company_brief(company_name)

    return questions, company_brief


if __name__ == "__main__":
    # Test du module
    example_job = {
        "description": "Développeur Senior IA chez Google. Nécessite une expertise en TensorFlow et en traitement du langage naturel.",
        "tailored_resume": "Expérience de 5 ans en développement de modèles NLP avec TensorFlow.",
        "company": "Google",
    }
    questions, brief = prepare_for_interview(example_job)
    print("--- Questions d'entretien ---")
    print(questions)
    print("\n--- Briefing Entreprise ---")
    print(brief)
