from app.core.base_downloader import BaseDownloader

from app.core.page_actions import PageActions
from datetime import datetime
from app.core.common.file_downloader import DownloadManager
from app.normalizers.quant_normalizer import PortfolioNormalizer
from app.extractors.ppfas_extractor import PPFASExcelExtractor
from app.core.exceptions.exception import FileNotFoundException, DownloadException
from database.DB.procedures.portfolio_procedures import PortfolioProcessor
from app.core.common.report_date_extractor import ReportDateExtractor

# from database.DB.insert import insert_holdings
from app.scrapers.ppfas.ppfas_config import PPFASConfig
# from app.core.common.amc_name_extractor import extract_amc_name


class PPFASDownloader(BaseDownloader, DownloadManager):

    def __init__(self, page):

        self.page = page

        self.actions = PageActions(page)

    def open_monthly_portfolio(self):

        try:

            portfolio_sidebarlink = self.actions.get_locator(
                PPFASConfig.MONTHLY_PORTFOLIO_XPATH
            )

            portfolio_sidebarlink.click()

        except Exception as e:

            print(f"[ERROR] Failed to open monthly portfolio: {e}")

            raise DownloadException("Unable to open monthly portfolio section.")

    def open_latest_year(self):

        try:

            year_buttons = self.actions.get_locator(PPFASConfig.YEAR_XPATH)

            latest_year = year_buttons

            latest_year.click()

        except Exception as e:

            print(f"[ERROR] Failed to open latest year: {e}")

            raise DownloadException("Unable to open latest year.")

    def download_file(self):

        try:

            expanded_element = self.actions.get_locator(PPFASConfig.MONTH_XPATH)

            if expanded_element.is_visible():

                with self.page.expect_download() as d:

                    expanded_element.click();

                download = d.value

                filepath = self.save_download(download)
                return filepath
            else :
                print("Section not expanded, clicking collapsed section")

                collapse_element = self.actions.get_locator(PPFASConfig.COLLAPSE_XPATH);
                collapse_element.click(0)
                expanded_element = self.actions.get_locator(PPFASConfig.MONTH_XPATH)

                if expanded_element.is_visible():

                    with self.page.expect_download() as d:

                        expanded_element.click();

                    download = d.value

                    filepath = self.save_download(download)
                    return filepath
                

                print("Section expanded successfully")

        except Exception as e:

            print(f"[ERROR] Failed to download file: {e}")

            raise DownloadException("Unable to download latest portfolio file.")

    def download_latest_portfolio(self):

        try:

            self.actions.navigate(PPFASConfig.URL)

            self.actions.wait(3000)

            self.open_monthly_portfolio()

            self.actions.wait(3000)

            self.open_latest_year()

            self.actions.wait(2000)

            filepath = self.download_file()
            extractor = PPFASExcelExtractor()

            df = extractor.extract(filepath)

            print(df)
            print("before normalizer")
            print("name:" + df["scheme_name"].iloc[0])
            normalizer = PortfolioNormalizer()

            normalized_df = normalizer.normalize(df)
            date_extractor = ReportDateExtractor()

            report_month = date_extractor.extract_report_month(filepath)

            print(report_month)
            normalized_df["report_month"] = report_month
            print("after normalizer")

            print(normalized_df.head())
            print("database connection")
        
            processor = PortfolioProcessor()
          

            processor.process(normalized_df)

            return filepath

        except Exception as e:

            print(f"[ERROR] PPFAS download flow failed: {e}")

            raise DownloadException("PPFAS portfolio download process failed.")
