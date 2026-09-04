import requests
from dotenv import load_dotenv
import os
from scr.coadjuvantes.engines import get_users_engine
from sqlalchemy import text


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def get_registered_users():
    engine = get_users_engine()
    query = text("SELECT chat_id, first_name FROM telegram_users;")
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            rows= result.fetchall()
            chat_ids = [row[0] for row in rows]
            names = [row[1] for row in rows]
            return chat_ids, names
    except Exception as e:
        print(f"Erro ao obter utilizadores da base de dados: {e}")
        return []


def main():
    chat_ids, names = get_registered_users()
    image_path = "../data/dados.png"

    if not chat_ids:
        print("Nenhum utilizador registado encontrado na base de dados.")
        return

    print(f"A iniciar o envio do relatório para {len(chat_ids)} utilizador(es)...")

    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    for chat_id in chat_ids:
        try:
            message = f"🚀 Bom dia {names}.\n\n*Estes são os preços de hoje.*"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(text_url, json=payload, timeout=5)

            # 2. Envia a imagem do relatório (se existir)
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as photo:
                    requests.post(
                        photo_url,
                        data={"chat_id": chat_id},
                        files={"photo": photo},
                        timeout=10
                    )
            print(f" Relatório entregue com sucesso ao chat_id: {chat_id}")

        except Exception as e:
            print(f" Erro ao enviar para o chat_id {chat_id}: {e}")

if __name__ == "__main__":
    main()