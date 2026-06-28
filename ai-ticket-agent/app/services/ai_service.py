from openai import OpenAI
from dotenv import load_dotenv

import os
import json


# Cargar variables .env
load_dotenv()


# Cliente OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Función IA
def analyze_ticket(title, description):

    try:

        # Prompt IA
        prompt = f"""
        Analyze this support ticket.

        Return ONLY valid JSON.

        Ticket title:
        {title}

        Ticket description:
        {description}

        JSON format:
        {{
            "priority": "low/medium/high",
            "category": "bug/authentication/billing/general",
            "summary": "short summary",
            "recommended_action": "action recommendation"
        }}
        """


        # Request OpenAI
        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        # Texto IA
        result = response.choices[0].message.content


        # Convertir JSON string → Python dict
        parsed_result = json.loads(result)


        return parsed_result


    except Exception as e:

        return {
            "error": str(e)
        }