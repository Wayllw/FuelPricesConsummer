import pandas as pd
from pathlib import Path
from scr.coadjuvantes.engines import get_oracle_engine
from sqlalchemy.types import  VARCHAR, BOOLEAN, DATE, TIMESTAMP
from sqlalchemy.dialects.oracle import FLOAT, NUMBER


def load_to_oracle():
    data_path = Path("../data/dados.csv")

    if not data_path.exists():
        raise FileNotFoundError("O arquivo dados.csv não foi encontrado. Execute extract.py primeiro.")

    oracle_dtypes = {
        'fuel_slug': VARCHAR(50),
        'fuel_name': VARCHAR(100),
        'road_vehicle': BOOLEAN,
        'avg_price_eur': FLOAT(binary_precision=53),
        'min_price_eur': FLOAT(binary_precision=53),
        'max_price_eur': FLOAT(binary_precision=53),
        'station_count': FLOAT(binary_precision=53),
        'date': VARCHAR(20),
        'updated_at': VARCHAR(50)
    }

    df = pd.read_csv(data_path)
    engine = get_oracle_engine()

    print("Iniciando carga no Oracle...")
    df.to_sql("Fuel_Prices", con=engine, if_exists="append", index=False, dtype=oracle_dtypes)
    print(" Carga concluída com sucesso no Oracle!")


if __name__ == "__main__":
    load_to_oracle()