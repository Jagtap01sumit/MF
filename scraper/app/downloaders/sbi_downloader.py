from app.core.base_downloader import BaseDownloader

from app.core.page_actions import PageActions
from app.extractors.sbi_extractor import SBIExtractor
from app.core.common.file_downloader import DownloadManager
from app.core.exceptions.exception import FileNotFoundException, DownloadException

# from database.DB.insert import insert_holdings
from app.scrapers.sbi.sbi_config import SBIConfig
from app.core.common.report_date_extractor import ReportDateExtractor
from database.DB.procedures.portfolio_procedures import PortfolioProcessor

# from app.core.common.report_date_extractor import ReportDateExtractor
# from app.normalizers.sbi_normalizer import PortfolioNormalizer
from app.normalizers.quant_normalizer import PortfolioNormalizer


class SBIDownloader(BaseDownloader, DownloadManager):

    def __init__(self, page):

        self.page = page

        self.actions = PageActions(page)

    def get_latest_portfolio_button(self):

        try:

            xpath = SBIConfig.PORTFOLIO_ROW_XPATH + SBIConfig.XLSX_BUTTON_RELATIVE_XPATH

            button = self.actions.get_locator(xpath)

            return button

        except Exception as e:

            print(f"[ERROR] Failed to get latest portfolio button: {e}")

            raise FileNotFoundException(
                "Unable to locate SBI portfolio download button."
            )

    def download_latest_portfolio(self, manual_file_path=None):
        try:
            if manual_file_path:
                file_path = manual_file_path
            else:
                self.actions.navigate(SBIConfig.URL)
                self.actions.wait(5000)

                button = self.get_latest_portfolio_button()

                with self.page.expect_download() as d:
                    button.click()

                download = d.value
                file_path = self.save_download(download)

            print(f"Using file: {file_path}")

            extractor = SBIExtractor()
            df = extractor.extract(file_path)

            normalizer = PortfolioNormalizer()
            normalized_df = normalizer.normalize(df)

            date_extractor = ReportDateExtractor()
            report_month = date_extractor.extract_report_month(file_path)
            normalized_df["report_month"] = report_month

            processor = PortfolioProcessor()
            processor.process(normalized_df)

            return file_path

        except Exception as e:
            raise DownloadException(f"Failed: {e}")