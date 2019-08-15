# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 09:54:41 2019

@author: zzx
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#读取数据
mnist = input_data.read_data_sets('/datasets/ud730/mnist', one_hot=True, reshape=False)
#设定参数
learning_rate = 0.01
epoch = 10
n_features = 28*28
n_labels = 10
batch_size = 128
n_hiddens = 256

#初始化权重和偏移
weights = {'weight_input':tf.Variable(tf.random_normal([n_features,n_hiddens]))
          ,'weight_output':tf.Variable(tf.random_normal([n_hiddens,n_labels]))
}
biases = {'biases_input':tf.Variable(tf.random_normal([n_hiddens]))
          ,'biase_output':tf.Variable(tf.random_normal([n_labels]))
}

#定义各种变量
features = tf.placeholder(tf.float32,[None,28,28,1])
features_ = tf.reshape(features,[-1,n_features])
labels = tf.placeholder(tf.float32,[None,n_labels])

#定义节点前向流动关系
hidden_layer = tf.add(tf.matmul(features_,weights['weight_input']),biases['biases_input'])
hidden_layer = tf.nn.relu(hidden_layer)
output = tf.add(tf.matmul(hidden_layer,weights['weight_output']),biases['biase_output'])

#优化策略，反向传播
cost = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits = output,labels = labels))
optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate).minimize(cost)
#计算精确度（此处应用测试集）
correct_prediction = tf.equal(tf.arg_max(output,1),tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#运行session
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for i in range(epoch):
        total_batch = int(mnist.train.num_examples/batch_size)
        for i in range(total_batch):
            features_value,labels_value = mnist.train.next_batch(batch_size)
            sess.run(optimizer,feed_dict = {features:features_value,labels:labels_value})

    print(sess.run(accuracy,feed_dict = {features:features_value,labels:labels_value}))

    
    
