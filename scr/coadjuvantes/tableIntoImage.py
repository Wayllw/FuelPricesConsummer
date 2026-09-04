import pandas as pd
from pathlib import Path
import dataframe_image as dfi

def getImage():
    excel_path = Path('../data/dados.xlsx')
    df = pd.read_excel(excel_path)

    selected_fields = ['fuel_name', 'avg_price_eur', 'min_price_eur', 'max_price_eur','date']
    filtro = df[selected_fields]
    filtro.to_excel('../data/dadosSimplificados.xlsx', index=False)
    output_image_path = Path('../data/dados.png')
    dfi.export(filtro.head(15), str(output_image_path), table_conversion="matplotlib")

if __name__ == '__main__':
    getImage()