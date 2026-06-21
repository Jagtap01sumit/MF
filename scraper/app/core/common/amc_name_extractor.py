import pandas as pd
import os


class ExtractAMCName:
    @staticmethod
    def extract_amc_name(df=None, filepath=None):

    # ----------------------------------
    # Check filename first
    # ----------------------------------
        if filepath:

            filename = os.path.basename(filepath).lower()
            print(filename)
            print("file name hhhh")
            amc_mapping = {
            "ppfas": "PPFAS Mutual Fund",
            "quant": "Quant Mutual Fund",
            "sbi": "SBI Mutual Fund",
            "hdfc": "HDFC Mutual Fund",
            "icici": "ICICI Prudential Mutual Fund",
            "nippon": "Nippon India Mutual Fund",
            "axis": "Axis Mutual Fund",
            "kotak": "Kotak Mahindra Mutual Fund",
        }

            for keyword, amc_name in amc_mapping.items():

                if keyword in filename:
                    return amc_name

    # ----------------------------------
    # Existing logic
    # ----------------------------------
        for _, row in df.iterrows():

            for cell in row:

                if isinstance(cell, str) and "Mutual Fund" in cell:

                    return cell.strip()

        return None
