import pandas as pd
from pathlib import Path
from engines import get_mysql_engine


def load_to_mysql():
    data_path = Path("../data/dados.csv")

    if not data_path.exists():
        raise FileNotFoundError("O arquivo dados.csv não foi encontrado. Execute extract.py primeiro.")

    df = pd.read_csv(data_path)
    engine = get_mysql_engine()

    print("Iniciando carga no MySQL...")
    df.to_sql("Fuel_Prices", con=engine, if_exists="replace", index=False)
    print(" Carga concluída com sucesso no MySQL!")


if __name__ == "__main__":
    load_to_mysql()