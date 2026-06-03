### Folder structure

```
scraper/
│
├── app/
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── constants.py
│   │   └── logging_config.py
│   │
│   ├── core/
│   │   ├── base_scraper.py
│   │   ├── base_parser.py
│   │   ├── base_downloader.py
│   │   ├── base_normalizer.py
│   │   └── exceptions.py
│   │
│   ├── scrapers/
│   │   ├── sbi/
│   │   │   ├── sbi_scraper.py
│   │   │   ├── sbi_parser.py
│   │   │   └── sbi_config.py
│   │   │
│   │   ├── hdfc/
│   │   └── quant/
│   │
│   ├── parsers/
│   │   ├── pdf/
│   │   │   ├── pdf_parser.py
│   │   │   └── camelot_parser.py
│   │   │
│   │   ├── excel/
│   │   │   └── excel_parser.py
│   │   │
│   │   └── html/
│   │       └── html_parser.py
│   │
│   ├── normalizers/
│   │   ├── stock_normalizer.py
│   │   ├── sector_normalizer.py
│   │   └── cleaner.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── repositories/
│   │   │   ├── holdings_repository.py
│   │   │   └── funds_repository.py
│   │   │
│   │   └── models/
│   │
│   ├── services/
│   │   ├── comparison_service.py
│   │   ├── holdings_service.py
│   │   └── snapshot_service.py
│   │
│   ├── utils/
│   │   ├── file_utils.py
│   │   ├── date_utils.py
│   │   ├── retry_utils.py
│   │   ├── validators.py
│   │   └── logger.py
│   │
│   ├── downloads/
│   │
│   ├── extracted/
│   │
│   └── logs/
│
├── tests/
│
├── requirements.txt
│
├── .env
│
├── main.py
│
└── README.md

```

### STEP 1 — Install Dependencies

```
pip install playwright pandas openpyxl python-dotenv

playwright install


```

```
pip install sqlalchemy psycopg2-binary python-dotenv
```

# Mutual Fund Analytics Database Design

---

# 📊 Tables & Relations Diagram

```text
┌────────────────────┐
│       amcs         │
├────────────────────┤
│ id (PK)            │
│ amc_name           │
│ created_at         │
└─────────┬──────────┘
          │
          │ 1 → Many
          ▼
┌────────────────────┐
│      schemes       │
├────────────────────┤
│ id (PK)            │
│ amc_id (FK)        │
│ scheme_code        │
│ scheme_name        │
│ created_at         │
└─────────┬──────────┘
          │
          │ 1 → Many
          ▼
┌────────────────────────────────────┐
│             portfolio              │
├────────────────────────────────────┤
│ id (PK)                            │
│ scheme_id (FK)                     │
│ stock_id (FK)                      │
│ report_month                       │
│ quantity                           │
│ market_value                       │
│ created_at                         │
└─────────┬──────────────────────────┘
          │
          │ Many → 1
          ▼
┌────────────────────┐
│       stocks       │
├────────────────────┤
│ id (PK)            │
│ isin               │
│ stock_name         │
│ industry_id (FK)   │
│ created_at         │
└─────────┬──────────┘
          │
          │ Many → 1
          ▼
┌────────────────────┐
│     industries     │
├────────────────────┤
│ id (PK)            │
│ industry_name      │
│ created_at         │
└────────────────────┘
```

# Extractor function flow

## Overview

The `SBIExtractor` class reads an Excel file containing mutual fund portfolio data, processes each sheet, extracts stock holdings, and returns the result as a Pandas DataFrame.

---

## Step 1: Open Excel File

```python
excel = pd.ExcelFile(file_path)
```

This loads the Excel workbook and gives access to all sheet names.

Example:

```python
excel.sheet_names
# ['INDEX', 'SCHEME_1', 'SCHEME_2']
```

---

## Step 2: Process Each Sheet

```python
for sheet_name in excel.sheet_names:
```

The code processes sheets one by one.

For every sheet:

```python
df = pd.read_excel(
    file_path,
    sheet_name=sheet_name,
    header=None
)
```

The entire sheet is loaded into a DataFrame.

Then:

```python
normalized_rows = self.process_sheet(df, sheet_name)
```

