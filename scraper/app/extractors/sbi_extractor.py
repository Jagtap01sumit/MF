import pandas as pd

from app.core.common.scheme_name_extractor import ExtractSchemeName


from app.core.common.extract_fund_type import extract_fund_type
from app.core.common.scheme_name_extractor import ExtractSchemeName
from app.core.common.amc_name_extractor import ExtractAMCName


class SBIExtractor:

    POSSIBLE_HEADERS = [
        "Name of the Instrument",
        "ISIN",
        "Quantity",
        "Industry/Rating",
    ]

    IGNORE_KEYWORDS = [
        "Sub Total",
        "Total",
        "DERIVATIVES",
        "Unlisted",
        "Grand Total",
        "TREPS",
        "Mutual Fund",
        "Net Receivable",
        "Reverse Repo",
    ]

    def extract(self, file_path):
        excel = pd.ExcelFile(file_path)
        all_data = []

        for sheet_name in excel.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            all_data.extend(self.process_sheet(df, sheet_name))

        return pd.DataFrame(all_data)
    def process_sheet(self, df, sheet_name):
        extracted = []

        scheme_name = ExtractSchemeName.extract_scheme_name(df)
        fund_type = extract_fund_type(scheme_name)
        amc_name = ExtractAMCName.extract_amc_name(df)

        ignore_keywords = {
        "sub total",
        "total",
        "derivatives",
        "unlisted",
        "grand total",
        "treps",
        "mutual fund",
        "net receivable",
        "reverse repo",
        }

        valid_prefixes = ("INE", "INF", "IDIA")

        for _, row in df.iterrows():
            values = [
            "" if pd.isna(v) else str(v).strip()
            for v in row.tolist()
        ]

            if len(values) < 7:
                continue

            instrument_name = values[2]
            isin = values[3]

            if not instrument_name:
                continue

            if any(keyword in instrument_name.lower() for keyword in        ignore_keywords):
                continue

            if not isin.startswith(valid_prefixes):
                continue

            extracted.append({
            "scheme_code": sheet_name,
            "scheme_name": scheme_name,
            "fund_type": fund_type,
            "isin": isin,
            "stock_name": instrument_name,
            "industry": values[4],
            "quantity": values[5],
            "market_value": values[6],
            "amc_name": amc_name,
        })

        return extracted