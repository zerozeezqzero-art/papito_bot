import requests
from dotenv import load_dotenv
import os


load_dotenv()


FOLDER_ID = os.getenv("FOLDER_ID")
API_KEY =  os.getenv("API_KEY")



def gpt_answer(text):
    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers={
            "Authorization": f"Api-Key {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
            "completionOptions": {
                "temperature": 0.6,
                "maxTokens": 1000
            },
            "messages": [
                {"role": "user", "text":text}
            ]
        }
    )
    
    return response.json()["result"]["alternatives"][0]["message"]["text"]
