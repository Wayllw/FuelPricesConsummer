import pandas as pd
from pathlib import Path
from scr.coadjuvantes.engines import get_postgres_engine


def load_to_postgres():
    data_path = Path("../data/dados.csv")

    if not data_path.exists():
        raise FileNotFoundError("O arquivo dados.csv não foi encontrado. Execute extract.py primeiro.")

    df = pd.read_csv(data_path)
    engine = get_postgres_engine()

    print("Iniciando carga no PostgreSQL...")
    df.to_sql("Fuel_Prices", con=engine, if_exists="append", index=False)
    print(" Carga concluída com sucesso no PostgreSQL!")


if __name__ == "__main__":
    load_to_postgres()