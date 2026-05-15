from app.core.base_downloader import BaseDownloader

from app.core.page_actions import PageActions
from app.extractors.sbi_extractor import SBIExtractor
from app.core.file_downloader import DownloadManager
from app.exceptions.exception import (
    FileNotFoundException,
    DownloadException
)

from app.scrapers.sbi.sbi_config import SBIConfig


class SBIDownloader(
    BaseDownloader,
    DownloadManager
):

    def __init__(self, page):

        self.page = page

        self.actions = PageActions(page)

    def get_latest_portfolio_button(self):

        try:

            xpath = (
                SBIConfig.PORTFOLIO_ROW_XPATH +
                SBIConfig.XLSX_BUTTON_RELATIVE_XPATH
            )

            button = self.actions.get_locator(xpath)

            return button

        except Exception as e:

            print(
                f"[ERROR] Failed to get latest portfolio button: {e}"
            )

            raise FileNotFoundException(
                "Unable to locate SBI portfolio download button."
            )

    def download_latest_portfolio(self):

        try:

            self.actions.navigate(
                SBIConfig.URL
            )

            self.actions.wait(5000)

            button = (
                self.get_latest_portfolio_button()
            )

            print(
                f"Button Locator: {button}"
            )

            with self.page.expect_download() as d:

                button.click()

            download = d.value

            file_path = self.save_download(
                download
            )

            print(
                f"Downloaded: {file_path}"
            )
            extractor = SBIExtractor()

            df = extractor.extract(file_path)
            print("sumit df"+df);
            # normalizer = PortfolioNormalizer()

            # normalized_df = normalizer.normalize(df)

            # print(normalized_df.head())
            return file_path

        except FileNotFoundException as e:

            print(
                f"[FILE NOT FOUND ERROR] {e}"
            )

            raise

        except Exception as e:

            print(
                f"[DOWNLOAD ERROR] {e}"
            )

            raise DownloadException(
                f"Failed to download SBI portfolio file: {e}"
            )