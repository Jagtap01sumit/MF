class PageActions:

    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def wait(self, milliseconds=3000):
        self.page.wait_for_timeout(milliseconds)

    def get_locator(self, xpath):
        return self.page.locator(xpath)

    def click(self, locator):
        locator.click()

    def get_text(self, locator):
        return locator.inner_text()