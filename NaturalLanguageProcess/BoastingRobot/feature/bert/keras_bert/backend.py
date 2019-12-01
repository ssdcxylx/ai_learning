# -*- coding: utf-8 -*-
# @time       : 15/11/2019 10:38 上午
# @author     : ssdcxy
# @email      : 18379190862@163.com
# @file       : backend
# @description: 


import os
from distutils.util import strtobool

__all__ = [
    'keras', 'utils', 'activations', 'applications', 'backend', 'datasets', 'engine',
    'layers', 'preprocessing', 'wrappers', 'callbacks', 'constraints', 'initializers',
    'metrics', 'models', 'losses', 'optimizers', 'regularizers', 'TF_KERAS',
]

TF_KERAS = strtobool(os.environ.get('TF_KERAS', '0'))

if TF_KERAS:
    from tensorflow.python import keras
else:
    import keras

utils = keras.utils
activations = keras.activations
applications = keras.applications
backend = keras.backend
datasets = keras.datasets
engine = keras.engine
layers = keras.layers
preprocessing = keras.preprocessing
wrappers = keras.wrappers
callbacks = keras.callbacks
constraints = keras.constraints
initializers = keras.initializers
metrics = keras.metrics
models = keras.models
losses = keras.losses
optimizers = keras.optimizers
regularizers = keras.regularizers