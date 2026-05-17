from app.core.base_downloader import BaseDownloader

from app.core.page_actions import PageActions
from datetime import datetime
from app.core.common.file_downloader import DownloadManager
from app.normalizers.quant_normalizer import PortfolioNormalizer
from app.extractors.quant_extractor import QUANTExcelExtractor
from app.exceptions.exception import FileNotFoundException, DownloadException
from database.DB.procedures.portfolio_procedures import PortfolioProcessor
from app.core.common.report_date_extractor import ReportDateExtractor
from database.DB.insert import insert_holdings
from app.scrapers.quant.quant_config import QUANTConfig
from app.core.common.amc_name_extractor import extract_amc_name


class QuantDownloader(BaseDownloader, DownloadManager):

    def __init__(self, page):

        self.page = page

        self.actions = PageActions(page)

    def open_monthly_portfolio(self):

        try:

            portfolio_dropdown = self.actions.get_locator(
                QUANTConfig.MONTHLY_PORTFOLIO_XPATH
            )

            portfolio_dropdown.click()

        except Exception as e:

            print(f"[ERROR] Failed to open monthly portfolio: {e}")

            raise DownloadException("Unable to open monthly portfolio section.")

    def open_latest_year(self):

        try:

            year_buttons = self.actions.get_locator(QUANTConfig.YEAR_XPATH)

            latest_year = year_buttons

            latest_year.click()

        except Exception as e:

            print(f"[ERROR] Failed to open latest year: {e}")

            raise DownloadException("Unable to open latest year.")

    def download_file(self):

        try:

            download_button = self.actions.get_locator(QUANTConfig.MONTH_XPATH)

            with self.page.expect_download() as d:

                download_button.click()

            download = d.value

            filepath = self.save_download(download)
            return filepath

        except Exception as e:

            print(f"[ERROR] Failed to download file: {e}")

            raise DownloadException("Unable to download latest portfolio file.")

    def download_latest_portfolio(self):

        try:

            self.actions.navigate(QUANTConfig.URL)

            self.actions.wait(3000)

            self.open_monthly_portfolio()

            self.actions.wait(3000)

            self.open_latest_year()

            self.actions.wait(2000)

            # self.open_latest_month()

            self.actions.wait(2000)

            filepath = self.download_file()
            extractor = QUANTExcelExtractor()

            df = extractor.extract(filepath)

            print(df)
            print("before normalizer")
            print("name:" + df["scheme_name"].iloc[0])
            normalizer = PortfolioNormalizer(
                scheme_name=df["scheme_name"],
                amc_name=df["amc_name"],
            )

            normalized_df = normalizer.normalize(df)
            date_extractor = ReportDateExtractor()

            report_month = date_extractor.extract_report_month(filepath)

            print(report_month)
            normalized_df["report_month"] = report_month
            print("after normalizer")

            print(normalized_df.head())
            print("database connection")
            # insert_holdings(normalized_df);
            processor = PortfolioProcessor()
            # amc_name = extract_amc_name(filepath)
            # normalized_df["amc_name"] = amc_name

            processor.process(normalized_df)

            return filepath

        except Exception as e:

            print(f"[ERROR] Quant download flow failed: {e}")

            raise DownloadException("Quant portfolio download process failed.")
