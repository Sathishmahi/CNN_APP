from Classifier import logger
from Classifier.entity import BaseModelConfig
from Classifier.config.configuration import Configuration
from pathlib import Path
import os
import tensorflow as tf




class PreapareBaseModel:
    def __init__(self,config=Configuration())->None:
        self.prepare_base_model_config=config.prepare_base_model_config

    def get_base_model(self):
        model=tf.keras.applications.vgg16.VGG16(
            input_shape=self.prepare_base_model_config.params_img_size,
            weights=self.prepare_base_model_config.params_weights,
            include_top=self.prepare_base_model_config.params_include_top
        )

        base_model_path=self.prepare_base_model_config.base_model_path
        self.save_model(base_model_path,model)
        return model


    @staticmethod
    def _prepare_full_model(model:tf.keras.Model, classes:int, freeze_all:bool, freeze_till:int, learning_rate:float):
        if freeze_all:
            model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(flatten_in)

        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        full_model.summary()
        return full_model

    def update_base_model(self):
        base_model=self.get_base_model()
        lr=self.prepare_base_model_config.params_learning_rate
        classes=self.prepare_base_model_config.params_classes
        freeze_all=True
        freeze_till=None
        full_model=self._prepare_full_model(base_model,classes=classes,freeze_all=freeze_all,
        freeze_till=freeze_till,learning_rate=lr)
        self.save_model( path=self.prepare_base_model_config.updated_model_path, model=full_model)
    @staticmethod
    def save_model(path:Path,model:tf.keras.Model):
        model.save(path)