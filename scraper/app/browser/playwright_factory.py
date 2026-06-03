from playwright.sync_api import sync_playwright


class PlaywrightFactory:

    @staticmethod
    def launch_browser(headless):

        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=headless)

        return playwright, browser
