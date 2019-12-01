# -*- coding: utf-8 -*-
# @Time    : 2019-01-14 19:35
# @Author  : ssdcxy
# @Email   : 18379190862@163.com
# @File    : RecurrentNeuralNetworks.py

import numpy as np
import os
import tensorflow as tf
from six.moves import urllib
import errno
import os
import zipfile
from collections import Counter
from collections import deque
from sklearn.manifold import TSNE


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
CHAPTER_ID = "rnn"


def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID, fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format="png", dpi=300)


reset_graph()

# n_inputs = 3
# n_neurons = 5
#
# X0 = tf.placeholder(tf.float32, [None, n_inputs])
# X1 = tf.placeholder(tf.float32, [None, n_inputs])
#
# Wx = tf.Variable(tf.random_normal(shape=[n_inputs, n_neurons], dtype=tf.float32))
# Wy = tf.Variable(tf.random_normal(shape=[n_neurons, n_neurons], dtype=tf.float32))
# b = tf.Variable(tf.zeros([1, n_neurons], dtype=tf.float32))
#
# Y0 = tf.tanh(tf.matmul(X0, Wx) + b)
# Y1 = tf.tanh(tf.matmul(Y0, Wy) + tf.matmul(X1, Wx) + b)
#
# init = tf.global_variables_initializer()
#
# X0_batch = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 0, 1]])
# X1_batch = np.array([[9, 8, 7], [0, 0, 0], [6, 5, 4], [3, 2, 1]])
#
# with tf.Session() as sess:
#     init.run()
#     Y0_val, Y1_val = sess.run([Y0, Y1], feed_dict={X0: X0_batch, X1: X1_batch})
#
# print(Y0_val)
# print(Y1_val)

# reset_graph()
#
# n_inputs = 3
# n_neurons = 5
#
# X0 = tf.placeholder(tf.float32, [None, n_inputs])
# X1 = tf.placeholder(tf.float32, [None, n_inputs])
#
# basic_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
# output_seqs, states = tf.nn.static_rnn(basic_cell, [X0, X1], dtype=tf.float32)
# Y0, Y1 = output_seqs
#
# init = tf.global_variables_initializer()
#
# X0_batch = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 0, 1]])
# X1_batch = np.array([[9, 8, 7], [0, 0, 0], [6, 5, 4], [3, 2, 1]])
#
# with tf.Session() as sess:
#     init.run()
#     Y0_val, Y1_val = sess.run([Y0, Y1], feed_dict={X0: X0_batch, X1: X1_batch})
#
# print(Y0_val)
# print(Y1_val)

# reset_graph()
#
# n_steps = 2
# n_inputs = 3
# n_neurons = 5
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# X_seqs = tf.unstack(tf.transpose(X, perm=[1, 0, 2]))
#
# basic_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
# output_seqs, states = tf.nn.static_rnn(basic_cell, X_seqs, dtype=tf.float32)
# outputs = tf.transpose(tf.stack(output_seqs), perm=[1, 0, 2])
#
# init = tf.global_variables_initializer()
#
# X_batch = np.array([
#     [[0, 1, 2], [9, 8, 7]],
#     [[3, 4, 5], [0, 0, 0]],
#     [[6, 7, 8], [6, 5, 4]],
#     [[9, 0, 1], [3, 2, 1]]
# ])
#
# with tf.Session() as sess:
#     init.run()
#     output_val = outputs.eval(feed_dict={X: X_batch})
#
# print(output_val)
# print(np.transpose(output_val, axes=[1, 0, 2])[1])

# reset_graph()
#
# n_steps = 2
# n_inputs = 3
# n_neurons = 5
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# basic_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
# outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32)
#
# init = tf.global_variables_initializer()
#
# X_batch = np.array([
#     [[0, 1, 2], [9, 8, 7]],
#     [[3, 4, 5], [0, 0, 0]],
#     [[6, 7, 8], [6, 5, 4]],
#     [[9, 0, 1], [3, 2, 1]]
# ])
#
# with tf.Session() as sess:
#     init.run()
#     outputs_val = outputs.eval(feed_dict={X: X_batch})
#
# print(outputs_val)

