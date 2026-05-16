class PortfolioNormalizer:

    def normalize(self, df):

        import pandas as pd

        normalized_rows = []

        ignore_keywords = [
            "Sub Total",
            "Total",
            "Grand Total",
            "DERIVATIVES",
            "Unlisted"
        ]

        # Standardize column names
        df.columns = [
            str(col).strip().lower()
            for col in df.columns
        ]

        for _, row in df.iterrows():

            stock_name = str(
                row.get("stock_name", "")
            ).strip()

            # Skip empty rows
            if not stock_name:
                continue

            # Skip unwanted rows
            if any(
                keyword.lower() in stock_name.lower()
                for keyword in ignore_keywords
            ):
                continue

            normalized_row = {
                "scheme_code": str(
                    row.get("scheme_code", "")
                ).strip(),

                "isin": str(
                    row.get("isin", "")
                ).strip(),

                "stock_name": stock_name,

                "industry": str(
                    row.get("industry", "")
                ).strip(),

                "quantity": self.safe_int(
                    row.get("quantity", 0)
                ),

                "market_value": self.safe_float(
                    row.get("market_value", 0)
                ),
                "report_month": self.safe_float(
                    row.get("report_month",0)
                )
            }

            normalized_rows.append(
                normalized_row
            )

        normalized_df = pd.DataFrame(
            normalized_rows
        )

        # Remove duplicates
        normalized_df.drop_duplicates(
            subset=["scheme_code", "isin"],
            inplace=True
        )

        # Reset index
        normalized_df.reset_index(
            drop=True,
            inplace=True
        )

        return normalized_df

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