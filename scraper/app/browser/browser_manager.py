class BrowserManager:

    def __init__(self, browser):
        self.browser = browser

    def create_page(self):

        context = self.browser.new_context(
            accept_downloads=True
        )

        page = context.new_page()

        return page