# reset_graph()
#
# n_steps = 2
# n_inputs = 3
# n_neurons = 5
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# basic_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
#
# seq_length = tf.placeholder(tf.int32, [None])
# outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32, sequence_length=seq_length)
#
# init = tf.global_variables_initializer()
#
# X_batch = np.array([
#     [[0, 1, 2], [9, 8, 7]],
#     [[3, 4, 5], [0, 0, 0]],
#     [[6, 7, 8], [6, 5, 4]],
#     [[9, 0, 1], [3, 2, 1]]
# ])
# seq_length_batch = np.array([2, 1, 2, 2])
#
# with tf.Session() as sess:
#     init.run()
#     outputs_val, states_val = sess.run([outputs, states], feed_dict={X: X_batch, seq_length: seq_length_batch})
#
# print(outputs_val)
# print(states_val)

# reset_graph()
#
# n_steps = 28
# n_inputs = 28
# n_neurons = 150
# n_outputs = 10
#
# learning_rate = 0.001
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.int32, [None])
#
# basic_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
# outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32)
#
# logits = tf.layers.dense(states, n_outputs)
# xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
#
# loss = tf.reduce_mean(xentropy)
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
#
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_train = X_train.astype(np.float32).reshape(-1, 28 * 28) / 255.0
X_test = X_test.astype(np.float32).reshape(-1, 28 * 28) / 255.0
y_train = y_train.astype(np.int32)
y_test = y_test.astype(np.int32)
X_valid, X_train = X_train[:5000], X_train[5000:]
y_valid, y_train = y_train[:5000], y_train[5000:]


def shuffle_batch(X, y, batch_size):
    rnd_idx = np.random.permutation(len(X))
    n_batches = len(X) // batch_size
    for batch_idx in np.array_split(rnd_idx, n_batches):
        X_batch, y_batch = X[batch_idx], y[batch_idx]
        yield X_batch, y_batch


# X_test = X_test.reshape((-1, n_steps, n_inputs))
#
# n_epochs = 100
# batch_size = 150
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             X_batch = X_batch.reshape((-1, n_steps, n_inputs))
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         acc_batch = accuracy.eval(feed_dict={X: X_batch, y: y_batch})
#         acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
#         print(epoch, "Last batch accuracy:", acc_batch, "Test accuracy:", acc_test)

# reset_graph()
#
# n_steps = 28
# n_inputs = 28
# n_outputs = 10
#
# learning_rate = 0.001
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.int32, [None])
#
# n_neurons = 100
# n_layers = 4
#
# layers = [tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons, activation=tf.nn.relu) for layer in range(n_layers)]
# mult_layer_cell = tf.nn.rnn_cell.MultiRNNCell(layers)
# outputs, states = tf.nn.dynamic_rnn(mult_layer_cell, X, dtype=tf.float32)
#
# states_concat = tf.concat(axis=1, values=states)
# logits = tf.layers.dense(states_concat, n_outputs)
# xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
# loss = tf.reduce_mean(xentropy)
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
#
# n_epochs = 10
# batch_size = 150
#
# X_test = X_test.reshape((-1, n_steps, n_inputs))
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             X_batch = X_batch.reshape((-1, n_steps, n_inputs))
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         acc_batch = accuracy.eval(feed_dict={X: X_batch, y: y_batch})
#         acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
#         print(epoch, "Last batch accuracy:", acc_batch, "Test accuracy:", acc_test)

t_min, t_max = 0, 30
resolution = 0.1


def time_series(t):
    return t * np.sin(t) / 3 + 2 * np.sin(5 * t)


def next_batch(batch_size, n_steps):
    t0 = np.random.rand(batch_size, 1) * (t_max - t_min - n_steps * resolution)
    Ts = t0 + np.arange(0., n_steps + 1) * resolution
    ys = time_series(Ts)
    return ys[:, :-1].reshape(-1, n_steps, 1), ys[:, 1:].reshape(-1, n_steps, 1)


t = np.linspace(t_min, t_max, int((t_max - t_min) / resolution))

n_steps = 20
t_instance = np.linspace(12.2, 12.2 + resolution * (n_steps + 1), n_steps + 1)

# plt.figure(figsize=(11, 4))
# plt.subplot(121)
# plt.title("A time series (generated)", fontsize=14)
# plt.plot(t, time_series(t), label=r"$t . \sin(t) / 3 + 2. sin(5t)$")
# plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "b-", linewidth=3, label="A training instance")
# plt.legend(loc="lower left", fontsize=14)
# plt.axis([0, 30, -17, 13])
# plt.xlabel("Time")
# plt.ylabel("Value")
#
# plt.subplot(122)
# plt.title("A training instance", fontsize=14)
# plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "bo", markersize=10, label="instance")
# plt.plot(t_instance[1:], time_series(t_instance[1:]), "w*", markersize=10, label="target")
# plt.legend(loc="upper left")
# plt.xlabel("Time")
# save_fig("time_series_plot")
# plt.show()
#
# X_batch, y_batch = next_batch(1, n_steps)
# print(np.c_[X_batch[0], y_batch[0]])

