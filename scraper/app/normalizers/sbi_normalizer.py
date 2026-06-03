import pandas as pd
from app.core.common.scheme_name_extractor import ExtractSchemeName


class PortfolioNormalizer:

    IGNORE_KEYWORDS = [
        "Sub Total",
        "Total",
        "Grand Total",
        "DERIVATIVES",
        "Unlisted",
        "TREPS",
        "Mutual Fund",
        "Net Receivable",
        "Reverse Repo",
    ]

    def normalize(self, df, report_month=None):

        normalized_rows = []

        # Standardize column names
        df.columns = [str(col).strip().lower() for col in df.columns]

        print("\n[NORMALIZATION STARTED]")

        print(f"Total Raw Rows: {len(df)}")

        for _, row in df.iterrows():

            stock_name = self.safe_str(row.get("stock_name", ""))
            scheme_name = ExtractSchemeName.extract_scheme_name(df)
            print(scheme_name + "name of schenme")
            # Skip empty rows
            if not stock_name:

                continue

            # Skip unwanted rows
            if any(
                keyword.lower() in stock_name.lower()
                for keyword in self.IGNORE_KEYWORDS
            ):

                continue

            normalized_row = {
                "scheme_code": self.safe_str(row.get("scheme_code", "")),
                "scheme_name": scheme_name,
                "isin": self.safe_str(row.get("isin", "")),
                "stock_name": stock_name,
                "industry": self.safe_str(row.get("industry", "")),
                "quantity": self.safe_int(row.get("quantity", 0)),
                "market_value": self.safe_float(row.get("market_value", 0)),
                "report_month": report_month,
            }

            # Skip rows without ISIN
            if not normalized_row["isin"]:

                continue

            normalized_rows.append(normalized_row)

        normalized_df = pd.DataFrame(normalized_rows)

        # Remove duplicates
        normalized_df.drop_duplicates(subset=["scheme_code", "isin"], inplace=True)

        # Reset clean index
        normalized_df.reset_index(drop=True, inplace=True)

        print(f"Normalized Rows: {len(normalized_df)}")

        print("\n[NORMALIZATION COMPLETED]")

        return normalized_df

    def safe_str(self, value):

        if pd.isna(value):

            return ""

        return str(value).strip()

    def safe_int(self, value):

        try:

            value = str(value).replace(",", "").strip()

            if value == "" or value.lower() == "nan":

                return 0

            return int(float(value))

        except:

            return 0

    def safe_float(self, value):

        try:

            value = str(value).replace(",", "").strip()

            if value == "" or value.lower() == "nan":

                return 0.0

            return float(value)

        except:

            return 0.0
