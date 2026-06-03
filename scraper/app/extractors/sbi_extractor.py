import pandas as pd

from app.core.common.scheme_name_extractor import ExtractSchemeName
from app.core.common.amc_name_extractor import extract_amc_name


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

        # ======================================================
        # SKIP FIRST SHEET (INDEX SHEET)
        # ======================================================
        # sheets_to_process = excel.sheet_names[-1:]

        print(f"length Sheet: {len(excel.sheet_names)}")
        for sheet_name in excel.sheet_names:
            # for sheet_name in sheets_to_process:

            print(f"Processing Sheet: {sheet_name}")

            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

            normalized_rows = self.process_sheet(df, sheet_name)

            all_data.extend(normalized_rows)

        return pd.DataFrame(all_data)

    def process_sheet(self, df, sheet_name):

        extracted = []

        ignore_keywords = ["Sub Total", "Total", "DERIVATIVES", "Unlisted"]
        scheme_name = ExtractSchemeName.extract_scheme_name(df)
        print(f"scheme name: {scheme_name}")
        amc_name = extract_amc_name(df)
        print(f"amc name: {amc_name}")
        if len(df.columns) < 4:
            print(f"Skipping sheet {sheet_name} - less than 4 columns")
            return extracted
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

            isin = values[3]
            print(f"values Sheet: {values}")
            print(f"ISIN: {isin}")
            instrument_name = values[2]

            # Ignore subtotal / section rows
            if any(
                keyword.lower() in instrument_name.lower()
                for keyword in ignore_keywords
            ):
                continue

            # normalized_df["amc_name"] = amc_name
            # Actual stock rows
            if isin.startswith("INE"):

                extracted.append(
                    {
                        "scheme_code": sheet_name,
                        "scheme_name": scheme_name,
                        "isin": isin,
                        "stock_name": instrument_name,
                        "industry": values[4],
                        "quantity": values[5],
                        "market_value": values[6],
                        "amc_name": amc_name,
                    }
                )
        print("--------------------------")
        print(extracted)
        return extracted