# reset_graph()
#
# n_steps = 20
# n_inputs = 1
# n_neurons = 100
# n_outputs = 1
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
#
# cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons, activation=tf.nn.relu)
# outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)


# reset_graph()
#
# n_steps = 20
# n_inputs = 1
# n_neurons = 100
# n_outputs = 1
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
#
# cell = tf.contrib.rnn.OutputProjectionWrapper(
#     tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons, activation=tf.nn.relu),
#     output_size=n_outputs
# )
# outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
#
# learning_rate = 0.001
#
# loss = tf.reduce_mean(tf.square(outputs - y))
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
#
# init = tf.global_variables_initializer()
#
# saver = tf.train.Saver()
#
# n_iteration = 1500
# batch_size = 50

# with tf.Session() as sess:
#     init.run()
#     for iteration in range(n_iteration):
#         X_batch, y_batch = next_batch(batch_size, n_steps)
#         sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         if iteration % 100 == 0:
#             mse = loss.eval(feed_dict={X: X_batch, y: y_batch})
#             print(iteration, "\tMSE:", mse)
#
#     saver.save(sess, "./my_time_series_model")

# with tf.Session() as sess:
#     saver.restore(sess, "./my_time_series_model")
#     X_new = time_series(np.array(t_instance[:-1].reshape(-1, n_steps, n_inputs)))
#     y_pred = sess.run(outputs, feed_dict={X: X_new})
#
# print(y_pred)
#
# plt.title("Testing the model", fontsize=14)
# plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "bo", markersize=10, label="instance")
# plt.plot(t_instance[1:], time_series(t_instance[1:]), "w*", markersize=10, label="target")
# plt.plot(t_instance[1:], y_pred[0, :, 0], "r.", markersize=10, label="prediction")
# plt.legend(loc="upper left")
# plt.xlabel("Time")
#
# save_fig("time_series_pred_plot")
# plt.show()

# reset_graph()
#
# n_steps = 20
# n_inputs = 1
# n_neurons = 100
# n_outputs = 1
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
#
# cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons, activation=tf.nn.relu)
# rnn_outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
#
# n_outputs = 1
# learning_rate = 0.001
#
# stacked_rnn_outputs = tf.reshape(rnn_outputs, [-1, n_neurons])
# stacked_outputs = tf.layers.dense(stacked_rnn_outputs, n_outputs)
# outputs = tf.reshape(stacked_outputs, [-1, n_steps, n_outputs])
#
# loss = tf.reduce_mean(tf.square(outputs - y))
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# n_iteration = 1500
# batch_size = 50

# with tf.Session() as sess:
#     init.run()
#     for iteration in range(n_iteration):
#         X_batch, y_batch = next_batch(batch_size, n_steps)
#         sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         if iteration % 100 == 0:
#             mse = loss.eval(feed_dict={X: X_batch, y: y_batch})
#             print(iteration, "\tMSE:", mse)
#     X_new = time_series(np.array(t_instance[:-1].reshape(-1, n_steps, n_inputs)))
#     y_pred = sess.run(outputs, feed_dict={X: X_new})
#     saver.save(sess, "./my_time_series_model")

# with tf.Session() as sess:
#     saver.restore(sess, "./my_time_series_model")
#     sequence = [0.] * n_steps
#     for iteration in range(300):
#         X_batch = np.array(sequence[-n_steps:]).reshape(1, n_steps, 1)
#         y_pred = sess.run(outputs, feed_dict={X: X_batch})
#         sequence.append(y_pred[0, -1, 0])
#
# plt.figure(figsize=(8, 4))
# plt.plot(np.arange(len(sequence)), sequence, "b-")
# plt.plot(t[:n_steps], sequence[:n_steps], "b-", linewidth=3)
# plt.xlabel("Time")
# plt.ylabel("Value")
# plt.show()

