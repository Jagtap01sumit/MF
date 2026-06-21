import pandas as pd

from app.core.common.scheme_name_extractor import ExtractSchemeName
# from app.core.common.amc_name_extractor import extract_amc_name
from app.core.common.extract_fund_type import extract_fund_type
from app.core.common.amc_name_extractor import ExtractAMCName

class QUANTExcelExtractor:

    def extract(self, file_path):

        excel = pd.ExcelFile(file_path)

        all_data = []

        for sheet_name in excel.sheet_names:

            print(f"Processing Sheet: {sheet_name}")

            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

            normalized_rows = self.process_sheet(df, sheet_name)

            all_data.extend(normalized_rows)

        return pd.DataFrame(all_data)

    def process_sheet(self, df, sheet_name):

        extracted = []
        VALID_ISIN_PREFIXES = ("INE", "INF", "IDIA")
        ignore_keywords = ["Sub Total", "Total", "DERIVATIVES", "Unlisted"]
        scheme_name = ExtractSchemeName.extract_scheme_name(df)
        fund_type = extract_fund_type(scheme_name)
        # print(scheme_name + "scheme name")
        amc_name = ExtractAMCName.extract_amc_name(df)
        # print(amc_name + "amc name")

        for _, row in df.iterrows():

            values = []

            for value in row.tolist():

                if pd.isna(value):

                    values.append("")

                else:

                    values.append(str(value).strip())

            # Ignore completely empty rows
            if all(v == "" for v in values):
                continue

            isin = values[1]

            instrument_name = values[2]

            # Ignore subtotal / section rows
            if any(
                keyword.lower() in instrument_name.lower()
                for keyword in ignore_keywords
            ):
                continue

        #    if len(isin) >= 10 and isin.isalnum():
        #         extracted.append(...)

            if isin.startswith(VALID_ISIN_PREFIXES):

                extracted.append(
                    {
                        "scheme_code": sheet_name,
                        "scheme_name": scheme_name,
                        "fund_type":fund_type,
                        "isin": isin,
                        "stock_name": instrument_name,
                        "industry": values[4],
                        "quantity": values[5],
                        "market_value": values[6],
                        "amc_name": amc_name,
                    }
                )

        return extracted
