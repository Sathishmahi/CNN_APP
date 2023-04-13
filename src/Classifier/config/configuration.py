from Classifier.constant import *
from Classifier.entity.config_entity import DataIngestionConfig
from Classifier.utils import read_yaml


class Configuration:
    def __init__(
        self, config_file_path=CONFIG_FILE_PATH, params_file_path=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(path_to_yaml=config_file_path)
        self.params = read_yaml(path_to_yaml=params_file_path)

        self.data_ingestion_config = self.get_data_ingestion_config()

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        data_injection_config_attr = self.config.get("data_ingestion")
        data_injection_config = DataIngestionConfig(
            root_dir=data_injection_config_attr.get("root_dir"),
            source_URL=data_injection_config_attr.get("source_URL"),
            local_data_file=data_injection_config_attr.get("local_data_file"),
            unzip_dir=data_injection_config_attr.get("unzip_dir"),
        )

        return data_injection_config