# with tf.Session() as sess:
#     saver.restore(sess, "./my_time_series_model")
#     sequence1 = [0. for i in range(n_steps)]
#     for iteration in range(len(t) - n_steps):
#         X_batch = np.array(sequence1[-n_steps:]).reshape(1, n_steps, 1)
#         y_pred = sess.run(outputs, feed_dict={X: X_batch})
#         sequence1.append(y_pred[0, -1, 0])
#
#     sequence2 = [time_series(i * resolution + t_min + (t_max-t_min/3)) for i in range(n_steps)]
#     for iteration in range(len(t) - n_steps):
#         X_batch = np.array(sequence2[-n_steps:]).reshape(1, n_steps, 1)
#         y_pred = sess.run(outputs, feed_dict={X: X_batch})
#         sequence2.append(y_pred[0, -1, 0])
#
# plt.figure(figsize=(11, 4))
# plt.subplot(121)
# plt.plot(t, sequence1, "b-")
# plt.plot(t[:n_steps], sequence1[:n_steps], "b-", linewidth=3)
# plt.xlabel("Time")
# plt.ylabel("Value")
#
# plt.subplot(122)
# plt.plot(t, sequence2, "b-")
# plt.plot(t[:n_steps], sequence2[:n_steps], "b-", linewidth=3)
# plt.xlabel("Time")
# save_fig("creative_sequence_plot")
# plt.show()

# reset_graph()
#
# n_inputs = 2
# n_steps = 5
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
#
# n_nurons = 100
# n_layers = 3
#
# layers = [tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
#           for layer in range(n_layers)]
# multi_layer_cell = tf.nn.rnn_cell.MultiRNNCell(layers)
# outputs, states = tf.nn.dynamic_rnn(multi_layer_cell, X, dtype=tf.float32)
#
# init = tf.global_variables_initializer()
#
# X_batch = np.random.rand(2, n_steps, n_inputs)
#
# with tf.Session() as sess:
#     init.run()
#     outputs_val, states_val = sess.run([outputs, states], feed_dict={X: X_batch})
#
# print(outputs_val.shape)


class DeviceCellWrapper(tf.nn.rnn_cell.RNNCell):
    def __init__(self, device, cell):
        self._cell = cell
        self._device = device

    @property
    def state_size(self):
        return self._cell.state_size

    @property
    def output_size(self):
        return self._cell.output_size

    def __call__(self, inputs, state, scope=None):
        with tf.device(self._device):
            return self._cell(inputs, state, scope)


# reset_graph()
#
# n_inputs = 5
# n_steps = 20
# n_neurons = 100
#
# X = tf.placeholder(tf.float32, shape=[None, n_steps, n_inputs])
#
# devices = ["/cpu:0", "/cpu:0", "/cpu:0"]
# cells = [DeviceCellWrapper(dev, tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)) for dev in devices]
# multi_layer_cell = tf.nn.rnn_cell.MultiRNNCell(cells)
# outputs, states = tf.nn.dynamic_rnn(multi_layer_cell, X, dtype=tf.float32)
#
# init = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     init.run()
#     print(sess.run(outputs, feed_dict={X: np.random.rand(2, n_steps, n_inputs)}))

# reset_graph()
#
# n_inputs = 1
# n_neurons = 100
# n_layers = 3
# n_steps = 20
# n_outputs = 1
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
#
# keep_prob = tf.placeholder_with_default(1.0, shape=())
# cells = [tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons) for layer in range(n_layers)]
# cells_drop = [tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=keep_prob) for cell in cells]
# multi_layer_cell = tf.nn.rnn_cell.MultiRNNCell(cells_drop)
# rnn_outputs, states = tf.nn.dynamic_rnn(multi_layer_cell, X, dtype=tf.float32)
#
# learning_rate = 0.01
#
# stacked_rnn_outputs = tf.reshape(rnn_outputs, [-1, n_neurons])
# stacked_outputs = tf.layers.dense(stacked_rnn_outputs, n_outputs)
# outputs = tf.reshape(stacked_outputs, [-1, n_steps, n_outputs])
#
# loss = tf.reduce_mean(tf.square(outputs - y))
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
#
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
#
# n_iterations = 1500
# batch_size = 50
# train_keep_prob = 0.5
#
# with tf.Session() as sess:
#     init.run()
#     for iteration in range(n_iterations):
#         X_batch, y_batch = next_batch(batch_size, n_steps)
#         _, mse = sess.run([training_op, loss],
#                           feed_dict={X: X_batch, y: y_batch,
#                                      keep_prob: train_keep_prob})
#         if iteration % 100 == 0:
#             print(iteration, "Training MSE:", mse)
#     saver.save(sess, "./my_dropout_time_series_model")
#
# with tf.Session() as sess:
#     saver.restore(sess, "./my_dropout_time_series_model")
#     X_new = time_series(np.array(t_instance[:-1]).reshape(-1, n_steps, n_inputs))
#     y_pred = sess.run(outputs, feed_dict={X: X_new})
#
# plt.title("Testing the model", fontsize=14)
# plt.plot(t_instance[:-1], time_series(t_instance[:-1]), "bo", markersize=10, label="instance")
# plt.plot(t_instance[1:], time_series(t_instance[1:]), "w*", markersize=10, label="target")
# plt.plot(t_instance[1:], y_pred[0, :, 0], "r.", markersize=10, label="prediction")
# plt.legend(loc="upper left")
# plt.xlabel("Time")
#
# plt.show()
#
# reset_graph()
#
# n_steps = 28
# n_inputs = 28
# n_neurons = 150
# n_outputs = 10
# n_layers = 3
#
# learning_rate = 0.001