All extracted stock records from that sheet are returned.

---

## Step 3: Extract Scheme & AMC Name

Inside `process_sheet()`:

```python
scheme_name = ExtractSchemeName.extract_scheme_name(df)
amc_name = extract_amc_name(df)
```

These helper functions identify:

- Scheme Name
- AMC Name

from the sheet contents.

Example:

```text
Scheme Name:
SBI Bluechip Fund

AMC Name:
SBI Mutual Fund
```

---

## Step 4: Loop Through Every Row

```python
for _, row in df.iterrows():
```

The code processes each row one by one.

Example row:

| Col0 | Col1 | Col2                | Col3         | Col4      | Col5 | Col6    |
| ---- | ---- | ------------------- | ------------ | --------- | ---- | ------- |
|      |      | Reliance Industries | INE002A01018 | Oil & Gas | 1000 | 1500000 |

---

## Step 5: Convert Row Into `values` Array

```python
values = []
```

Every column value of the row is stored in the `values` list.

```python
for value in row.tolist():
```

If the cell is empty:

```python
values.append("")
```

Otherwise:

```python
values.append(str(value).strip())
```

Example:

```python
values = [
    "",
    "",
    "Reliance Industries",
    "INE002A01018",
    "Oil & Gas",
    "1000",
    "1500000"
]
```

### Column Mapping

```python
values[0] -> Column A
values[1] -> Column B
values[2] -> Instrument Name
values[3] -> ISIN
values[4] -> Industry
values[5] -> Quantity
values[6] -> Market Value
```

---

## Step 6: Skip Empty Rows

```python
if all(v == "" for v in values):
    continue
```

If every column is empty, the row is ignored.

---

## Step 7: Read Important Fields

```python
isin = values[3]
instrument_name = values[2]
```

Example:

```python
isin = "INE002A01018"
instrument_name = "Reliance Industries"
```

---

## Step 8: Ignore Total/Subtotal Rows

```python
if any(
    keyword.lower() in instrument_name.lower()
    for keyword in ignore_keywords
):
    continue
```

Rows containing:

```text
Sub Total
Total
DERIVATIVES
Unlisted
```

are skipped.

These rows are not actual stock holdings.

---

## Step 9: Check ISIN

```python
if isin.startswith("INE"):
```

The code only keeps rows whose ISIN starts with:

```text
INE
```

Example:

```text
INE002A01018  -> Accepted
INE009A01021  -> Accepted
INF123456789  -> Ignored
```

Reason:

Most Indian listed equity securities have ISINs beginning with `INE`.

---

## Step 10: Save Stock Record

When the ISIN starts with `INE`, a dictionary is created:

```python
{
    "scheme_code": sheet_name,
    "scheme_name": scheme_name,
    "isin": isin,
    "stock_name": instrument_name,
    "industry": values[4],
    "quantity": values[5],
    "market_value": values[6],
    "amc_name": amc_name,
}
```

Example:

```python
{
    "scheme_code": "Sheet1",
    "scheme_name": "SBI Bluechip Fund",
    "isin": "INE002A01018",
    "stock_name": "Reliance Industries",
    "industry": "Oil & Gas",
    "quantity": "1000",
    "market_value": "1500000",
    "amc_name": "SBI Mutual Fund"
}
```

This dictionary is appended to:

```python
extracted
```

---

## Step 11: Return Extracted Records

At the end of sheet processing:

```python
return extracted
```

Example:

```python
[
    {...},
    {...},
    {...}
]
```

---

## Step 12: Combine Data From All Sheets

Back in `extract()`:

```python
all_data.extend(normalized_rows)
```

Records from every sheet are merged into a single list.

Finally:

```python
return pd.DataFrame(all_data)
```

A final DataFrame is created.

Example:

| scheme_name       | stock_name          | isin         | quantity |
| ----------------- | ------------------- | ------------ | -------- |
| SBI Bluechip Fund | Reliance Industries | INE002A01018 | 1000     |
| SBI Bluechip Fund | HDFC Bank           | INE040A01034 | 500      |
| SBI Bluechip Fund | Infosys             | INE009A01021 | 750      |

---

## Complete Flow Summary

