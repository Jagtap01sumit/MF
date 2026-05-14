from playwright.sync_api import sync_playwright


class PlaywrightFactory:

    @staticmethod
    def launch_browser(headless=True):

        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=False
        )

        return playwright, browser