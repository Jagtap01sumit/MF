from app.browser.playwright_factory import (
    PlaywrightFactory
)

from app.browser.browser_manager import (
    BrowserManager
)

from app.downloaders.sbi_downloader import (
    SBIDownloader
)


def main():

    playwright, browser = (
        PlaywrightFactory.launch_browser()
    )

    manager = BrowserManager(browser)

    page = manager.create_page()

    downloader = SBIDownloader(page)

    file_path = downloader.download_latest_portfolio()

    print(file_path)

    browser.close()

    playwright.stop()


if __name__ == "__main__":
    main()