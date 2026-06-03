# import pandas as pd
# import re


# class ReportDateExtractor:

#     def extract_report_month(self, filepath):

#         try:

#             temp_df = pd.read_excel(filepath, header=None, nrows=15)

#             # Convert all cells to text
#             rows_text = " ".join(temp_df.fillna("").astype(str).values.flatten())

#             # Clean extra spaces
#             rows_text = " ".join(rows_text.split())

#             # Regex patterns
#             patterns = [
#                 # 30-Apr-2026
#                 r"\d{1,2}[-/][A-Za-z]{3}[-/]\d{4}",
#                 # 30 April 2026
#                 r"\d{1,2}\s+[A-Za-z]+\s+\d{4}",
#                 # April 30 2026
#                 r"[A-Za-z]+\s+\d{1,2}\s+\d{4}",
#                 # Apr 2026
#                 r"[A-Za-z]{3,9}\s+\d{4}",
#             ]

#             for pattern in patterns:

#                 match = re.search(pattern, rows_text)

#                 if match:

#                     extracted_date = match.group()

#                     parsed_date = pd.to_datetime(extracted_date, errors="coerce")

#                     if pd.notnull(parsed_date):

#                         return parsed_date.strftime("%Y-%m-01")

#             return None

#         except Exception as e:

#             print(f"[ERROR] Failed to extract report month: {e}")

#             return None

import pandas as pd
import re
import os


class ReportDateExtractor:

    def extract_report_month(self, filepath):

        try:

            temp_df = pd.read_excel(filepath, header=None, nrows=15)

            rows_text = " ".join(temp_df.fillna("").astype(str).values.flatten())

            rows_text = " ".join(rows_text.split())

            patterns = [
                r"\d{1,2}[-/][A-Za-z]{3}[-/]\d{4}",
                r"\d{1,2}\s+[A-Za-z]+\s+\d{4}",
                r"[A-Za-z]+\s+\d{1,2}\s+\d{4}",
                r"[A-Za-z]{3,9}\s+\d{4}",
            ]

            for pattern in patterns:

                match = re.search(pattern, rows_text)

                if match:

                    extracted_date = match.group()

                    parsed_date = pd.to_datetime(extracted_date, errors="coerce")

                    if pd.notnull(parsed_date):
                        return parsed_date.strftime("%Y-%m-01")

            # ==================================================
            # NEW CASE: Extract from filename
            # Example:
            # All-Schemes-Monthly-Portfolio---as-on-30th-April-2026.xlsx
            # ==================================================

            filename = os.path.basename(filepath)

            filename_match = re.search(
                r"(\d{1,2})(?:st|nd|rd|th)?[- ]([A-Za-z]+)[- ](\d{4})",
                filename,
                re.IGNORECASE,
            )

            if filename_match:

                day = filename_match.group(1)
                month = filename_match.group(2)
                year = filename_match.group(3)

                date_str = f"{day} {month} {year}"

                parsed_date = pd.to_datetime(date_str, errors="coerce")

                if pd.notnull(parsed_date):
                    return parsed_date.strftime("%Y-%m-01")

            return None

        except Exception as e:

            print(f"[ERROR] Failed to extract report month: {e}")

            return None
