# -*- coding: utf-8 -*-
# @Time    : 2018-12-25 09:51
# @Author  : ssdcxy
# @Email   : 18379190862@163.com
# @File    : DeppLearning.py

import numpy as np
import os
import tensorflow as tf
from functools import partial
from tensorflow.examples.tutorials.mnist import input_data
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
import time


def reset_graph(seed=42):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)


import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

PROJECT_ROOT_DIR = "."
CHAPTER_ID = "deep"


def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID, fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format="png", dpi=300)


reset_graph()


def leaky_relu(z, alpha, name=None):
    return tf.maximum(alpha * z, z, name=name)


def elu(z, alpha=1):
    return np.where(z < 0, alpha * (np.exp(z) - 1), z)


def selu(z,
         scale=1.0507009873554804934193349852946,
         alpha=1.6732632423543772848170429916717):
    return scale * elu(z, alpha)


# np.random.seed(42)
# Z = np.random.normal(size=(500, 100))
# for layer in range(100):
#     W = np.random.normal(size=(100, 100), scale=np.sqrt(1/100))
#     Z = selu(np.dot(Z, W))
#     means = np.mean(Z, axis=1)
#     stds = np.std(Z, axis=1)
#     if layer % 10 == 0:
#         print("Layer {}:{:.2f} < mean < {:.2f}, {:.2f} < std_deviation < {:.2f}".format(
#             layer, means.min(), means.max(), stds.min(), stds.max()
#         ))


# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 100
# n_outputs = 10
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")

# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.leaky_relu, name="hidden1")
#     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.leaky_relu, name="hidden2")
#     logits = tf.layers.dense(hidden2, n_outputs, name="outputs")
#
# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.elu, name="hidden1")
#     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.elu, name="hidden2")
#     logits = tf.layers.dense(hidden2, n_outputs, name="outputs")

# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.selu, name="hidden1")
#     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.selu, name="hidden2")
#     logits = tf.layers.dense(hidden2, n_outputs, name="outputs")
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
# learning_rate = 0.01
#
# with tf.name_scope("train"):
#     optimizer = tf.train.GradientDescentOptimizer(learning_rate)
#     training_op = optimizer.minimize(loss)
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_train = X_train.astype(np.float32).reshape(-1, 28 * 28) / 255.0
X_test = X_test.astype(np.float32).reshape(-1, 28 * 28) / 255.0
y_train = y_train.astype(np.int32)
y_test = y_test.astype(np.int32)
X_valid, X_train = X_train[:5000], X_train[5000:]
y_valid, y_train = y_train[:5000], y_train[5000:]
mnist = input_data.read_data_sets("tmp/img")


def shuffle_batch(X, y, batch_size):
    rnd_idx = np.random.permutation(len(X))
    n_batches = len(X) // batch_size
    for batch_idx in np.array_split(rnd_idx, n_batches):
        X_batch, y_batch = X[batch_idx], y[batch_idx]
        yield X_batch, y_batch


# n_epochs = 40
# batch_size = 50
#
# means = X_train.mean(axis=0, keepdims=True)
# stds = X_train.std(axis=0, keepdims=True) + 1e-10
# X_val_scaled = (X_valid - means) / stds
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             X_batch_scaled = (X_batch - means) / stds
#             sess.run(training_op, feed_dict={X: X_batch_scaled, y: y_batch})
#         if epoch % 5 == 0:
#             acc_batch = accuracy.eval(feed_dict={X: X_batch_scaled, y: y_batch})
#             acc_valid = accuracy.eval(feed_dict={X: X_val_scaled, y: y_valid})
#             print(epoch, "Batch accuracy:", acc_batch, "Validation accuracy:", acc_valid)
#     save_path = saver.save(sess, "./my_model_final.ckpt")

# reset_graph()

# 批量正则化 Batch Normalization
# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 100
# n_outputs = 10
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# training = tf.placeholder_with_default(False, shape=(), name="training")

# hidden1 = tf.layers.dense(X, n_hidden1, name="hidden1")
# bn1 = tf.layers.batch_normalization(hidden1, training=training, momentum=0.9)
# bn1_act = tf.nn.elu(bn1)
#
# hidden2 = tf.layers.dense(bn1_act, n_hidden2, name="hidden2")
# bn2 = tf.layers.batch_normalization(hidden2, training=training, momentum=0.9)
# bnn2_act = tf.nn.elu(bn2)
#
# logits_before_bn = tf.layers.dense(bnn2_act, n_outputs, name="outputs")
# logits = tf.layers.batch_normalization(logits_before_bn, training=training,
#                                        momentum=0.9)
#
# my_batch_norm_layer = partial(tf.layers.batch_normalization, training=training,
#                               momentum=0.9)
#
# hidden1 = tf.layers.dense(X, n_hidden1, name="hidden1")
# bn1 = my_batch_norm_layer(hidden1)
# bn1_act = tf.nn.elu(bn1)
# hidden2 = tf.layers.dense(bn1_act, n_hidden2, name="hidden2")
# bn2 = my_batch_norm_layer(hidden2)
# bn2_act = tf.nn.elu(hidden2)
# logits_before_bn = tf.layers.dense(bn2_act, n_outputs, name="outputs")
# logits = my_batch_norm_layer(logits_before_bn)

# reset_graph()
#
# batch_norm_momentum = 0.9
# learning_rate = 0.01
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
# training = tf.placeholder_with_default(False, shape=(), name="training")
#
# with tf.name_scope("dnn"):
#     he_init = tf.variance_scaling_initializer()
#
#     my_batch_norm_layer = partial(
#         tf.layers.batch_normalization,
#         training=training,
#         momentum=batch_norm_momentum
#     )
#     my_dense_layer = partial(
#         tf.layers.dense,
#         kernel_initializer=he_init
#     )
#     hidden1 = my_dense_layer(X, n_hidden1, name="hidden1")
#     bn1 = tf.nn.elu(my_batch_norm_layer(hidden1))
#     hidden2 = my_dense_layer(bn1, n_hidden2, name="hidden2")
#     bn2 = tf.nn.elu(my_batch_norm_layer(hidden2))
#     logits_before_bn = my_dense_layer(bn2, n_outputs, name="outputs")
#     logits = my_batch_norm_layer(logits_before_bn)
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
# with tf.name_scope("train"):
#     # 梯度下降
#     # optimizer = tf.train.GradientDescentOptimizer(learning_rate)
#     # 动量优化
#     # optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=0.9)
#     # Nesterov 加速梯度
#     # optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=0.9, use_nesterov=True)
#     # AdaGrad
#     # optimizer = tf.train.AdagradOptimizer(learning_rate)
#     # RMSProp
#     # optimizer = tf.train.RMSPropOptimizer(learning_rate, momentum=0.9, decay=0.9, epsilon=1e-10)
#     # Adam
#     optimizer = tf.train.AdamOptimizer(learning_rate)
#     extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
#     with tf.control_dependencies(extra_update_ops):
#         training_op = optimizer.minimize(loss)
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# n_epochs = 20
# batch_size = 200
#
# # extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             sess.run(training_op, feed_dict={training: True, X: X_batch, y: y_batch})
#             # sess.run([training_op, extra_update_ops], feed_dict={training: True, X: X_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
#         print(epoch, "Validation accuracy", accuracy_val)
#     save_path = saver.save(sess, "./my_model_final.ckpt")
#
# print([v.name for v in tf.trainable_variables()])
# print([v.name for v in tf.global_variables()])

