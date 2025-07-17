# Définition de l'agent LangChain principal

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import config

# Importer les outils personnalisés
from tools import notion_tools, gmail_tools, calendar_tools, scraping_tools


class CareerAgent:
    def __init__(self):
        # Initialiser le LLM
        self.llm = OpenAI(api_key=config.OPENAI_API_KEY, temperature=0)

        # Définir les outils disponibles pour l'agent
        self.tools = [
            notion_tools.add_application,
            notion_tools.update_application_status,
            gmail_tools.scan_emails_for_updates,
            calendar_tools.schedule_interview,
            scraping_tools.scrape_job_posting,
        ]

        # Définir le prompt de l'agent
        # Le prompt doit inclure des instructions sur l'utilisation des outils
        # et les placeholders requis : {tools}, {tool_names}, {input}, {agent_scratchpad}
        prompt_template = """
        Tu es "Co-pilote de Carrière", un agent IA expert en recherche d'emploi.
        Réponds à la question suivante du mieux que tu peux. Tu as accès aux outils suivants :

        {tools}

        Utilise le format suivant :

        Question : la question à laquelle tu dois répondre
        Pensée : tu dois toujours réfléchir à ce que tu dois faire
        Action : l'action à entreprendre, doit être l'un des [{tool_names}]
        Action Input : l'entrée pour l'action
        Observation : le résultat de l'action
        ... (cette séquence Pensée/Action/Action Input/Observation peut se répéter N fois)
        Pensée : Je connais maintenant la réponse finale
        Réponse finale : la réponse finale à la question d'origine

        Commence !

        Question : {input}
        Pensée : {agent_scratchpad}
        """

        self.prompt = PromptTemplate.from_template(prompt_template)

        # Créer l'agent avec la logique ReAct
        agent = create_react_agent(self.llm, self.tools, self.prompt)

        # Créer l'exécuteur de l'agent
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run(self, user_input: str):
        """
        Exécute une tâche donnée avec l'agent.
        """
        return self.agent_executor.invoke({"input": user_input})


if __name__ == "__main__":
    # Exemple d'utilisation
    career_agent = CareerAgent()
    result = career_agent.run(
        "Recherche les nouvelles offres pour 'Développeur Python' et ajoute-les à Notion."
    )
    print(result)
