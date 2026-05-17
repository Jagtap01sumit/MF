import pandas as pd


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

        ignore_keywords = ["Sub Total", "Total", "DERIVATIVES", "Unlisted"]

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

            # Actual stock rows
            if isin.startswith("INE"):

                extracted.append(
                    {
                        "scheme_code": sheet_name,
                        "isin": isin,
                        "stock_name": instrument_name,
                        "industry": values[4],
                        "quantity": values[5],
                        "market_value": values[6],
                    }
                )

        return extracted
