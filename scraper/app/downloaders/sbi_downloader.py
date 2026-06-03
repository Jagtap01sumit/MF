from app.core.base_downloader import BaseDownloader

from app.core.page_actions import PageActions
from app.extractors.sbi_extractor import SBIExtractor
from app.core.common.file_downloader import DownloadManager
from app.exceptions.exception import FileNotFoundException, DownloadException
from database.DB.insert import insert_holdings
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

    def download_latest_portfolio(self):

        try:

            self.actions.navigate(SBIConfig.URL)

            self.actions.wait(5000)

            button = self.get_latest_portfolio_button()

            print(f"Button Locator: {button}")

            with self.page.expect_download() as d:

                button.click()

            download = d.value

            file_path = self.save_download(download)

            print(f"Downloaded: {file_path}")
            extractor = SBIExtractor()
            df = extractor.extract(file_path)
            print(df)
            print("before col")
            # print(df.sheet_names);
            print("after col")
            normalizer = PortfolioNormalizer()
            normalized_df = normalizer.normalize(df)
            date_extractor = ReportDateExtractor()

            report_month = date_extractor.extract_report_month(file_path)

            print(report_month)
            normalized_df["report_month"] = report_month
            print("after normalizer")

            print(normalized_df.head())

            print(normalized_df)
            date_extractor = ReportDateExtractor()

            report_month = date_extractor.extract_report_month(file_path)
            processor = PortfolioProcessor()
            processor.process(normalized_df)

            return file_path

        except FileNotFoundException as e:

            print(f"[FILE NOT FOUND ERROR] {e}")

            raise

        except Exception as e:

            print(f"[DOWNLOAD ERROR] {e}")

            raise DownloadException(f"Failed to download SBI portfolio file: {e}")
