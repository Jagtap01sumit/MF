import os


class FileDownloader:

    def save_download(
        self,
        download,
        folder
    ):

        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(
            folder,
            download.suggested_filename
        )

        download.save_as(file_path)

        return file_path