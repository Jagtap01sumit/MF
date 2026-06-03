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


class SBIExtractor:

    POSSIBLE_HEADERS = ["Name of the Instrument", "ISIN", "Quantity", "Industry/Rating"]

    def safe_str(self, value):

        if pd.isna(value):

            return ""

        return str(value).strip()

    def safe_float(self, value):

        if pd.isna(value):

            return 0.0

        try:

            value = str(value).replace(",", "").strip()

            if value == "":

                return 0.0

            return float(value)

        except:

            return 0.0

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

        for sheet_name in excel.sheet_names:

            print(f"\nProcessing Sheet: {sheet_name}")

            try:

                header_row = self.detect_header_row(file_path, sheet_name)

                print(f"Header Found at Row: {header_row}")

                df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)

                print("\nDATAFRAME TYPE:")
                print(type(df))

                print("\nDATAFRAME HEAD:")
                print(df.head())

                rows = self.process_sheet(df, sheet_name)

                all_data.extend(rows)

            except Exception as e:

                print(f"[WARNING] Skipping Sheet {sheet_name}: {e}")

        final_df = pd.DataFrame(all_data)

        if not final_df.empty:

            final_df = final_df.astype(
                {
                    "scheme_code": "string",
                    "isin": "string",
                    "stock_name": "string",
                    "industry": "string",
                }
            )

        print("\n[DATA EXTRACTED SUCCESSFULLY]")

        print(final_df.head())

        return final_df

    def detect_header_row(self, file_path, sheet_name):

        preview_df = pd.read_excel(
            file_path, sheet_name=sheet_name, header=None, nrows=20
        )

        for row_index in range(len(preview_df)):

            row_values = preview_df.iloc[row_index].astype(str).str.strip().tolist()

            matched_headers = 0

            for header in self.POSSIBLE_HEADERS:

                for value in row_values:

                    if header.lower() in str(value).lower():

                        matched_headers += 1

                        break

            print(f"\nROW {row_index}:")

            print(row_values)

            print(f"Matched Headers: {matched_headers}")

            if matched_headers >= 2:

                return row_index

        raise Exception("Header row not found")

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

            isin = self.safe_str(row.get(isin_column, ""))

            stock_name = self.safe_str(row.get(stock_column, ""))

            # Skip empty rows
            if stock_name == "" or stock_name.lower() == "nan":

                continue

            # Skip unwanted rows
            if any(
                keyword.lower() in stock_name.lower() for keyword in ignore_keywords
            ):

                continue

            # Accept only valid ISIN rows
            if isin and isin.lower() != "nan":

                extracted.append(
                    {
                        "scheme_code": str(sheet_name).strip(),
                        "isin": isin,
                        "stock_name": stock_name,
                        "industry": self.safe_str(row.get(industry_column, "")),
                        "quantity": self.safe_float(row.get(quantity_column, 0)),
                        "market_value": self.safe_float(
                            row.get(market_value_column, 0)
                        ),
                    }
                )

        print(f"\nExtracted Rows: {len(extracted)}")

        return extracted
