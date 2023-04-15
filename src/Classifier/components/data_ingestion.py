import os
from urllib import request as req
from zipfile import ZipFile as zip
from Classifier.config import Configuration
from Classifier.utils import create_directories
from Classifier import logger
from Classifier.utils import get_size
from tqdm import tqdm
from pathlib import Path


class DataIngestion:
    def __init__(self, Config: Configuration = Configuration()):
        self.data_injectioin_config = Config.data_ingestion_config

    def download_data(self):
        logger.info(f"try to download file ...")
        download_url = self.data_injectioin_config.source_URL
        local_data_file = self.data_injectioin_config.local_data_file
        folder, _ = local_data_dir = os.path.split(local_data_file)
        create_directories([folder], True)
        if not os.path.exists(path=local_data_file):
            logger.info(f"start download file ")
            req.urlretrieve(url=download_url, filename=local_data_file)
            logger.info(f"finish download file path is {local_data_file}")
        else:
            logger.info(f" file already exist - existing file path {local_data_file}")
            logger.info(
                f" file already exist - file size is  {get_size(Path(local_data_file))}"
            )

    def _extract_helper(self, path: str, zip_file_names: list, zf):
        for file_name in tqdm(zip_file_names):
            zf.extract(file_name, path=path)
            over_all_path = Path(os.path.join(path, file_name))
            if get_size(over_all_path) == 0:
                logger.info(f"remove file  file path is {over_all_path} ")
                os.remove(path)

    def extract_data(self):
        logger.info(f"unzip started...")
        unzip_dir = self.data_injectioin_config.unzip_dir
        create_directories(path_to_directories=[unzip_dir])
        local_data_file = self.data_injectioin_config.local_data_file
        with zip(local_data_file) as zf:
            all_content_name_list = zf.namelist()
            all_filters_name = [
                name
                for name in all_content_name_list
                if name.endswith(".jpg") and ("Dog" in name or "Cat" in name)
            ]
            self._extract_helper(path=unzip_dir, zip_file_names=all_filters_name, zf=zf)
        logger.info(f"finish unzip")
