import pandas as pd

from app.core.common.scheme_name_extractor import ExtractSchemeName
from app.core.common.amc_name_extractor import ExtractAMCName
from app.core.common.extract_fund_type import extract_fund_type


class PPFASExcelExtractor:

    def extract(self, file_path):
       
      
        excel = pd.ExcelFile(file_path)

        all_data = []

        for sheet_name in excel.sheet_names:

            print(f"Processing Sheet: {sheet_name}")

            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

            normalized_rows = self.process_sheet(df, sheet_name,file_path)

            all_data.extend(normalized_rows)

        return pd.DataFrame(all_data)

    def process_sheet(self, df, sheet_name,file_path):

        extracted = []
        VALID_ISIN_PREFIXES = ("INE", "INF", "IDIA")
        amc_name = ExtractAMCName.extract_amc_name(df,file_path)
        ignore_keywords = ["Sub Total", "Total", "DERIVATIVES", "Unlisted"]
        scheme_name = ExtractSchemeName.extract_scheme_name(df)
        fund_type = extract_fund_type(scheme_name)
      
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

            isin = values[2]

            instrument_name = values[1]

            # Ignore subtotal / section rows
            if any(
                keyword.lower() in instrument_name.lower()
                for keyword in ignore_keywords
            ):
                continue

            # normalized_df["amc_name"] = amc_name
            # Actual stock rows
             
            if isin.startswith(VALID_ISIN_PREFIXES):
                extracted.append(
                    {
                        "scheme_code": sheet_name,
                        "scheme_name": scheme_name,
                        "fund_type":fund_type,
                        "isin": isin,
                        "stock_name": instrument_name,
                        "industry": values[3],
                        "quantity": values[4],
                        "market_value": values[5],
                        "amc_name": amc_name,
                    }
                )

        return extracted
