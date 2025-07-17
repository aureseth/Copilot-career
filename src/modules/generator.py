# Module III: Générateur de CV/LM avec RAG

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import config


def create_vector_db_from_resume(resume_path: str):
    """
    Charge un CV au format PDF, le découpe, crée des embeddings,
    et le stocke dans une base de données vectorielle FAISS.
    """
    print("Création de la base de données vectorielle à partir du CV...")
    loader = PyPDFLoader(resume_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(texts, embeddings)

    print("Base de données vectorielle créée.")
    return vectorstore


def generate_personalized_documents(vectorstore, job_description: str):
    """
    Utilise la pipeline RAG pour générer un CV et une lettre de motivation.
    """
    print("Génération des documents personnalisés...")

    # 1. Récupération des informations pertinentes du CV
    # retriever = vectorstore.as_retriever()

    # 2. Construction du prompt pour le LLM
    # prompt_template_cv = """
    # Basé sur la description de poste suivante et les extraits de mon CV,
    # rédige une version de mon CV qui met en avant les expériences les plus pertinentes.
    # Ne jamais inventer d'expériences. Sois concis et professionnel.

    # Description de poste:
    # {job_description}

    # Extraits de mon CV:
    # {context}

    # CV personnalisé:
    # """

    # 3. Création de la chaîne LangChain
    # qa_chain = RetrievalQA.from_chain_type(
    #     llm=OpenAI(api_key=config.OPENAI_API_KEY, temperature=0.2),
    #     chain_type="stuff",
    #     retriever=retriever,
    #     chain_type_kwargs={"prompt": ...},  # A compléter avec le prompt
    # )

    # 4. Génération
    # cv = qa_chain.run(job_description)
    # lm = ... # Une autre chaîne pour la lettre de motivation

    cv_placeholder = "CV personnalisé basé sur la description."
    lm_placeholder = "Lettre de motivation personnalisée."

    return cv_placeholder, lm_placeholder


if __name__ == "__main__":
    # Test du module
    # Assurez-vous d'avoir un fichier master_resume.pdf dans /data
    resume_file = "data/master_resume.pdf"
    # vector_db = create_vector_db_from_resume(resume_file)

    job_desc_example = (
        "Nous recherchons un développeur Python avec une expérience en IA..."
    )
    # cv, lm = generate_personalized_documents(vector_db, job_desc_example)
    # print("--- CV ---")
    # print(cv)
    # print("\n--- Lettre de Motivation ---")
    # print(lm)
