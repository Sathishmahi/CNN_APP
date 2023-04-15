from Classifier.constant import *
from Classifier.entity import BaseModelConfig,CallBacksConfig,DataIngestionConfig,TrainingConfig
from Classifier.utils import read_yaml,create_directories
from pathlib import Path
import os

class Configuration:
    def __init__(
        self, config_file_path=CONFIG_FILE_PATH, params_file_path=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(path_to_yaml=config_file_path)
        self.params = read_yaml(path_to_yaml=params_file_path)

        self.data_ingestion_config = self.get_data_ingestion_config()
        self.prepare_base_model_config = self.get_prepare_base_model_config()
        self.prepare_call_backs_config = self.get_prepare_call_backs()
        self.training_config=self.get_training_config()

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        data_injection_config_attr = self.config.get("data_ingestion")
        data_injection_config = DataIngestionConfig(
            root_dir=Path(data_injection_config_attr.get("root_dir")),
            source_URL=data_injection_config_attr.get("source_URL"),
            local_data_file=Path(data_injection_config_attr.get("local_data_file")),
            unzip_dir=Path(data_injection_config_attr.get("unzip_dir")),
        )

        # create_directories([
        #     root_dir,
        #     local_data_file,
        #     unzip_dir
        # ])
        return data_injection_config


    def get_prepare_base_model_config(self)->BaseModelConfig:

        prepare_base_model_attr= self.config.get("prepare_base_model")

        prepare_base_model_config= BaseModelConfig(
        root_dir=Path(prepare_base_model_attr.get("root_dir")), 
        base_model_path= Path(prepare_base_model_attr.get("base_model_path")) , 
        updated_model_path=Path(prepare_base_model_attr.get("updated_model_path")),
        
        params_img_size=self.params.get("IAMGE_SIZE"),
        params_augmentation=self.params.get("AUGMENTATION"),
        params_learning_rate=self.params.get("LEARNING_RATE"),
        params_include_top=self.params.get("INCLUDE_TOP"),
        params_weights=self.params.get("WEIGHTS"),
        params_classes=self.params.get("CLASSES"),
        params_epochs=self.params.get("EPOCHS"),
        params_batch_size=self.params.get("BATCH_SIZE"),
     )
           
        # create_directories([
        #     root_dir,
        #     os.path.dirname(updated_model_path),
        #     os.path.dirname(base_model_path)
        # ])
        return prepare_base_model_config

    def get_prepare_call_backs(self)->CallBacksConfig:
        prepare_call_backs_attr = self.config.get("prepare_callbacks")
        root_dir= Path(prepare_call_backs_attr.get("root_dir"))
        tensorboard_log_dir=Path(prepare_call_backs_attr.get("tensorboard_log_dir"))
        checkpoint_model_path=Path(prepare_call_backs_attr.get("checkpoint_model_path"))

        prepare_call_backs_config = CallBacksConfig(
            root_dir=root_dir,
            tensorboard_log_dir=tensorboard_log_dir,
            checkpoint_model_path=checkpoint_model_path,
        )

        create_directories([
            root_dir,
            tensorboard_log_dir,
            os.path.dirname(checkpoint_model_path)
        ])

        return prepare_call_backs_config


    def get_training_config(self)->TrainingConfig:

        params=self.params

        data_file_path=os.path.join(self.data_ingestion_config.unzip_dir,"PetImages")
        updated_model_path=self.prepare_base_model_config.updated_model_path
        image_size=params.get("IAMGE_SIZE")
        epochs=params.get("EPOCHS")
        is_augmented=params.get("AUGMENTATION")

        print(self.config.keys())

        training_config_attr=self.config.get("training")
        root_dir=Path(training_config_attr.get("root_dir"))
        trained_model_path=Path(training_config_attr.get("trained_model_path"))


        return TrainingConfig(root_dir, 
        trained_model_path, 
        data_file_path, updated_model_path, image_size, epochs, is_augmented)