from app.browser.playwright_factory import PlaywrightFactory
from database.test_connections import DatabaseConnection
from app.browser.browser_manager import BrowserManager

# from database.test_connections import DBConnection
from app.downloaders.sbi_downloader import SBIDownloader
from app.core.factory.downloader_factory import DownloaderFactory
from database.DB.schemas.schemas import TableCreation

from app.config.constant import AMC


def main():

    playwright = None
    browser = None

    try:

        playwright, browser = PlaywrightFactory.launch_browser(headless=False)

        manager = BrowserManager(browser)

        DatabaseConnection.check_connection()
        TableCreation.create_tables()
        amcs = [
            # AMC.SBI,
            AMC.QUANT
        ]

        for amc in amcs:

            try:
                print(f"\n[INFO] Starting download for: {amc}")
                page = manager.create_page()

                downloader = DownloaderFactory.get_downloader(amc, page)

                file_path = downloader.download_latest_portfolio()

                print(f"[SUCCESS] {amc} Downloaded: {file_path}")

            except Exception as e:

                print(f"[ERROR] Failed for {amc}: {e}")

    except Exception as e:

        print(f"[MAIN ERROR] {e}")

    # finally:

    # if browser:
    # browser.close()

    # if playwright:
    # playwright.stop()


if __name__ == "__main__":
    main()