# reset_graph()
#
# # 梯度裁剪
# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 50
# n_hidden3 = 50
# n_hidden4 = 50
# n_hidden5 = 50
# n_outputs = 10
#
# learning_rate = 0.01
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
#
# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.relu, name="hidden1")
#     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.relu, name="hidden2")
#     hidden3 = tf.layers.dense(hidden2, n_hidden3, activation=tf.nn.relu, name="hidden3")
#     hidden4 = tf.layers.dense(hidden3, n_hidden4, activation=tf.nn.relu, name="hidden4")
#     hidden5 = tf.layers.dense(hidden4, n_hidden5, activation=tf.nn.relu, name="hidden5")
#     logits = tf.layers.dense(hidden5, n_outputs, name="outputs")
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
# # threshold = 1.0
# # optimizer = tf.train.GradientDescentOptimizer(learning_rate)
# # grads_and_vars = optimizer.compute_gradients(loss)
# # capped_gvs = [(tf.clip_by_value(grad, -threshold, threshold), var)
# #               for grad, var in grads_and_vars]
# # training_op = optimizer.apply_gradients(capped_gvs)
#
# # with tf.name_scope("train"):
# #     optimizer = tf.train.GradientDescentOptimizer(learning_rate)
# #     training_op = optimizer.minimize(loss)
#
# with tf.name_scope("train"):
#     optimizer = tf.train.GradientDescentOptimizer(learning_rate)
#     train_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
#                                    scope="hidden[345]|outputs")
#     training_op = optimizer.minimize(loss, var_list=train_vars)
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
# file_writer = tf.summary.FileWriter("logs", tf.get_default_graph())
#
# n_epochs = 20
# batch_size = 200
#
# reuse_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
#                                scope="hidden[123]")
# restore_saver = tf.train.Saver()
#
# with tf.Session() as sess:
#
#     init.run()
#     restore_saver.restore(sess, "./my_model_final.ckpt")
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
#         print(epoch, "Validation accuracy:", accuracy_val)
#     save_path = saver.save(sess, "./my_model_final.ckpt")

# reset_graph()
#
# saver = tf.train.import_meta_graph("./my_model_final.ckpt.meta")
#
# for op in tf.get_default_graph().get_operations():
#     print(op.name)
#
# X = tf.get_default_graph().get_tensor_by_name("X:0")
# y = tf.get_default_graph().get_tensor_by_name("y:0")
#
# accuracy = tf.get_default_graph().get_tensor_by_name("eval/accuracy:0")
# training_op = tf.get_default_graph().get_operation_by_name("GradientDescent")
#
# for op in(X, y, accuracy, training_op):
#     tf.add_to_collection("my_important_ops", op)
#
# X, y, accuracy, training_op = tf.get_collection("my_important_ops")
#
# n_epochs = 20
# batch_size = 200
#
# with tf.Session() as sess:
#     saver.restore(sess, "./my_model_final.ckpt")
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
#         print(epoch, "Validation accuracy:", accuracy_val)
#     save_path = saver.save(sess, "./my_new_model_final.ckpt")

