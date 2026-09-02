import json
import os
import requests
from sqlalchemy import create_engine, text

DB_URL = os.getenv("RDS_DB_URL")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
engine = create_engine(DB_URL, pool_pre_ping=True)



def save_user(chat_id, first_name, username):
    query = text(""" 
        CREATE TABLE IF NOT EXISTS telegram_users(
            chat_id BIGINT PRIMARY KEY,
            first_name VARCHAR (255),
            username VARCHAR (255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
            
        INSERT INTO telegram_users (chat_id, first_name, username)
        VALUES (:chat_id, :first_name, :username) ON CONFLICT (chat_id) DO
        UPDATE
        SET first_name = EXCLUDED.first_name, username = EXCLUDED.username;
        """)
    with engine.connect() as conn:
        conn.execute(query, {
            "chat_id": chat_id,
            "first_name": first_name,
            "username": username
        })
        conn.commit()


def send_message(chat_id, text_to_send):
    """Envia uma mensagem de texto para o utilizador via Telegram API."""
    try:
        text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text_to_send,
            "parse_mode": "Markdown"
        }
        res = requests.post(text_url, json=payload, timeout=5)
        print(f"Telegram API status: {res.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        if "message" in body:
            chat_id = body["message"]["chat"]["id"]
            first_name = body["message"]["chat"].get("first_name", "")
            username = body["message"]["chat"].get("username", "")

            # Obtém o texto enviado pelo utilizador (convertido para minúsculas para facilitar a comparação)
            user_text = body["message"].get("text", "").strip().lower()

            # Garante que o utilizador fica registado na BD em qualquer interação
            save_user(chat_id, first_name, username)

            RESPOSTAS = {
                "ping": "pong",
                "pao": "manteiga",
                "ola": f"Olá {first_name}!👋 \nEspero que tudo esteja bem. \nUm dia com muito sol para ti!",
                "adeus": f"Até já {first_name}!👋 \nEspero que voltes rápido, vai com cuidado!",
                "xau": f"Até já {first_name}!👋 \nEspero que voltes rápido, vai com cuidado!",
                "/start": f"Olá {first_name}! 👋 \nFicaste registado para receber os relatórios diários de combustíveis. \nFaz /help para obteres a lista de comandos.",
                "/estado": "Estamos em desenvolvimento atualmente, esperamos trazer novas funcionalidades em breve.",
                "/preço": "",
                "/dono": "Olá. Chamo-me Rui. Se caíste aqui desamparado, este bot faz parte de um projeto pessoal de software development.",
                "/help": "🤖 *Comandos disponíveis:*\n\n• /start — Regista o contacto no sistema\n• /estado — Consulta o estado do bot\n• /dono — Informações sobre o projeto\n• `ping` — Testa a resposta do bot\n• `pao` — Manteiga!\n• `ola`\n• `adeus ou xau`"
            }

            # --- LÓGICA DE RESPOSTAS ESPECÍFICAS ---
            if user_text in RESPOSTAS:
                send_message(chat_id, RESPOSTAS[user_text])
            else:
                # Resposta padrão caso ele diga algo não reconhecido
                send_message(
                    chat_id,
                    f"Comando não reconhecido. Escreve /help ou aguarda pelo próximo relatório de combustíveis! 🚀"
                )

        return {"statusCode": 200, "body": json.dumps("OK")}

    except Exception as e:
        print(f"Erro na execução da Lambda: {e}")
        return {"statusCode": 500, "body": json.dumps(str(e))}