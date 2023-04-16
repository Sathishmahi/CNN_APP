from Classifier.config import Configuration
from pathlib import Path
import os
from PIL import Image
import tensorflow as tf
import numpy as np
import matplotlib.image as mpimg

class Validation:
    def __init__(self, config: Configuration=Configuration()):
        self.eval_config = config.eval_config

    def load_trained_model(self,model_path:Path)->tf.keras.Model:
        return tf.keras.models.load_model(model_path)

    def _get_data(self,data_path:Path,image_size:list)->list:
        img_li,original_out,predicted_out=[],[],[]
        for sub_dir in os.listdir(data_path):
         
            for img in os.listdir(os.path.join(data_path,sub_dir)):
                file_path=os.path.join(data_path,sub_dir,img)
                image = Image.open(file_path)
                new_image = image.resize(tuple(image_size))
                img_li.append(np.array(new_image))
                original_out.append(sub_dir)
        return np.array(img_li),list(map(lambda x: 0 if x=='cat' else 1,original_out))

    def predict(self):
        trained_model_path=self.eval_config.trained_model_path
        eval_data_path=self.eval_config.eval_data_path
        image_size=self.eval_config.image_size
        trained_model=self.load_trained_model(model_path=trained_model_path)

        img_arr,y_true=self._get_data(data_path=eval_data_path,image_size=image_size)
        print(img_arr.shape)
        y_pre=trained_model.predict(img_arr)
        y_pre_arg=np.argmax(y_pre,axis=-1)
        m = tf.keras.metrics.Accuracy()
        m.update_state(y_true,y_pre_arg)
        return m.result().numpy()

    # def write_json(self):