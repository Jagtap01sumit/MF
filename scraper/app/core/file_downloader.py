import os


class DownloadManager:

    DOWNLOAD_FOLDER = "app/downloads"

    def save_download(
        self,
        download
    ):

        os.makedirs(
            self.DOWNLOAD_FOLDER,
            exist_ok=True
        )

        file_path = os.path.join(
            self.DOWNLOAD_FOLDER,
            download.suggested_filename
        )

        download.save_as(file_path)

        return file_path