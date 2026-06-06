from app.config.constant import AMC

from app.downloaders.sbi_downloader import SBIDownloader
from app.downloaders.quant_downloader import QuantDownloader


from app.downloaders.ppfas_downloader import PPFASDownloader


class DownloaderFactory:

    @staticmethod
    def get_downloader(amc_name, page):

        if amc_name == AMC.SBI:
            return SBIDownloader(page)

        elif amc_name == AMC.QUANT:
            return QuantDownloader(page)
        
        elif amc_name == AMC.PPFAS:
            return PPFASDownloader(page)

        raise ValueError(f"Unsupported AMC: {amc_name}")