# LSTM
# lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=n_neurons)
# peepholes LSTM
# lstm_cell = tf.nn.rnn_cell.LSTMCell(num_units=n_neurons, use_peepholes=True)
# GRU
# gru_cell = tf.nn.rnn_cell.GRUCell(num_units=n_neurons)
#
# X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
# y = tf.placeholder(tf.int32, [None])
#
# lstm_cells = [tf.nn.rnn_cell.BasicLSTMCell(num_units=n_neurons) for layer in range(n_layers)]
# multi_cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cells)
# outputs, states = tf.nn.dynamic_rnn(multi_cell, X, dtype=tf.float32)
# top_layer_h_state = states[-1][1]
# logits = tf.layers.dense(top_layer_h_state, n_outputs, name="softmax")
# xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
# loss = tf.reduce_mean(xentropy, name="loss")
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
# correct = tf.nn.in_top_k(logits, y, 1)
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
#
# init = tf.global_variables_initializer()
#
# print(states)
# print(top_layer_h_state)
#
# n_epochs = 10
# batch_size = 150
#
# X_test = X_test.reshape((-1, n_steps, n_inputs))
#
# with tf.Session() as sess:
#     init.run()
#     for epoch in range(n_epochs):
#         for X_batch, y_batch in shuffle_batch(X_train, y_train, batch_size):
#             X_batch = X_batch.reshape((-1, n_steps, n_inputs))
#             sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
#         acc_batch = accuracy.eval(feed_dict={X: X_batch, y: y_batch})
#         acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
#         print(epoch, "Last batch accuracy:", acc_batch, "Test accuracy:", acc_test)

reset_graph()

WORDS_PATH = "garbage/words"
WORDS_URL = "http://mattmahoney.net/dc/text8.zip"


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def fetch_word_data(words_url=WORDS_URL, words_path=WORDS_PATH):
    os.makedirs(words_path, exist_ok=True)
    zip_path = os.path.join(words_path, "words.zip")
    if not os.path.exists(zip_path):
        urllib.request.urlretrieve(words_url, zip_path)
    with zipfile.ZipFile(zip_path) as f:
        data = f.read(f.namelist()[0])
    return data.decode("ascii").split()


words = fetch_word_data()

# print(words[:5])

vocabulary_size = 50000

vocabulary = [("UNK", None)] + Counter(words).most_common(vocabulary_size - 1)
vocabulary = np.array([word for word, _ in vocabulary])
dictionary = {word: code for code, word in enumerate(vocabulary)}
data = np.array([dictionary.get(word, 0) for word in words])
# print(" ".join(words[:9]), img[:9])
# print(" ".join([vocabulary[word_index] for word_index in [5241, 3081, 12, 6, 195, 2, 3134, 46, 59]]))
# print(words[24], img[24])


def generate_batch(batch_size, num_skips, skip_window):
    global data_index
    assert batch_size % num_skips == 0
    assert num_skips <= 2 * skip_window
    batch = np.ndarray(shape=[batch_size], dtype=np.int32)
    labels = np.ndarray(shape=[batch_size, 1], dtype=np.int32)
    span = 2 * skip_window + 1
    buffer = deque(maxlen=span)
    for _ in range(span):
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    for i in range(batch_size // num_skips):
        target = skip_window
        targets_to_avoid = [skip_window]
        for j in range(num_skips):
            while target in targets_to_avoid:
                target = np.random.randint(0, span)
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]
            labels[i * num_skips + j, 0] = buffer[target]
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    return batch, labels


data_index = 0
# batch, labels = generate_batch(8, 2, 1)
# print(labels, [vocabulary[word] for word in labels[:, 0]])

