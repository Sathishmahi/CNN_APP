from collections import namedtuple


DataIngestionConfig = namedtuple(
    "DataIngestionConfig", ["root_dir", "source_URL", "local_data_file", "unzip_dir"]
)


BaseModelConfig = namedtuple(
    "BaseModelConfig", ["root_dir", 
    "base_model_path",
     "updated_model_path",
     "params_img_size",
     "params_augmentation",
     "params_learning_rate",
     "params_include_top",
     "params_weights",
     "params_classes",
     "params_epochs",
     "params_batch_size"

     ]
)



CallBacksConfig = namedtuple(
    "CallBacksConfig",[
        "root_dir",
        "tensorboard_log_dir",
        "checkpoint_model_path"
    ]
    )



TrainingConfig=namedtuple("TrainingConfig",
[
    "root_dir",
    "trained_model_path",
    "data_file_path",
    "updated_model_path",
    "image_size",
    "epochs",
    "is_augmented"
]
)