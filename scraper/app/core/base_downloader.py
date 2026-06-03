from abc import ABC, abstractmethod


class BaseDownloader(ABC):

    @abstractmethod
    def download_latest_portfolio(self):
        pass