batch_size = 128
embedding_size = 128
skip_window = 1
num_skips = 2

valid_size = 16
valid_window = 100
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
num_sampled = 64

learning_rate = 0.01

reset_graph()

train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

vocabulary_size = 50000
embedding_size = 150

init_embeds = tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0)
embeddings = tf.Variable(init_embeds)

train_inputs = tf.placeholder(tf.int32, shape=[None])
embed = tf.nn.embedding_lookup(embeddings, train_inputs)

nce_weights = tf.Variable(
    tf.truncated_normal([vocabulary_size, embedding_size], stddev=1.0/np.sqrt(embedding_size))
)
nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

loss = tf.reduce_mean(tf.nn.nce_loss(nce_weights, nce_biases, train_labels, embed, num_sampled, vocabulary_size))

optimizer = tf.train.AdamOptimizer(learning_rate)
trianing_op = optimizer.minimize(loss)

norm = tf.sqrt(tf.reduce_mean(tf.square(embeddings), axis=1, keepdims=True))
normalized_embeddings = embeddings / norm
valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
similarity = tf.matmul(valid_embeddings, normalized_embeddings, transpose_b=True)

init = tf.global_variables_initializer()

num_steps = 10001

with tf.Session() as sess:
    init.run()
    average_loss = 0
    for step in range(num_steps):
        print("\rIteration:{}".format(step), end="\t")
        batch_inputs, batch_labels = generate_batch(batch_size, num_skips, skip_window)
        feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}
        _, loss_val = sess.run([trianing_op, loss], feed_dict=feed_dict)
        average_loss += loss_val
        if step % 2000 == 0:
            if step > 0:
                average_loss /= 2000
            print("Average loss at step", step, ":", average_loss)
            average_loss = 0
        if step % 10000 == 0:
            sim = similarity.eval()
            for i in range(valid_size):
                valid_word = vocabulary[valid_examples[i]]
                top_k = 8
                nearst = (-sim[i, :]).argsort()[1:top_k + 1]
                log_str = "Nearest to %s:" % valid_word
                for k in range(top_k):
                    close_word = vocabulary[nearst[k]]
                    log_str = "%s %s," % (log_str, close_word)
                print(log_str)
    final_embedding = normalized_embeddings.eval()

np.save("./my_final_embeddings.npy", final_embedding)


def plot_with_labels(low_dim_embs, labels):
    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    plt.figure(figsize=(18, 18))
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        plt.annotate(
            label,
            xy=(x, y),
            xytext=(5, 2),
            textcoords="offset points",
            ha="right",
            va="bottom"
        )
    plt.show()


tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
plot_only = 500
low_dim_embs = tsne.fit_transform(final_embedding[:plot_only, :])
labels = [vocabulary[i] for i in range(plot_only)]
plot_with_labels(low_dim_embs, labels)

# reset_graph()
#
# n_steps = 50
# n_neurons = 200
# n_layers = 3
# num_encoder_symbols = 20000
# num_decoder_symbols = 20000
# embedding_size = 150
# learning_rate = 0.01
#
# X = tf.placeholder(tf.int32, [None, n_steps])
# Y = tf.placeholder(tf.int32, [None, n_steps])
# W = tf.placeholder(tf.float32, [None, n_steps - 1, 1])
# Y_input = Y[:, :-1]
# Y_target = Y[:, 1:]
#
# encoder_inputs = tf.unstack(tf.transpose(X))
# decoder_inputs = tf.unstack(tf.transpose(Y_input))
#
# lstm_cells = [tf.nn.rnn_cell.BasicLSTMCell(num_units=n_neurons) for layer in range(n_layers)]
# cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cells)
#
# output_seqs, states = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(
#     encoder_inputs,
#     decoder_inputs,
#     cell,
#     num_encoder_symbols,
#     num_decoder_symbols,
#     embedding_size
# )
# logits = tf.transpose(tf.unstack(output_seqs), perm=[1, 0, 2])
#
# logits_flat = tf.reshape(logits, [-1, num_decoder_symbols])
# Y_target_flat = tf.reshape(Y_target, [-1])
# W_flat = tf.reshape(W, [-1])
# xentropy = W_flat * tf.nn.sparse_softmax_cross_entropy_with_logits(labels=Y_target_flat, logits=logits_flat)
# loss = tf.reduce_mean(xentropy)
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# training_op = optimizer.minimize(loss)
#
# init = tf.global_variables_initializer()




