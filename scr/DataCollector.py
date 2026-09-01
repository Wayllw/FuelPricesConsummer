import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")
OUTPUT_DIR = Path("../data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_data(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["data"]

def main():
    # Etapa 2: Extrair dados e carregar no Pandas DataFrame
    print("Buscando dados da API...")
    data = fetch_data(API_URL)
    df = pd.DataFrame(data)
    print(f"DataFrame criado com sucesso! Formato: {df.shape}")

    csv_path = OUTPUT_DIR / "dados.csv"
    excel_path = OUTPUT_DIR / "dados.xlsx"
    parquet_path = OUTPUT_DIR / "dados.parquet"

    df.to_csv(csv_path, index=False)
    print(f"Arquivo CSV salvo em: {csv_path}")

    df.to_excel(excel_path, index=False, engine="openpyxl")
    print(f"Arquivo Excel salvo em: {excel_path}")

    df.to_parquet(parquet_path, index=False, engine="pyarrow")
    print(f"Arquivo Parquet salvo em: {parquet_path}")

if __name__ == "__main__":
    main()