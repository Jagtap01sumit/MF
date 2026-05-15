import pandas as pd


class SBIExtractor:

    POSSIBLE_HEADERS = [
        "Name of the Instrument",
        "ISIN",
        "Quantity",
        "Industry/Rating"
    ]

    def safe_str(self, value):

        if pd.isna(value):
            return ""

        return str(value).strip()

    def safe_float(self, value):

        if pd.isna(value):
            return 0.0

        try:
            return float(value)

        except:
            return 0.0

    def extract(self, file_path):

        excel = pd.ExcelFile(file_path)

        all_data = []

        print(
            f"Sheets Found: {excel.sheet_names}"
        )

        for sheet_name in excel.sheet_names:

            print(
                f"Processing Sheet: {sheet_name}"
            )

            try:

                header_row = (
                    self.detect_header_row(
                        file_path,
                        sheet_name
                    )
                )

                print(
                    f"Header Found at Row: {header_row}"
                )

                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    header=header_row
                )

                rows = self.process_sheet(
                    df,
                    sheet_name
                )

                all_data.extend(rows)

            except Exception as e:

                print(
                    f"Skipping Sheet {sheet_name}: {e}"
                )

        final_df = pd.DataFrame(all_data)

        print(
            "\n[DATA EXTRACTED SUCCESSFULLY]"
        )

        print(
            final_df.head()
        )

        return final_df

    def detect_header_row(
        self,
        file_path,
        sheet_name
    ):

        preview_df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=None,
            nrows=20
        )

        for row_index in range(len(preview_df)):

            row_values = (
                preview_df.iloc[row_index]
                .astype(str)
                .str.strip()
                .tolist()
            )

            matched_headers = sum(

                header in row_values

                for header in self.POSSIBLE_HEADERS
            )

            if matched_headers >= 2:

                return row_index

        raise Exception(
            "Header row not found"
        )

    def process_sheet(
        self,
        df,
        sheet_name
    ):

        extracted = []

        ignore_keywords = [
            "Sub Total",
            "Total",
            "Grand Total",
            "TREPS",
            "Mutual Fund",
            "Net Receivable",
            "Reverse Repo"
        ]

        # Normalize column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        print(
            f"\nColumns in {sheet_name}:"
        )

        print(
            df.columns.tolist()
        )

        # Detect columns dynamically
        isin_column = None
        stock_column = None
        industry_column = None
        quantity_column = None
        market_value_column = None

        for col in df.columns:

            col_upper = col.upper()

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

        print("\nDetected Columns:")

        print(
            f"ISIN: {isin_column}"
        )

        print(
            f"Stock Name: {stock_column}"
        )

        print(
            f"Industry: {industry_column}"
        )

        print(
            f"Quantity: {quantity_column}"
        )

        print(
            f"Market Value: {market_value_column}"
        )

        for _, row in df.iterrows():

            isin = self.safe_str(
                row.get(
                    isin_column,
                    ""
                )
            )

            stock_name = self.safe_str(
                row.get(
                    stock_column,
                    ""
                )
            )

            # Skip empty rows
            if (
                stock_name == ""
                or stock_name.lower() == "nan"
            ):
                continue

            # Skip subtotal rows
            if any(
                keyword.lower()
                in stock_name.lower()
                for keyword in ignore_keywords
            ):
                continue

            # Accept valid rows
            if (
                isin
                and isin.lower() != "nan"
            ):

                extracted.append({

                    "scheme_code": sheet_name,

                    "isin": isin,

                    "stock_name": stock_name,

                    "industry": self.safe_str(
                        row.get(
                            industry_column,
                            ""
                        )
                    ),

                    "quantity": self.safe_float(
                        row.get(
                            quantity_column,
                            0
                        )
                    ),

                    "market_value": self.safe_float(
                        row.get(
                            market_value_column,
                            0
                        )
                    )

                })

        return extracted