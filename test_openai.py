import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger les variables d'environnement depuis config/.env
dotenv_path = os.path.join(os.path.dirname(__file__), "config", ".env")
load_dotenv(dotenv_path=dotenv_path)

print("Tentative d'appel à l'API OpenAI avec la clé chargée...")

try:
    client = OpenAI()  # Le client lit la clé depuis l'environnement

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    )

    print("\nSuccès ! L'API a répondu :")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\nUne erreur est survenue : {e}")