# reset_graph()
#
# n_hidden4 = 20
# n_outputs = 10
#
# learning_rate = 0.01
# n_epochs = 20
# batch_size = 200
#
# saver = tf.train.import_meta_graph("./my_model_final.ckpt.meta")
#
# X = tf.get_default_graph().get_tensor_by_name("X:0")
# y = tf.get_default_graph().get_tensor_by_name("y:0")
#
# hidden3 = tf.get_default_graph().get_tensor_by_name("dnn/hidden3/Relu:0")
#
# new_hidden4 = tf.layers.dense(hidden3, n_hidden4, activation=tf.nn.relu, name="new_hidden4")
# new_logits = tf.layers.dense(new_hidden4, n_outputs, name="new_outputs")
#
# with tf.name_scope("new_loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=new_logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
# with tf.name_scope("new_eval"):
#     correct = tf.nn.in_top_k(new_logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# with tf.name_scope("new_train"):
#     optimizer = tf.train.GradientDescentOptimizer(learning_rate)
#     train_op = optimizer.minimize(loss)
#
# init = tf.global_variables_initializer()
# new_saver = tf.train.Saver()
#
# with tf.Session() as sess:
#     init.run()
#     saver.restore(sess, "./my_model_final.ckpt")
#
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             sess.run(train_op, feed_dict={X: X_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
#         print(epoch, "Validation accuray:", accuracy_val)
#     save_path = new_saver.save(sess, "./my_new_model_final.ckpt")

# reuse_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
#                                scope="hidden[123]")
# restore_saver = tf.train.Saver(reuse_vars)
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# with tf.Session() as sess:
#     init.run()
#     restore_saver.restore(sess, "./my_model_final.ckpt")
#
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
#         print(epoch, "Validation accuracy:", accuracy_val)
#     save_path = saver.save(sess, "./my_new_model_final.ckpt")

# reset_graph()
#
# n_inputs = 2
# n_hidden1 = 3
#
# original_w = [[1., 2., 3.], [4., 5., 6]]
# original_b = [7., 8., 9.]
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.relu, name="hidden1")
#
# # 构建模型
# with tf.variable_scope("", default_name="", reuse=True):
#     hidden1_weights = tf.get_variable("hidden1/kernel")
#     hidden1_biases = tf.get_variable("hidden1/bias")
#
# original_weights = tf.placeholder(tf.float32, shape=(n_inputs, n_hidden1))
# original_biases = tf.placeholder(tf.float32, shape=n_hidden1)
# assign_hidden1_weights = tf.assign(hidden1_weights, original_weights)
# assign_hidden2_bias = tf.assign(hidden1_biases, original_biases)
#
# init = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init)
#     sess.run(assign_hidden1_weights, feed_dict={original_weights: original_w})
#     sess.run(assign_hidden2_bias, feed_dict={original_biases: original_b})
#     # Train the model on your new task
#     print(hidden1.eval(feed_dict={X: [[10.0, 11.0]]}))
#
# print(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="hidden1"))
# print(tf.get_default_graph().get_tensor_by_name("hidden1/kernel:0"))
# print(tf.get_default_graph().get_tensor_by_name("hidden1/bias:0"))

#

# reset_graph()
#
# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 50
# n_hidden3 = 50
# n_hidden4 = 50
# n_hidden5 = 50
# n_outputs = 10
#
# learning_rate = 0.01
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
#
# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.relu, name="hidden1")
#     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.relu, name="hidden2")
#     hidden2_stop = tf.stop_gradient(hidden2)
#     hidden3 = tf.layers.dense(hidden2_stop, n_hidden3, activation=tf.nn.relu, name="hidden3")
#     hidden4 = tf.layers.dense(hidden3, n_hidden4, activation=tf.nn.relu, name="hidden4")
#     hidden5 = tf.layers.dense(hidden4, n_hidden5, activation=tf.nn.relu, name="hidden5")
#     logits = tf.layers.dense(hidden4, n_outputs, name="outputs")
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
#
# with tf.name_scope("train"):
#     optimizer = tf.train.GradientDescentOptimizer(learning_rate)
#     train_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
#                                    scope="hidden[345]|outputs")
#     training_op = optimizer.minimize(loss, var_list=train_vars)
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# n_epochs = 20
# batch_size = 200
#
# reuse_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
#                                scope="hidden[123]")
# restore_saver = tf.train.Saver()
#
# n_batches = len(X_train) // batch_size
#
# with tf.Session() as sess:
#
#     init.run()
#     restore_saver.restore(sess, "./my_model_final.ckpt")
#
#     h2_cache = sess.run(hidden2, feed_dict={X: X_train})
#     h2_cache_valid = sess.run(hidden2, feed_dict={X: X_valid})
#
#     for epoch in range(n_epochs):
#         shuffle_idx = np.random.permutation(len(X_train))
#         hidden2_batches = np.array_split(h2_cache[shuffle_idx], n_batches)
#         y_batches = np.array_split(y_train[shuffle_idx], n_batches)
#         for hidden2_batch, y_batch in zip(hidden2_batches, y_batches):
#             sess.run(training_op, feed_dict={hidden2: hidden2_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={hidden2: h2_cache_valid,
#                                                     y: y_valid})
#         print(epoch, "Validation accuracy:", accuracy_val)
#     save_path = saver.save(sess, "./my_model_final.ckpt")

# reset_graph()
#
# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 50
# n_outputs = 10
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
#
# scale = 0.001
#
# my_dense_layer = partial(
#     tf.layers.dense, activation=tf.nn.relu,
#     kernel_regularizer=tf.contrib.layers.l1_regularizer(scale)
# )
#
# with tf.name_scope("dnn"):
#     hidden1 = my_dense_layer(X, n_hidden1, name="hidden1")
#     hidden2 = my_dense_layer(hidden1, n_hidden2, name="hidden2")
#     logits = my_dense_layer(hidden2, n_outputs, activation=None, name="outputs")
#
# # with tf.name_scope("dnn"):
# #     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.relu, name="hidden1")
# #     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.relu, name="hidden2")
# #     logits = tf.layers.dense(hidden2, n_outputs, name="outputs")
#
# # with tf.name_scope("loss"):
# #     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
# #     loss = tf.reduce_mean(xentropy, name="loss")
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     base_loss = tf.reduce_mean(xentropy, name="avg_xentropy")
#     reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
#     loss = tf.add_n([base_loss] + reg_losses, name="loss")
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# with tf.name_scope("train"):
#     initial_learning_rate = 0.1
#     decay_steps = 10000
#     decay_rate = 1/10
#     global_step = tf.Variable(0, trainable=False, name="global_step")
#     learning_rate = tf.train.exponential_decay(initial_learning_rate, global_step,
#                                                decay_steps, decay_rate)
#     optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=0.9)
#     training_op = optimizer.minimize(loss, global_step=global_step)
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# # n_epochs = 5
# # batch_size = 50
#
# # with tf.Session() as sess:
# #     init.run()
# #     for epoch in range(n_epochs):
# #         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
# #             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
# #         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
# #         print(epoch, "Validation accuracy:", accuracy_val)
# #     save_path = saver.save(sess, "./my_model_final.ckpt")
#
# n_epochs = 20
# batch_size = 200
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for iteration in range(mnist.train.num_examples // batch_size):
#             X_batch, y_batch = mnist.train.next_batch(batch_size)
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         accuracy_val = accuracy.eval(feed_dict={X: mnist.test.images,
#                                                 y: mnist.test.labels})
#         print(epoch, "Test accuracy:", accuracy_val)
#     save_path = saver.save(sess, "./my_model_final.ckpt")

# reset_graph()
#
# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 50
# n_outputs = 10
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
#
# learning_rate = 0.01
#
# training = tf.placeholder_with_default(False, shape=(), name="training")
# dropout_rate = 0.2   # 1 - keep_prob
# X_drop = tf.layers.dropout(X, dropout_rate, training=training)
#
# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X_drop, n_hidden1, activation=tf.nn.relu, name="hidden1")
#     hidden1_drop = tf.layers.dropout(hidden1, dropout_rate, training=training)
#     hidden2 = tf.layers.dense(hidden1_drop, n_hidden2, activation=tf.nn.relu, name="hidden2")
#     hidden2_drop = tf.layers.dropout(hidden2, dropout_rate, training=training)
#     logits = tf.layers.dense(hidden2_drop, n_outputs, name="outputs")
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
# with tf.name_scope("train"):
#     optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=0.9)
#     training_op = optimizer.minimize(loss)
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# n_epochs = 20
# batch_size = 50
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch, training: True})
#         accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
#         print(epoch, "Validation accuracy:", accuracy_val)
#     save_path = saver.save(sess, "./my_model_final.ckpt")

# n_inputs = 28 * 28
# n_hidden1 = 300
# n_hidden2 = 50
# n_outputs = 10
#
# learning_rate = 0.01
# momentum = 0.9
#
#
# def max_norm_regularizer(threshold, axes=1, name="max_norm",
#                          collection="max_norm"):
#     def max_norm(weights):
#         clipped = tf.clip_by_norm(weights, clip_norm=threshold, axes=axes)
#         clip_weights = tf.assign(weights, clipped, name=name)
#         tf.add_to_collection(collection, clip_weights)
#         return None
#     return max_norm
#
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int64, shape=(None), name="y")
#
# max_norm_reg = max_norm_regularizer(threshold=1.0)
#
# with tf.name_scope("dnn"):
#     hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.relu, kernel_regularizer=max_norm_reg, name="hidden1")
#     hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.relu, kernel_regularizer=max_norm_reg, name="hidden2")
#     logits = tf.layers.dense(hidden2, n_outputs, name="outputs")
#
# with tf.name_scope("loss"):
#     xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#     loss = tf.reduce_mean(xentropy, name="loss")
#
# with tf.name_scope("train"):
#     optimizer = tf.train.MomentumOptimizer(learning_rate, momentum)
#     training_op = optimizer.minimize(loss)
#
# with tf.name_scope("eval"):
#     correct = tf.nn.in_top_k(logits, y, 1)
#     accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# # threshold = 1.0
# # weights = tf.get_default_graph().get_tensor_by_name("hidden1/kernel:0")
# # clipped_weights = tf.clip_by_norm(weights, clip_norm=threshold, axes=1)
# # clip_weights = tf.assign(weights, clipped_weights)
# #
# # weights2 = tf.get_default_graph().get_tensor_by_name("hidden2/kernel:0")
# # clipped_weights2 = tf.clip_by_norm(weights2, clip_norm=threshold, axes=1)
# # clip_weights2 = tf.assign(weights2, clipped_weights2)
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# clip_all_weights = tf.get_collection("max_norm")
#
# n_epochs = 20
# batch_size = 50
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for iteration in range(mnist.train.num_examples // batch_size):
#             X_batch, y_batch = mnist.train.next_batch(batch_size)
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#             sess.run(clip_all_weights)
#             # clip_weights.eval()
#             # clip_weights2.eval()
#         acc_test = accuracy.eval(feed_dict={X: mnist.test.images,
#                                             y: mnist.test.labels})
#         print(epoch, "Test accuracy:", acc_test)
#     save_path = saver.save(sess, "./my_model_final.ckpt")

# # he_init = tf.variance_scaling_initializer()
#
#
# def dnn(inputs, n_hidden_layers=5, n_nerurons=100, name=None,
#         activation=tf.nn.elu, initializer=he_init):
#     with tf.variable_scope(name, "dnn"):
#         for layer in range(n_hidden_layers):
#             inputs = tf.layers.dense(inputs, n_nerurons, activation=activation,
#                                      kernel_initializer=initializer, name="hidden%d"%(layer + 1))
#         return inputs
#

# n_inputs = 28 * 28
# n_outputs = 5
#
# reset_graph()
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
#
# dnn_outputs = dnn(X)
#
# logits = tf.layers.dense(dnn_outputs, n_outputs, kernel_initializer=he_init, name="logits")
# Y_proba = tf.nn.softmax(logits, name="Y_proba")
#
# learning_rate = 0.01
#
# xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
# loss = tf.reduce_mean(xentropy, name="loss")
#
# optimizer = tf.train.AdamOptimizer(learning_rate)
# training_op = optimizer.minimize(loss, name="training_op")
#
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()

X_train1 = X_train[y_train < 5]
y_train1 = y_train[y_train < 5]
X_valid1 = X_valid[y_valid < 5]
y_valid1 = y_valid[y_valid < 5]
X_test1 = X_test[y_test < 5]
y_test1 = y_test[y_test < 5]

# n_epochs = 1000
# batch_size = 20
#
# max_checks_without_progress = 20
# checks_without_progress = 0
# best_loss = np.infty
#
# with tf.Session() as sess:
#     init.run()
#
#     for epoch in range(n_epochs):
#         rnd_idx = np.random.permutation(len(X_train1))
#         for rnd_indices in np.array_split(rnd_idx, len(X_train1) // batch_size):
#             X_batch, y_batch = X_train1[rnd_indices], y_train1[rnd_indices]
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         loss_val, acc_val = sess.run([loss, accuracy], feed_dict={X: X_valid1, y: y_valid1})
#         if loss_val < best_loss:
#             save_path = saver.save(sess, "./my_mnist_model_0_to_4.ckpt")
#             best_loss = loss_val
#             checks_without_progress = 0
#         else:
#             checks_without_progress += 1
#             if checks_without_progress > max_checks_without_progress:
#                 print("Early stopping!")
#                 break
#         print("{}\tValidation loss: {:.6f}\t Best loss: {:.6f}\t Accuracy: {:.2f}%".format(
#             epoch, loss_val, best_loss, acc_val * 100
#         ))
#
# with tf.Session() as sess:
#     saver.restore(sess, "./my_mnist_model_0_to_4.ckpt")
#     acc_test = accuracy.eval(feed_dict={X: X_test1, y: y_test1})
#     print("Final test accuracy: {:.2f}%".format(acc_test * 100))

he_init = tf.variance_scaling_initializer()


class DNNClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, n_hidden_layers=5, n_neurons=100, optimizer_class=tf.train.AdamOptimizer,
                 learning_rate=0.01, batch_size=20, activation=tf.nn.elu, initializer=he_init,
                 batch_norm_momentum=None, dropout_rate=None, random_state=None):
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons = n_neurons
        self.optimizer_class = optimizer_class
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.activation = activation
        self.initializer = initializer
        self.batch_norm_momentum = batch_norm_momentum
        self.dropout_rate = dropout_rate
        self.random_state = random_state
        self._session = None

    def _dnn(self, inputs):
        for layer in range(self.n_hidden_layers):
            if self.dropout_rate:
                inputs = tf.layers.dropout(inputs, self.dropout_rate, training=self._training)
            inputs = tf.layers.dense(inputs, self.n_neurons,
                                     kernel_initializer=self.initializer,
                                     name="hidden%d" % (layer + 1))
            if self.batch_norm_momentum:
                inputs = tf.layers.batch_normalization(inputs, momentum=self.batch_norm_momentum,
                                                       training=self._training)
            inputs = self.activation(inputs, name="hidden%d_out" % (layer + 1))
        return inputs

    def _build_graph(self, n_inputs, n_outputs):
        if self.random_state is not None:
            tf.set_random_seed(self.random_state)
            np.random.seed(self.random_state)

        X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
        y = tf.placeholder(tf.int32, shape=(None), name="y")

        if self.batch_norm_momentum or self.dropout_rate:
            self._training = tf.placeholder_with_default(False, shape=(), name="training")
        else:
            self._training = None

        dnn_outputs = self._dnn(X)

        logits = tf.layers.dense(dnn_outputs, n_outputs, kernel_initializer=he_init, name="logits")
        Y_proba = tf.nn.softmax(logits, name="Y_proba")

        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
        loss = tf.reduce_mean(xentropy, name="loss")

        optimizer = self.optimizer_class(learning_rate=self.learning_rate)
        training_op = optimizer.minimize(loss)

        correct = tf.nn.in_top_k(logits, y, 1)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()

        self._X, self._y = X, y
        self._Y_Proba, self._loss = Y_proba, loss
        self._training_op, self._accuracy = training_op, accuracy
        self._init, self._saver = init, saver

    def close_session(self):
        if self._session:
            self._session.close()

    def _get_model_params(self):
        with self._graph.as_default():
            gvar = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
        return {gvar.op.name: value for gvar, value in zip(gvar, self._session.run(gvar))}

    def _restore_model_params(self, model_params):
        gvar_names = list(model_params.keys())
        assign_ops = {gvar_name: self._graph.get_operation_by_name(gvar_name + "/Assign") for gvar_name in gvar_names}
        init_values = {gvar_name: assign_op.inputs[1] for gvar_name, assign_op in assign_ops.items()}
        feed_dict = {init_values[gvar_name]: model_params[gvar_name] for gvar_name in gvar_names}
        self._session.run(assign_ops, feed_dict=feed_dict)

    def fit(self, X, y, n_epochs=100, X_valid=None, y_valid=None):
        self.close_session()

        n_inputs = X.shape[1]
        self.classes_ = np.unique(y)
        n_outputs = len(self.classes_)

        self.class_to_index = {label: index for index, label in enumerate(self.classes_)}
        y = np.array([self.class_to_index[label] for label in y], dtype=np.int32)

        self._graph = tf.Graph()
        with self._graph.as_default():
            self._build_graph(n_inputs, n_outputs)
            extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

        max_checks_without_progress = 20
        checks_without_progress = 0
        best_loss = np.infty
        best_params = None

        self._session = tf.Session(graph=self._graph)
        with self._session.as_default() as sess:
            self._init.run()
            for epoch in range(n_epochs):
                rnd_idx = np.random.permutation(len(X))
                for rnd_indices in np.array_split(rnd_idx, len(X) // self.batch_size):
                    X_batch, y_batch = X[rnd_indices], y[rnd_indices]
                    feed_dict = {self._X: X_batch, self._y: y_batch}
                    if self._training is not None:
                        feed_dict[self._training] = True
                    sess.run(self._training_op, feed_dict=feed_dict)
                    if extra_update_ops:
                        sess.run(self._training_op, feed_dict=feed_dict)
                if X_valid is not None and y_valid is not None:
                    loss_val, acc_val = sess.run([self._loss, self._accuracy],
                                                 feed_dict={self._X: X_valid, self._y: y_valid})
                    if loss_val < best_loss:
                        best_params = self._get_model_params()
                        best_loss = loss_val
                        checks_without_progress = 0
                    else:
                        checks_without_progress += 1
                    print("{}\tValidation loss: {:.6f}\tBest loss:{:.6f}\tAccuracy:{:.2f}%".format(
                        epoch, loss_val, best_loss, acc_val * 100
                    ))
                    if checks_without_progress > max_checks_without_progress:
                        print("Early stopping!")
                        break
                else:
                    loss_train, acc_train = sess.run([self._loss, self._accuracy],
                                                     feed_dict={self._X: X_batch, self._y: y_batch})
                    print("{}\tLast training batch loss:{:.6f}\tAccuracy:{:.2f}%".format(
                        epoch, loss_train, acc_train * 100
                    ))
            if best_params:
                self._restore_model_params(best_params)
            return self

    def predict_proba(self, X):
        if not self._session:
            raise NotFittedError("This %s instance is not fitted yet" % self.__class__.__name__)
        with self._session.as_default() as sess:
            return self._Y_Proba.eval(feed_dict={self._X: X})

    def predict(self, X):
        class_indices = np.argmax(self.predict_proba(X), axis=1)
        return np.array([[self.classes_[class_index]]
                         for class_index in class_indices], np.int32)

    def save(self, path):
        self._saver.save(self._session, path)


def leaky_relu(alpha=0.01):
    def parametrized_leaky_relu(z, name=None):
        return tf.maximum(alpha * z, z, name=name)
    return parametrized_leaky_relu


# dnn_clf = DNNClassifier(random_state=42)
# print(dnn_clf.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1))
#
# y_pred = dnn_clf.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))

# param_distribs = {
#     "n_neurons": [10, 30, 50, 70, 90, 100, 120, 140, 160],
#     "batch_size": [10, 50, 100, 500],
#     "learning_rate": [0.01, 0.02, 0.05, 0.1],
#     "activation": [tf.nn.relu, tf.nn.elu, leaky_relu(alpha=0.01), leaky_relu(alpha=0.1)],
#     "n_hidden_layers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     "optimizer_class": [tf.train.AdamOptimizer, partial(tf.train.MomentumOptimizer, momentum=0.95)]
# }
#
# rnd_search = RandomizedSearchCV(DNNClassifier(random_state=42), param_distribs, n_iter=50, cv=3, random_state=42, verbose=2)
# rnd_search.fit(X_train1, y_train1, X_valid=X_valid1, y_valid=y_valid1, n_epochs=1000)
#
# print(rnd_search.best_params_)
#
# y_pred = rnd_search.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))
#
# print(rnd_search.best_estimator_.save("./my_best_mnist_model_0_to_4"))

# dnn_clf = DNNClassifier(activation=leaky_relu(alpha=0.1), batch_size=50, learning_rate=0.02,
#                            n_neurons=90, optimizer_class=partial(tf.train.MomentumOptimizer, momentum=0.95),
#                            random_state=42)
# print(dnn_clf.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1))
#
# y_pred = dnn_clf.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))
#
# dnn_clf_bn = DNNClassifier(activation=leaky_relu(alpha=0.1), batch_size=50, learning_rate=0.02,
#                            n_neurons=90, optimizer_class=tf.train.MomentumOptimizer(learning_rate=0.02, momentum=0.95),
#                            random_state=42, batch_norm_momentum=0.95)
# print(dnn_clf_bn.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1))
#
# y_pred = dnn_clf_bn.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))


# param_distribs = {
#     "n_neurons": [160],
#     "batch_size": [10],
#     "learning_rate": [0.01],
#     "activation": [tf.nn.relu],
#     "batch_norm_momentum": [0.98]
# }
#
#
# rnd_search_bn = RandomizedSearchCV(DNNClassifier(random_state=42), param_distribs, n_iter=50, cv=3,
#                                    random_state=42, verbose=2, n_jobs=-1)
# rnd_search_bn.fit(X_train1, y_train1, X_valid=X_valid1, y_valid=y_valid1, n_epochs=1000)
#
#
# print(rnd_search_bn.best_estimator_)
#
# y_pred = rnd_search_bn.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))


# dnn_clf_dropout = DNNClassifier(activation=leaky_relu(alpha=0.1), batch_size=500, learning_rate=0.01, n_neurons=90,
#                                 random_state=42, dropout_rate=0.5)
# dnn_clf_dropout.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1)
#
# y_pred = dnn_clf_dropout.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))
#
# param_distribs = {
#     "n_neurons": [160],
#     "batch_size": [100],
#     "learning_rate": [0.01],
#     "activation": [tf.nn.relu],
#     "dropout_rate": [0.2]
# }
#
# rnd_search_dropout = RandomizedSearchCV(DNNClassifier(random_state=42), param_distribs, n_iter=50,
#                                         cv=3, random_state=42, verbose=2, n_jobs=-1)
# rnd_search_dropout.fit(X_train1, y_train1, X_valid=X_valid1, y_valid=y_valid1, n_epochs=1000)
#
# print(rnd_search_dropout.best_estimator_)
#
# y_pred = rnd_search_dropout.predict(X_test1)
# print(accuracy_score(y_test1, y_pred))


# X_train2_full = X_train[y_train >= 5]
# y_train2_full = y_train[y_train >= 5] - 5
# X_valid2_full = X_valid[y_valid >= 5]
# y_valid2_full = y_valid[y_valid >= 5] - 5
# X_test2 = X_test[y_test >= 5]
# y_test2 = y_test[y_test >= 5] - 5
#
#
# def sample_n_instances_per_class(X, y, n=100):
#     Xs, ys = [], []
#     for labels in np.unique(y):
#         idx = (y == labels)
#         Xc = X[idx][:n]
#         yc = y[idx][:n]
#         Xs.append(Xc)
#         ys.append(yc)
#     return np.concatenate(Xs), np.concatenate(ys)
#
#
# X_train2, y_train2 = sample_n_instances_per_class(X_train2_full, y_train2_full, n=100)
# X_valid2, y_valid2 = sample_n_instances_per_class(X_train2_full, y_train2_full, n=30)

#
# reset_graph()
#
# restore_saver = tf.train.import_meta_graph("./my_best_mnist_model_0_to_4.meta")
#
# X = tf.get_default_graph().get_tensor_by_name("X:0")
# y = tf.get_default_graph().get_tensor_by_name("y:0")
# loss = tf.get_default_graph().get_tensor_by_name("loss:0")
# Y_proba = tf.get_default_graph().get_tensor_by_name("Y_proba:0")
# logits = Y_proba.op.inputs[0]
# accuracy = tf.get_default_graph().get_tensor_by_name("accuracy:0")
#
# learning_rate = 0.01
#
# output_layer_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope="logits")
# optimizer = tf.train.AdamOptimizer(learning_rate, name="Adam2")
# training_op = optimizer.minimize(loss, var_list=output_layer_vars)
#
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# init = tf.global_variables_initializer()
# five_frozen_saver = tf.train.Saver()
#
#
# n_epochs = 1000
# batch_size = 20
#
# max_checks_without_progress = 20
# checks_without_progress = 0
# best_loss = np.infty

# with tf.Session() as sess:
#     init.run()
#     restore_saver.restore(sess, "./my_best_mnist_model_0_to_4")
#     t0 = time.time()
#
#     for epoch in range(n_epochs):
#         rnd_idx = np.random.permutation(len(X_train2))
#         for rnd_indices in np.array_split(rnd_idx, len(X_train2) // batch_size):
#             X_batch, y_batch = X_train2[rnd_indices], y_train2[rnd_indices]
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         loss_val, acc_val = sess.run([loss, accuracy], feed_dict={X: X_valid2, y: y_valid2})
#         if loss_val < best_loss:
#             save_path = five_frozen_saver.save(sess, "./my_mnist_model_5_to_9_five_frozen")
#             best_loss = loss_val
#             checks_without_progress = 0
#         else:
#             checks_without_progress += 1
#             if checks_without_progress > max_checks_without_progress:
#                 print("Early stopping")
#                 break
#         print("{}\tValidation loss: {:.6f}\tBest loss:{:.6f}\tAccuracy: {:.2f}%".format(
#             epoch, loss_val, best_loss, acc_val * 100
#         ))
#     t1 = time.time()
#     print("Total training time:{:.1f}s".format(t1 - t0))
#
# with tf.Session() as sess:
#     five_frozen_saver.restore(sess, "./my_mnist_model_5_to_9_five_frozen")
#     acc_test = accuracy.eval(feed_dict={X: X_test2, y: y_test2})
#     print("Final tet accuracy: {:.2f}%".format(acc_test * 100))

# hidden5_out = tf.get_default_graph().get_tensor_by_name("hidden4_out:0")
#
# with tf.Session() as sess:
#     init.run()
#     restore_saver.restore(sess, "./my_best_mnist_model_0_to_4")
#     t0 = time.time()
#
#     hidden5_train = hidden5_out.eval(feed_dict={X: X_train2, y: y_train2})
#     hidden5_valid = hidden5_out.eval(feed_dict={X: X_valid2, y: y_valid2})
#
#     for epoch in range(n_epochs):
#         rnd_idx = np.random.permutation(len(X_train2))
#         for rnd_indices in np.array_split(rnd_idx, len(X_train2) // batch_size):
#             h5_batch, y_batch = hidden5_train[rnd_indices], y_train2[rnd_indices]
#             sess.run(training_op, feed_dict={hidden5_out: h5_batch, y: y_batch})
#         loss_val, acc_val = sess.run([loss, accuracy], feed_dict={hidden5_out: hidden5_valid, y: y_valid2})
#         if loss_val < best_loss:
#             save_path = five_frozen_saver.save(sess, "./my_mnist_model_5_to_9_five_frozen")
#             best_loss = loss_val
#             checks_without_progress = 0
#         else:
#             checks_without_progress += 1
#             if checks_without_progress > max_checks_without_progress:
#                 print("Early stopping!")
#                 break
#         print("{}\tValidation loss: {:.6f}\t Best loss: {:.6f} \t Accuracy: {:.2f}%".format(
#             epoch, loss_val, best_loss, acc_val * 100
#         ))
#
#     t1 = time.time()
#     print("Total training time:{:.1f}s".format(t1 - t0))
#
# with tf.Session() as sess:
#     five_frozen_saver.restore(sess, "./my_mnist_model_5_to_9_five_frozen")
#     acc_test = accuracy.eval(feed_dict={X: X_test2, y: y_test2})
#     print("Final test accuracy: {:.2f}%".format(acc_test * 100))

# reset_graph()
#
# n_outputs = 5
# restore_saver = tf.train.import_meta_graph("./my_best_mnist_model_0_to_4.meta")
#
# X = tf.get_default_graph().get_tensor_by_name("X:0")
# y = tf.get_default_graph().get_tensor_by_name("y:0")
#
# hidden3_out = tf.get_default_graph().get_tensor_by_name("hidden3_out:0")
# logits = tf.layers.dense(hidden3_out, n_outputs, kernel_initializer=he_init, name="new_logits")
# Y_proba = tf.nn.softmax(logits)
# xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
# loss = tf.reduce_mean(xentropy)
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
#
# learning_rate = 0.01
#
# output_layer_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope="new_logits")
# optimizer = tf.train.AdamOptimizer(learning_rate, name="Adam2")
# training_op = optimizer.minimize(loss, var_list=output_layer_vars)
#
# init = tf.global_variables_initializer()
# four_frozen_saver = tf.train.Saver()
#
# n_epochs = 1000
# batch_size = 20
#
# max_checks_without_progress = 20
# checks_without_progress = 0
# best_loss = np.infty
#
# with tf.Session() as sess:
#     init.run()
#     restore_saver.restore(sess, "./my_best_mnist_model_0_to_4")
#     for epoch in range(n_epochs):
#         rnd_idx = np.random.permutation(len(X_train2))
#         for rnd_indices in np.array_split(rnd_idx, len(X_train2) // batch_size):
#             X_batch, y_batch = X_train2[rnd_indices], y_train2[rnd_indices]
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         loss_val, acc_val = sess.run([loss, accuracy], feed_dict={X: X_valid2, y: y_valid2})
#         if loss_val < best_loss:
#             save_path = four_frozen_saver.save(sess, "./my_mnist_model_5_to_9_four_frozen")
#             best_loss = loss_val
#             checks_without_progress = 0
#         else:
#             checks_without_progress += 1
#             if checks_without_progress > max_checks_without_progress:
#                 print("Early stopping!")
#                 break
#         print("{}\tValidation loss: {:.6f}\t Best loss: {:.6f}\tAccuracy: {:.2f}%".format(
#             epoch, loss_val, best_loss, acc_val * 100
#         ))
#
# with tf.Session() as sess:
#     four_frozen_saver.restore(sess, "./my_mnist_model_5_to_9_four_frozen")
#     acc_test = accuracy.eval(feed_dict={X: X_test2, y: y_test2})
#     print("Final test accuracy: {:.2f}%".format(acc_test * 100))
#
# learning_rate = 0.01
#
# unfrozen_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope="hidden[23]|new_logits")
# optimizer = tf.train.AdamOptimizer(learning_rate, name="Adam3")
# training_op = optimizer.minimize(loss, var_list=unfrozen_vars)
#
# init = tf.global_variables_initializer()
# two_frozen_saver = tf.train.Saver()
#
# n_epochs = 1000
# batch_size = 20
#
# max_checks_without_progress = 20
# checks_without_progress = 0
# best_loss = np.infty
#
# with tf.Session() as sess:
#     init.run()
#     four_frozen_saver.restore(sess, "./my_mnist_model_5_to_9_four_frozen")
#     for epoch in range(n_epochs):
#         rnd_idx = np.random.permutation(len(X_train2))
#         for rnd_indices in np.array_split(rnd_idx, len(X_train2) // batch_size):
#             X_batch, y_batch = X_train2[rnd_indices], y_train2[rnd_indices]
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         loss_val, acc_val = sess.run([loss, accuracy], feed_dict={X: X_valid2, y: y_valid2})
#         if loss_val < best_loss:
#             save_path = two_frozen_saver.save(sess, "./my_mnist_model_5_to_9_two_frozen")
#             best_loss = loss_val
#             checks_without_progress = 0
#         else:
#             checks_without_progress += 1
#             if checks_without_progress > max_checks_without_progress:
#                 print("Early stopping!")
#                 break
#         print("{}\tValidation loss: {:.6f}\t Best loss: {:.6f}\t Accuracy: {:.2f}%".format(
#             epoch, loss_val, best_loss, acc_val * 100
#         ))
#
# with tf.Session() as sess:
#     two_frozen_saver.restore(sess, "./my_mnist_model_5_to_9_two_frozen")
#     acc_test = accuracy.eval(feed_dict={X: X_test2, y: y_test2})
#     print("Final test accuracy: {:.2f}%".format(acc_test * 100))
#
# dnn_clf_5_to_9 = DNNClassifier(n_hidden_layers=3, random_state=42)
# print(dnn_clf_5_to_9.fit(X_train2, y_train2, n_epochs=1000, X_valid=X_valid2, y_valid=y_valid2))
#
# y_pred = dnn_clf_5_to_9.predict(X_test2)
# print(accuracy_score(y_test2, y_pred))

n_inputs = 28 * 28

reset_graph()

X = tf.placeholder(tf.float32, shape=(None, 2, n_inputs), name="X")
X1, X2 = tf.unstack(X, axis=1)

y = tf.placeholder(tf.int32, shape=[None, 1])

he_init = tf.variance_scaling_initializer()


def dnn(inputs, n_hidden_layers=5, n_nerurons=100, name=None,
        activation=tf.nn.elu, initializer=he_init):
    with tf.variable_scope(name, "dnn"):
        for layer in range(n_hidden_layers):
            inputs = tf.layers.dense(inputs, n_nerurons, activation=activation,
                                     kernel_initializer=initializer, name="hidden%d" % (layer + 1))
        return inputs


dnn1 = dnn(X1, name="DNN_A")
dnn2 = dnn(X2, name="DNN_B")

dnn_outputs = tf.concat([dnn1, dnn2], axis=1)

hidden = tf.layers.dense(dnn_outputs, units=10, activation=tf.nn.elu, kernel_initializer=he_init)
logits = tf.layers.dense(hidden, units=1, kernel_initializer=he_init)
Y_proba = tf.nn.sigmoid(logits)

y_pred = tf.cast(tf.greater_equal(logits, 0), tf.int32)

y_as_float = (tf.cast(y, tf.float32))
xentropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_as_float, logits=logits)
loss = tf.reduce_mean(xentropy)

learning_rate = 0.01
momentum = 0.95

optimizer = tf.train.MomentumOptimizer(learning_rate, momentum, use_nesterov=True)
training_op = optimizer.minimize(loss)

y_pred_correct = tf.equal(y_pred, y)
accuracy = tf.reduce_mean(tf.cast(y_pred_correct, tf.float32))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

X_train1 = X_train
y_train1 = y_train

X_train2 = X_valid
y_train2 = y_valid

X_test = X_test
y_test = y_test


def generate_batch(images, labels, batch_size):
    size1 = batch_size // 2
    size2 = batch_size - size1
    if size1 != size2 and np.random.rand() > 0.5:
        size1, size2 = size2, size1
    X = []
    y = []
    while len(X) < size1:
        rnd_idx1, rnd_idx2 = np.random.randint(0, len(images), 2)
        if rnd_idx1 != rnd_idx2 and labels[rnd_idx1] == labels[rnd_idx2]:
            X.append(np.array([images[rnd_idx1], images[rnd_idx2]]))
            y.append([1])
    while len(X) < batch_size:
        rnd_idx1, rnd_idx2 = np.random.randint(0, len(images), 2)
        if labels[rnd_idx1] != labels[rnd_idx2]:
            X.append(np.array([images[rnd_idx1], images[rnd_idx2]]))
            y.append([0])
    rnd_indices = np.random.permutation(batch_size)
    return np.array(X)[rnd_indices], np.array(y)[rnd_indices]


# batch_size = 5
# X_batch, y_batch = generate_batch(X_train1, y_train1, batch_size)
# print(X_batch.shape, X_batch.dtype)
#
# plt.figure(figsize=(3, 3 * batch_size))
# plt.subplot(121)
# plt.imshow(X_batch[:, 0].reshape(28 * batch_size, 28), cmap="binary", interpolation="nearest")
# plt.axis('off')
# plt.subplot(122)
# plt.imshow(X_batch[:, 1].reshape(28 * batch_size, 28), cmap="binary", interpolation="nearest")
# plt.axis('off')
# plt.show()
#
# print(y_batch)

# X_test1, y_test1 = generate_batch(X_test, y_test, batch_size=len(X_test))
#
# n_epochs = 100
# batch_size = 500
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for iteration in range(len(X_train1) // batch_size):
#             X_batch, y_batch = generate_batch(X_train1, y_train1, batch_size)
#             loss_val, _ = sess.run([loss, training_op], feed_dict={X: X_batch, y: y_batch})
#         print(epoch, "Train loss:", loss_val)
#         if epoch % 5 == 0:
#             acc_test = accuracy.eval(feed_dict={X: X_test1, y: y_test1})
#             print(epoch, "Test accuracy:", acc_test)
#     save_path = saver.save(sess, "./my_digit_comparison_model.ckpt")

# reset_graph()
#
# n_inputs = 28 * 28
# n_outputs = 10
#
# X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
# y = tf.placeholder(tf.int32, shape=(None), name="y")
#
# dnn_outputs = dnn(X, name="DNN_A")
# frozen_outputs = tf.stop_gradient(dnn_outputs)
#
# logits = tf.layers.dense(dnn_outputs, n_outputs, kernel_initializer=he_init)
# Y_proba = tf.nn.softmax(logits)
#
# xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
# loss = tf.reduce_mean(xentropy, name="loss")
#
# optimizer = tf.train.MomentumOptimizer(learning_rate, momentum, use_nesterov=True)
# training_op = optimizer.minimize(loss)
#
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
#
# dnn_A_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="DNN_A")
# restore_saver = tf.train.Saver(var_list={var.op.name: var for var in dnn_A_vars})
# saver = tf.train.Saver()
#
# n_epochs = 100
# batch_size = 50
#
# with tf.Session() as sess:
#     init.run()
#     restore_saver.restore(sess, "./my_digit_comparison_model.ckpt")
#
#     for epoch in range(n_epochs):
#         rnd_idx = np.random.permutation(len(X_train2))
#         for rnd_indices in np.array_split(rnd_idx, len(X_train2) // batch_size):
#             X_batch, y_batch = X_train2[rnd_indices], y_train2[rnd_indices]
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         if epoch % 10 == 0:
#             acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
#             print(epoch, "Test accuracy:", acc_test)
#     save_path = saver.save(sess, "./my_mnist_model_final.ckpt")

reset_graph()

n_inputs = 28 * 28
n_outputs = 10

X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
y = tf.placeholder(tf.int32, shape=(None), name="y")

dnn_outputs = dnn(X, name="DNN_A")

logits = tf.layers.dense(dnn_outputs, n_outputs, kernel_initializer=he_init)
Y_proba = tf.nn.softmax(logits)

xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
loss = tf.reduce_mean(xentropy, name="loss")

optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=momentum, use_nesterov=True)
training_op = optimizer.minimize(loss)

correct = tf.nn.in_top_k(logits, y, 1)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

init = tf.global_variables_initializer()

dnn_A_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="DNN_A")
restore_vars = tf.train.Saver(var_list={var.op.name: var for var in dnn_A_vars})
saver = tf.train.Saver()

n_epochs = 150
batch_size = 50

with tf.Session() as sess:
    init.run()

    for epoch in range(n_epochs):
        rnd_idx = np.random.permutation(len(X_train2))
        for rnd_indices in np.array_split(rnd_idx, len(X_train2) // batch_size):
            X_batch, y_batch = X_train2[rnd_indices], y_train2[rnd_indices]
            sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
        if epoch % 10 == 0:
            acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
            print(epoch, "Test accuracy:", acc_test)
    save_path = saver.save(sess, "./my_mnist_model_final.ckpt")