```
text
Excel File
    │
    ▼
Read Sheet 1
    │
    ▼
Read Row
    │
    ▼
Store Columns in values[]
    │
    ▼
Extract Instrument Name & ISIN
    │
    ▼
Ignore Empty/Total Rows
    │
    ▼
Check:
ISIN starts with "INE" ?
    │
 ┌──┴──┐
 │ Yes │
 └──┬──┘
    ▼
Save Record
    │
    ▼
Process Next Row
    │
    ▼
Process Next Sheet
    │
    ▼
Combine All Records
    │
    ▼
Return Final DataFrame
```

## ``

````
import logging
from typing import Dict, List

import pandas as pd

from app.core.common.scheme_name_extractor import ExtractSchemeName
from app.core.common.amc_name_extractor import extract_amc_name


logger = logging.getLogger(__name__)


class SBIExtractor:
    """
    Extract equity holdings from SBI Mutual Fund portfolio files.
    """

    # Column positions
    INSTRUMENT_NAME_COL = 2
    ISIN_COL = 3
    INDUSTRY_COL = 4
    QUANTITY_COL = 5
    MARKET_VALUE_COL = 6

    MIN_REQUIRED_COLUMNS = 7

    IGNORE_KEYWORDS = {
        "sub total",
        "total",
        "derivatives",
        "unlisted",
        "grand total",
        "treps",
        "mutual fund",
        "net receivable",
        "reverse repo",
    }

    def extract(self, file_path: str) -> pd.DataFrame:
        """
        Process all sheets and return normalized holdings.
        """

        excel = pd.ExcelFile(file_path)
        all_records: List[Dict] = []

        for sheet_name in excel.sheet_names:
            logger.info("Processing sheet: %s", sheet_name)

            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=None
            )

            records = self.process_sheet(df, sheet_name)
            all_records.extend(records)

        return pd.DataFrame(all_records)

    def process_sheet(
        self,
        df: pd.DataFrame,
        sheet_name: str
    ) -> List[Dict]:

        # Skip sheets with insufficient columns
        if len(df.columns) < self.MIN_REQUIRED_COLUMNS:
            logger.warning(
                "Skipping sheet %s. Expected at least %s columns, found %s",
                sheet_name,
                self.MIN_REQUIRED_COLUMNS,
                len(df.columns),
            )
            return []

        scheme_name = ExtractSchemeName.extract_scheme_name(df)
        amc_name = extract_amc_name(df)

        logger.info("Scheme Name: %s", scheme_name)
        logger.info("AMC Name: %s", amc_name)

        extracted_records: List[Dict] = []

        for _, row in df.iterrows():

            values = self._normalize_row(row)

            if not values:
                continue

            record = self._extract_record(
                values=values,
                sheet_name=sheet_name,
                scheme_name=scheme_name,
                amc_name=amc_name,
            )

            if record:
                extracted_records.append(record)

        return extracted_records

    def _normalize_row(self, row: pd.Series) -> List[str]:
        """
        Convert row values to cleaned strings.
        """

        values = [
            "" if pd.isna(value) else str(value).strip()
            for value in row.tolist()
        ]

        if all(v == "" for v in values):
            return []

        return values

    def _extract_record(
        self,
        values: List[str],
        sheet_name: str,
        scheme_name: str,
        amc_name: str,
    ) -> Dict | None:
        """
        Extract stock record from a row.
        """

        if len(values) < self.MIN_REQUIRED_COLUMNS:
            return None

        instrument_name = values[self.INSTRUMENT_NAME_COL]
        isin = values[self.ISIN_COL]

        if not instrument_name:
            return None

        # Ignore subtotal and section rows
        if any(
            keyword in instrument_name.lower()
            for keyword in self.IGNORE_KEYWORDS
        ):
            return None

        # Equity holdings only
        if not isin.startswith("INE"):
            return None

        return {
            "scheme_code": sheet_name,
            "scheme_name": scheme_name,
            "isin": isin,
            "stock_name": instrument_name,
            "industry": values[self.INDUSTRY_COL],
            "quantity": values[self.QUANTITY_COL],
            "market_value": values[self.MARKET_VALUE_COL],
            "amc_name": amc_name,
        }
    ```
````
