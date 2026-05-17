import pandas as pd
import re


class ExtractSchemeName:

    @staticmethod
    def extract_scheme_name(df):

        keywords = ["fund", "scheme", "plan", "growth", "direct"]

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
