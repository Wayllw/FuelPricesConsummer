import os, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import datetime
from pathlib import Path
from scr.coadjuvantes.tableIntoImage import getImage

getImage()
load_dotenv()
data=datetime.datetime.now().strftime("%d/%m/%Y")

TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL")
TO_EMAIL2 = os.environ.get("CONTACT_TO_EMAIL2")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")


def main():
    mensagem=f"Bom Dia.\nEstes são os preços da gasolina no dia de hoje {data}! \n\nEspero que o dia corra bem!"
    assunto="Preço da Gasolina"

    body_lines = [
        mensagem,
    ]
    body = "\n".join([line for line in body_lines if line is not None])

    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    #msg["CC"] = TO_EMAIL2
    msg["Subject"] = assunto
    msg.set_content(body)

    attachment_file = Path("../data/dados.png")
    with open(attachment_file, "rb") as attachment:
        msg.add_attachment(
            attachment.read(),
            maintype="image",
            subtype="jpeg",
            filename=attachment_file.name,
        )

    # send via SMTP (Gmail example)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
