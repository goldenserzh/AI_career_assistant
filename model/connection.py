from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def connection() -> OpenAI:
    API_KEY = os.getenv("OPENROUTER_SECRET_KEY")

    if not API_KEY:
        raise ValueError("Не доступа к SECRET KEY для API")

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    return client


if __name__ == "__main__":
    client = connection()
    print(client)
