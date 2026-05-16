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