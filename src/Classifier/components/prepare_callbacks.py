from Classifier.entity import CallBacksConfig
from pathlib import Path
from Classifier.config import Configuration
import tensorflow as tf
import time
import os

class PrepareCallback:
    def __init__(self, config=Configuration()):
        self.prepare_callbacks_config = config.prepare_call_backs_config

    @property
    def _create_tb_callbacks(self):
        time_stamp=time.strftime('%Y_%m_%d_%H_%M_%S')
        tb_runnig_log_dir=self.prepare_callbacks_config.tensorboard_log_dir
        final_log_dir=os.path.join(tb_runnig_log_dir,f"tb_logs_at_{time_stamp}")
        return tf.keras.callbacks.TensorBoard(log_dir=final_log_dir)
    @property
    def _create_chkt_callbacks(self):
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=self.prepare_callbacks_config.checkpoint_model_path,
            svae_best_only=True
        )
    def get_tb_chkt_call_backs(self):
        return [
            self._create_tb_callbacks,
            self._create_chkt_callbacks
        ]
