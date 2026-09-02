import requests
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MY_TOKEN = os.getenv("TELEGRAM_PERSONAL_TOKEN")

message="🚀 *Pipeline Executado com Sucesso!*\n\nOs arquivos foram salvos no S3 e atualizados nas bases de dados.\n\n*Estes são os preços de hoje.*"
image_path="../data/dados.png"

def main(message: str=message, image_path: str = image_path):
    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_TOKEN,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(text_url, json=payload)

    if image_path:
        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as photo:
            requests.post(photo_url, data={"chat_id": MY_TOKEN}, files={"photo": photo})

if __name__ == "__main__":
    main()