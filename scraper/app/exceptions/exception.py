class ScraperException(Exception):

    def __init__(
        self,
        message="Scraper exception occurred"
    ):

        self.message = message

        super().__init__(self.message)


class DownloadException(
    ScraperException
):
    pass


class FileNotFoundException(
    DownloadException
):
    pass


class DownloadTimeoutException(
    DownloadException
):
    pass

class BrowserException(
    ScraperException
):
    pass


class BrowserLaunchException(
    BrowserException
):
    pass

class ParserException(
    ScraperException
):
    pass


class InvalidExcelFormatException(
    ParserException
):
    pass


class SheetNotFoundException(
    ParserException
):
    pass


class ColumnNotFoundException(
    ParserException
):
    pass