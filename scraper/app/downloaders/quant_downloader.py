from app.core.base_downloader import BaseDownloader

from app.core.page_actions import PageActions

from app.core.file_downloader import DownloadManager
from app.extractors.quant_extractor import QUANTExcelExtractor
from app.exceptions.exception import (
    FileNotFoundException,
    DownloadException
)

from app.scrapers.quant.quant_config import QUANTConfig


class QuantDownloader(
    BaseDownloader,
    DownloadManager
):

    def __init__(self, page):

        self.page = page

        self.actions = PageActions(page)

    def open_monthly_portfolio(self):

        try:

            portfolio_dropdown = (
                self.actions.get_locator(
                    QUANTConfig.MONTHLY_PORTFOLIO_XPATH
                )
            )

            portfolio_dropdown.click()

        except Exception as e:

            print(
                f"[ERROR] Failed to open monthly portfolio: {e}"
            )

            raise DownloadException(
                "Unable to open monthly portfolio section."
            )

    def open_latest_year(self):

        try:

            year_buttons = (
                self.actions.get_locator(
                    QUANTConfig.YEAR_XPATH
                )
            )

            latest_year = year_buttons

            latest_year.click()

        except Exception as e:

            print(
                f"[ERROR] Failed to open latest year: {e}"
            )

            raise DownloadException(
                "Unable to open latest year."
            )


    def download_file(self):

        try:

            download_button = (
                self.actions.get_locator(
                    QUANTConfig.MONTH_XPATH
                )
            )

            with self.page.expect_download() as d:

                download_button.click()

            download = d.value
            
            filepath = self.save_download(download)
            return filepath

        except Exception as e:

            print(
                f"[ERROR] Failed to download file: {e}"
            )

            raise DownloadException(
                "Unable to download latest portfolio file."
            )

    def download_latest_portfolio(self):

        try:

            self.actions.navigate(
                QUANTConfig.URL
            )

            self.actions.wait(3000)

            self.open_monthly_portfolio()

            self.actions.wait(3000)

            self.open_latest_year()

            self.actions.wait(2000)

            # self.open_latest_month()

            self.actions.wait(2000)

            filepath =  self.download_file()
            extractor = QUANTExcelExtractor()

            df = extractor.extract(filepath)
            
            print(df);
            # normalizer = PortfolioNormalizer()

            # normalized_df = normalizer.normalize(df)

            # print(normalized_df.head())
            return filepath;

        except Exception as e:

            print(
                f"[ERROR] Quant download flow failed: {e}"
            )

            raise DownloadException(
                "Quant portfolio download process failed."
            )