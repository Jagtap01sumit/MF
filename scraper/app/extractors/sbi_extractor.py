import pandas as pd

from app.core.common.scheme_name_extractor import ExtractSchemeName
from app.core.common.amc_name_extractor import extract_amc_name


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

        print(f"Sheets Found: {excel.sheet_names}")

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

        ignore_keywords = [
            "Sub Total",
            "Total",
            "Grand Total",
            "TREPS",
            "Mutual Fund",
            "Net Receivable",
            "Reverse Repo",
        ]

        print("\nPROCESS SHEET CALLED")

        print("\nDF TYPE:")
        print(type(df))

        print("\nDF COLUMNS:")
        print(df.columns.tolist())

        # Normalize columns
        df.columns = [str(col).strip().lower() for col in df.columns]

        print("\nNORMALIZED COLUMNS:")
        print(df.columns.tolist())

        # Dynamic column detection
        isin_column = None
        stock_column = None
        industry_column = None
        quantity_column = None
        market_value_column = None

        for col in df.columns:

            col_upper = str(col).upper().strip()

            if "ISIN" in col_upper:

                isin_column = col

            elif "NAME OF THE INSTRUMENT" in col_upper:

                stock_column = col

            elif "INDUSTRY" in col_upper:

                industry_column = col

            elif "QUANTITY" in col_upper:

                quantity_column = col

            elif "MARKET" in col_upper:

                market_value_column = col

        print("\nDETECTED COLUMNS:")

        print(f"ISIN: {isin_column}")

        print(f"Stock Name: {stock_column}")

        print(f"Industry: {industry_column}")

        print(f"Quantity: {quantity_column}")

        print(f"Market Value: {market_value_column}")

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
