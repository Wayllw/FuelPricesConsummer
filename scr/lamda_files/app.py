import io
from curl_cffi import requests, CurlMime
import os
import certifi
import json
import datetime
import boto3
# import requests
import pandas as pd
from sqlalchemy import text,create_engine
import dataframe_image as dfi
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# from requests.adapters import HTTPAdapter
# from urllib3.util import create_urllib3_context

load_dotenv()
API_URL = os.getenv("API_URL")
aws_access_key= os.getenv("S3_ACCESS_KEY")
aws_secret_key= os.getenv("S3_SECRET_KEY")
aws_region_name= os.getenv("S3_REGION")
aws_bucket_name= os.getenv("S3_BUCKET_NAME")

postgres_url= os.getenv("DB_POSTGRES_RDS")
mysql_url= os.getenv("DB_MYSQL_RDS")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
users_postgres_url = os.getenv("db_telegram_users")

SMTP_USER = os.environ.get("SMTP_USER")
TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL")

session = boto3.client(
        service_name="s3",
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )
ses_client = boto3.client('ses', region_name='eu-west-3')


# class ModernTLSAdapter(HTTPAdapter):
#     def init_poolmanager(self, *args, **kwargs):
#         context = create_urllib3_context()
#         # Força o suporte a TLS moderno
#         context.set_ciphers('DEFAULT:@SECLEVEL=1')
#         kwargs['ssl_context'] = context
#         return super().init_poolmanager(*args, **kwargs)

def fetch_data(url: str) -> list:
    response = requests.get(url, impersonate="chrome", timeout=10)
    response.raise_for_status()

    return response.json().get("data", [])

def upload(date, csv, excel, parquet, img):
    # Upload CSV
    session.put_object(
        Bucket=aws_bucket_name,
        Body=csv,
        Key=f"{date}/dados.csv",
        ContentType="text/csv",
    )
    # Upload Excel
    session.put_object(
        Bucket=aws_bucket_name,
        Body=excel,
        Key=f"{date}/dados.xlsx",
        ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    # Upload Parquet
    session.put_object(
        Bucket=aws_bucket_name,
        Body=parquet,
        Key=f"{date}/dados.parquet",
        ContentType="application/octet-stream",
    )
    # Upload Image
    session.put_object(
        Bucket=aws_bucket_name,
        Body=img,
        Key=f"{date}/dados.png",
        ContentType="image/png",
    )

    print("Uploaded")

def send_email(img_bytes: bytes):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "Relatório de Preços de Combustível"
        msg['From'] = SMTP_USER
        msg['To'] = TO_EMAIL

        msg.attach(MIMEText("Segue em anexo o relatório simplificado.", 'plain'))
        att_img = MIMEApplication(img_bytes)
        att_img.add_header('Content-Disposition', 'attachment', filename='relatorio.png')
        msg.attach(att_img)

        # Envio via AWS SES
        response = ses_client.send_raw_email(
            Source=msg['From'],
            Destinations=[msg['To']],
            RawMessage={'Data': msg.as_string()}
        )

        print(f"E-mail enviado via SES! MessageID: {response['MessageId']}")
    except Exception as e:
        print(f" Erro ao enviar e-mail via SES: {e}")

def load_df_to_postgres(df: pd.DataFrame, table_name: str = "Fuel_Prices"):
    try:
        engine = create_engine(postgres_url)
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
        print(" Carga concluída com sucesso no PostgreSQL!")
    except Exception as e:
        print(f"Erro ao carregar no PostgreSQL: {e}")

def load_df_to_mysql(df: pd.DataFrame, table_name: str = "Fuel_Prices"):
    try:
        engine = create_engine(mysql_url)
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
        print(" Carga concluída com sucesso no MySQL!")
    except Exception as e:
        print(f"Erro ao carregar no MySQL: {e}")

def get_registered_users():
    try:
        engine = create_engine(users_postgres_url,)
        query = text("SELECT chat_id, first_name FROM telegram_users;")
        with engine.connect() as conn:
            result = conn.execute(query)
            rows= result.fetchall()
            return rows
    except Exception as e:
        print(f"Erro ao obter utilizadores da base de dados: {e}")
        return []

def telegram_notification(img_bytes):
    chat_ids= get_registered_users()
    if not chat_ids:
        print("Nenhum utilizador registado encontrado na base de dados.")
        return
    print(f"A iniciar o envio do relatório para {len(chat_ids)} utilizador(es)...")
    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id, name in chat_ids:
        try:
            message = f"🚀 Bom dia {name}.\n\n*Estes são os preços de hoje.*"
            mp=CurlMime()
            mp.addpart(name="photo", content_type="image/png", filename="dados.png", data=img_bytes)
            res=requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={"chat_id": chat_id, "caption":message,"parse_mode": "Markdown"}, multipart=mp, impersonate="chrome")
            mp.close()

            if res.status_code == 200:
                print(f" Relatório entregue com sucesso a: {name}")
            else:
                print(f" Falha na entrega a: {name}")

        except Exception as e:
            print(f" Erro ao enviar para o chat_id {chat_id}: {e}")

def lambda_handler(event, context):
    try:
        date = datetime.datetime.now().strftime("%Y%m%d")
        data = fetch_data(API_URL)
        df = pd.DataFrame(data)

        selected_fields = ['fuel_name', 'avg_price_eur', 'min_price_eur', 'max_price_eur', 'date']
        filtro = df[selected_fields]
        filtro.columns = ['Combustível', 'Média (€)', 'Mínimo (€)', 'Máximo (€)', 'Data']

        img_buffer = io.BytesIO()
        dfi.export(filtro, img_buffer, table_conversion="matplotlib")
        img_bytes = img_buffer.getvalue()

        csv_path=io.StringIO()
        df.to_csv(csv_path, index=False)
        csv_content = csv_path.getvalue().encode("utf8")

        excel_path=io.BytesIO()
        df.to_excel(excel_path, index=False, engine="openpyxl")
        excel_content = excel_path.getvalue()

        parquet_path=io.BytesIO()
        df.to_parquet(parquet_path, index=False, engine="pyarrow")
        parquet_content = parquet_path.getvalue()

        upload(date, csv_content, excel_content, parquet_content, img_bytes)
        load_df_to_postgres(df)
        load_df_to_mysql(df)
        telegram_notification(img_bytes)
        send_email(img_bytes)

    except Exception as e:
        print(f" Erro crítico na execução da Lambda: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Erro na execução: {str(e)}")
        }

if __name__ == "__main__":
    lambda_handler(None, None)