from app.config.constant import AMC

from app.downloaders.sbi_downloader import (
    SBIDownloader
)


from app.downloaders.quant_downloader import QuantDownloader
# from app.downloaders.hdfc_downloader import HDFCDownloader


class DownloaderFactory:

    @staticmethod
    def get_downloader(
        amc_name,
        page
    ):

        if amc_name == AMC.SBI:
            return SBIDownloader(page)

        elif amc_name == AMC.QUANT:
            return QuantDownloader(page)

        # elif amc_name == AMC.HDFC:
        #     return HDFCDownloader(page)

        raise ValueError(
            f"Unsupported AMC: {amc_name}"
        )