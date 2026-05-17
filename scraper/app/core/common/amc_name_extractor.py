import pandas as pd


def extract_amc_name(df):

    # df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)

    for _, row in df.iterrows():
        for cell in row:
            if isinstance(cell, str) and "Mutual Fund" in cell:
                return cell.strip()

    return None
