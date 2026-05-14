import os

from app.core.base_downloader import BaseDownloader


class SBIDownloader(BaseDownloader):

    SBI_URL = "https://www.sbimf.com/portfolios"

    def __init__(self, page):
        self.page = page

    def download_latest_portfolio(self):

        self.page.goto(self.SBI_URL)

        self.page.wait_for_timeout(5000)

        download_buttons = self.page.locator("(//td[contains(normalize-space(),'All Schemes Monthly Portfolio')])[1]/../td[4]")

        count = download_buttons.count()

        for i in range(count):

            element = download_buttons.nth(i)

            text = element.inner_text()

           

            with self.page.expect_download() as download_info:
                element.click()

            download = download_info.value

            save_path = os.path.join(
                    "app/downloads",
                    download.suggested_filename
                )

            download.save_as(save_path)

            print(f"Downloaded: {save_path}")

            return save_path

        raise Exception("No XLSX file found")