import pandas as pd


file_path = "downloads/Monthly_Portfolio_30042026.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="qSCF",
    header=7
)

print(df.head())