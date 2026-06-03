# import pandas as pd
# import re


# class ExtractSchemeName:

#     @staticmethod
#     def extract_scheme_name(df):

#         keywords = ["fund", "scheme", "plan", "growth", "direct"]

#         for _, row in df.iterrows():

#             for cell in row:

#                 if not isinstance(cell, str):
#                     continue

#                 text = cell.strip()

#                 # ======================================================
#                 # 1. Pattern: "Scheme Name: XYZ"
#                 # ======================================================
#                 match = re.search(r"scheme\s*name\s*[:\-]?\s*(.+)", text, re.IGNORECASE)

#                 if match:
#                     return match.group(1).strip()

#                 # ======================================================
#                 # 2. Keyword-based detection
#                 # ======================================================
#                 if any(k in text.lower() for k in keywords):

#                     if "mutual fund" not in text.lower():

#                         # cleaned =
#                         cleaned = text.strip()

#                         if len(cleaned) > 5:
#                             return cleaned

#         return None

import pandas as pd
import re


class ExtractSchemeName:

    @staticmethod
    def extract_scheme_name(df):

        keywords = ["fund", "scheme", "plan", "growth", "direct"]

        for row_idx, row in df.iterrows():

            values = [str(v).strip() if pd.notna(v) else "" for v in row.tolist()]

            for col_idx, cell in enumerate(values):

                if not cell:
                    continue

                # ======================================================
                # Case 1:
                # "Scheme Name: SBI Bluechip Fund"
                # ======================================================
                match = re.search(
                    r"scheme\s*name\s*[:\-]?\s*(.*)",
                    cell,
                    re.IGNORECASE,
                )

                if match:

                    extracted_name = match.group(1).strip()

                    # Name exists in same cell
                    if (
                        extracted_name
                        and extracted_name != ":"
                        and len(extracted_name) > 2
                    ):
                        return extracted_name

                    # ==================================================
                    # NEW CASE
                    # "Scheme Name:" | "SBI Bluechip Fund"
                    # ==================================================
                    for next_col in range(col_idx + 1, len(values)):

                        next_cell = values[next_col].strip()

                        if next_cell and "scheme name" not in next_cell.lower():
                            return next_cell

                # ======================================================
                # Case 2:
                # ["Scheme Name", "SBI Bluechip Fund"]
                # ======================================================
                if re.fullmatch(
                    r"scheme\s*name\s*[:\-]?",
                    cell,
                    re.IGNORECASE,
                ):

                    for next_col in range(col_idx + 1, len(values)):

                        next_cell = values[next_col].strip()

                        if next_cell:
                            return next_cell

            # ======================================================
            # Case 3:
            # Fallback keyword search
            # ======================================================
            for cell in values:

                if not cell:
                    continue

                if any(k in cell.lower() for k in keywords):

                    if "mutual fund" not in cell.lower():

                        cleaned = cell.strip()

        for _, row in df.iterrows():

            for cell in row:

                if not isinstance(cell, str):
                    continue

                text = cell.strip()

                # ======================================================
                # 1. Pattern: "Scheme Name: XYZ"
                # ======================================================
                match = re.search(r"scheme\s*name\s*[:\-]?\s*(.+)", text, re.IGNORECASE)

                if match:
                    return match.group(1).strip()

                # ======================================================
                # 2. Keyword-based detection
                # ======================================================
                if any(k in text.lower() for k in keywords):

                    if "mutual fund" not in text.lower():

                        cleaned = re.split(r"-|:", text)[0].strip()

                        if len(cleaned) > 5:
                            return cleaned

        return None
