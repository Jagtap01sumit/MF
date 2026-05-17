import pandas as pd
import re


class ReportDateExtractor:

    def extract_report_month(self, filepath):

        try:

            # Read first few rows only
            temp_df = pd.read_excel(filepath, header=None, nrows=15)

            # Convert all cells to text
            rows_text = " ".join(temp_df.fillna("").astype(str).values.flatten())

            # Clean extra spaces
            rows_text = " ".join(rows_text.split())

            # Regex patterns
            patterns = [
                # 30-Apr-2026
                r"\d{1,2}[-/][A-Za-z]{3}[-/]\d{4}",
                # 30 April 2026
                r"\d{1,2}\s+[A-Za-z]+\s+\d{4}",
                # April 30 2026
                r"[A-Za-z]+\s+\d{1,2}\s+\d{4}",
                # Apr 2026
                r"[A-Za-z]{3,9}\s+\d{4}",
            ]

            for pattern in patterns:

                match = re.search(pattern, rows_text)

                if match:

                    extracted_date = match.group()

                    parsed_date = pd.to_datetime(extracted_date, errors="coerce")

                    if pd.notnull(parsed_date):

                        return parsed_date.strftime("%Y-%m-01")

            return None

        except Exception as e:

            print(f"[ERROR] Failed to extract report month: {e}")

            return None
