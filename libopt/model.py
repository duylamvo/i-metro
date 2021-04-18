"""Models Definition."""
import os
import time
from tempfile import tempdir

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
# from tensorflow.keras import preprocessing

class MLOperators:
    """Machine Learning Operators.
    """
    def build(self, **kwargs):
        raise NotImplementedError

    def train(self, **kwargs):
        raise NotImplementedError

    def save(self, **kwargs):
        raise NotImplementedError

    def eval(self, **kwargs):
        raise NotImplementedError
    
class LinearModel(MLOperators):
    """Base Model: Linear Regression.
    """
    def __init__(self) -> None:
        super().__init__()
        self.model = self.build()
        self.metadata = dict()
        
        self.log("model_name", self.__class__.__name__)
        
    @staticmethod
    def build(**kwargs):
        normalizer = preprocessing.Normalization()
        model = tf.keras.Sequential([
            normalizer,
            layers.Dense(units=1)
        ])
        return model
    
    def train(self, train_x, train_y, **kwargs):
        optimizer = tf.optimizers.Adam(learning_rate=kwargs.get("learning_rate") or 0.1)
        loss = kwargs.get('loss') or 'mean_absolute_error'
        
        self.model.compile(optimizer=optimizer, loss=loss)
        history = self.model.fit(
            train_x, 
            train_y,
            epochs=kwargs.get("epochs") or 100,
            verbose=kwargs.get("verbose") or 0,
            validation_split=kwargs.get("validation_split") or 0.2
        )
        
        self.log("layers", "-".join([l.name for l in self.model.layers]))
        self.log("output_shape", "-".join([str(l.output_shape) for l in self.model.layers]))
        self.log("trained_on", int(time.time()))
        return history

    def save(self, dir_path='saved_model'):
        os.makedirs(dir_path, exist_ok=True)
        file_path = f"{dir_path}/{self.metadata['model_name']}-{int(time.time())}"
        self.model.save(file_path)
        
        self.log("saved_at", file_path)
        
    def eval(self, test_x, test_y, **kwargs):
        eval_result = self.model.evaluate(test_x, 
                                          test_y,
                                          verbose=kwargs.get("verbose") or 0,
        )

        self.log("evaluate_score", eval_result)
        self.log("evaluate_on", int(time.time()))
        return eval_result

    def log(self, k, v):
        self.metadata[k] = v

class DNNModel(LinearModel):
    def build(self, **kwargs):
        normalizer = preprocessing.Normalization()
        model = keras.Sequential([
            normalizer,
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)
        ])
        return model
