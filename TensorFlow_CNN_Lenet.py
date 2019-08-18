# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 08:37:59 2019

@author: zzx
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import random
import matplotlib.pyplot as plt
from tensorflow.contrib.layers import flatten
from sklearn.utils import shuffle

def load_data():
    mnist = input_data.read_data_sets('/datasets/ud730/mnist',one_hot = True,reshape = False)
    train_imgs, train_labels = mnist.train.images,mnist.train.labels
    validation_imgs,validation_labels = mnist.validation.images,mnist.validation.labels
    test_imgs, test_labels = mnist.test.images,mnist.test.labels
    
    assert(len(train_imgs)==len(train_labels))
    assert(len(validation_imgs)==len(validation_labels))
    assert(len(test_imgs)==len(test_labels))
    
    print("The shape of train_imgs is {}".format(train_imgs.shape))
    print("The shape of each img is {}".format(train_imgs[0].shape))

    
    print("Training set has {} examples".format(len(train_imgs)))
    print("validation set has {} examples".format(len(validation_imgs)))
    print("Test set has {} examples".format(len(test_imgs)))
    print("Each line of labels is like {}".format(train_labels[0]) )
    return train_imgs,train_labels,validation_imgs,validation_labels,test_imgs, test_labels

def pad_imgs(train_imgs,validation_imgs,test_imgs):
    train_imgs = np.pad(train_imgs,((0,0),(2,2),(2,2),(0,0)),'constant')
    validation_imgs = np.pad(validation_imgs,((0,0),(2,2),(2,2),(0,0)),'constant')
    test_imgs = np.pad(test_imgs,((0,0),(2,2),(2,2),(0,0)),'constant')
    
    print("The shape of each img is {}".format(train_imgs[0].shape))
    print("The shape of set is {}".format(train_imgs.shape))
    return train_imgs,validation_imgs,test_imgs
def show_one_img(train_imgs,train_labels):
    index = random.randint(0,len(train_imgs))
    
    plt.figure(figsize = (1,1))
    plt.imshow(train_imgs[index].squeeze(),cmap = 'gray')
    plt.text(0,-5,'{}'.format(train_labels[index]))
    plt.show()
    
def leNet(x):
    mu = 0
    sigma = 0.1
    
    #第一层卷积层，输入数据为(32*32*1),filter为(5*5),共6个，stride为1，输出数据为(28*28*6)
    conv1_w = tf.Variable(tf.truncated_normal(shape = (5,5,1,6),mean = mu,stddev = sigma))
    conv1_b = tf.Variable(tf.zeros(6))
    conv1 = tf.nn.conv2d(x,conv1_w,strides =[1,1,1,1],padding = 'VALID' )+conv1_b
    print('The out put of conv1 is {}'.format(conv1.shape))
    #relu
    conv1 = tf.nn.relu(conv1) 
    #池化，maxpooling,输出为(14*14*6)
    conv1 = tf.nn.max_pool(conv1,ksize = (1,2,2,1),strides = (1,2,2,1),padding = 'VALID')
    print('The out put of conv1_pool is {}'.format(conv1.shape))
    
    #第二层卷积层，输入为(14*14*6),filter为(5*5),共16个，stride为1，输出数据为(10*10*16)
    conv2_w = tf.Variable(tf.truncated_normal(shape = (5,5,6,16),mean = mu,stddev = sigma))
    conv2_b = tf.Variable(tf.zeros(16))
    conv2 = tf.nn.conv2d(conv1,conv2_w,strides =[1,1,1,1],padding = 'VALID' )+conv2_b
    print('The out put of conv2 is {}'.format(conv2.shape))
    #relu
    conv2 = tf.nn.relu(conv2) 
    #池化，maxpooling,输出为(14*14*6)
    conv2 = tf.nn.max_pool(conv2,ksize = (1,2,2,1),strides = (1,2,2,1),padding = 'VALID')
    print('The out put of conv2_pool is {}'.format(conv2.shape))
    
    #展开
    flat = flatten(conv2)
    print('The shape of flat is {}'.format(flat.shape))
    
    #全连接层输入为400，输出为120
    fc1_w = tf.Variable(tf.truncated_normal(shape = (400,120),mean = mu,stddev = sigma))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1 = tf.matmul(flat,fc1_w)+fc1_b
    print('The out put of fc1 is {}'.format(fc1.shape))
    
    #全连接层输入为120，输出为84
    fc2_w = tf.Variable(tf.truncated_normal(shape = (120,84),mean = mu,stddev = sigma))
    fc2_b = tf.Variable(tf.zeros(84))
    fc2 = tf.matmul(fc1,fc2_w)+fc2_b
    print('The out put of fc2 is {}'.format(fc2.shape))
    
    #全连接层输入为84，输出为10
    fc3_w = tf.Variable(tf.truncated_normal(shape = (84,10),mean = mu,stddev = sigma))
    fc3_b = tf.Variable(tf.zeros(10))
    fc3 = tf.matmul(fc2,fc3_w)+fc3_b
    print('The out put of fc3 is {}'.format(fc3.shape))
    
    return fc3
    

   
train_imgs_,train_labels_,validation_imgs_,validation_labels_,test_imgs_, test_labels_ = load_data()
train_imgs_,validation_imgs_,test_imgs_ = pad_imgs(train_imgs_,validation_imgs_,test_imgs_)

show_one_img(train_imgs_,train_labels_)

train_imgs = tf.placeholder(tf.float32,[None,32,32,1])
train_labels = tf.placeholder(tf.int32,[None,len(train_labels_[0])]) 



logits = leNet(train_imgs)
cost = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits = logits,labels = train_labels))
optimizer = tf.train.AdamOptimizer(learning_rate = 0.001).minimize(cost)
correct_prediction = tf.equal(tf.arg_max(logits,1),tf.argmax(train_labels,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
init = tf.global_variables_initializer()
Epoch = 5
batch_size = 128
with tf.Session() as sess:
    sess.run(init)
    print('训练中。。。')
    for i in range(Epoch):
        train_imgs_, train_labels_ = shuffle(train_imgs_,train_labels_)
        for offset in range(0,len(train_imgs_),batch_size):
            end = offset + batch_size
            img_batch,label_batch = train_imgs_[offset:end], train_labels_[offset:end]
            sess.run(optimizer,feed_dict = {train_imgs:img_batch,train_labels:label_batch})
        print('已完成第{}次训练'.format(i+1))
        print(sess.run(accuracy,feed_dict = {train_imgs:train_imgs_,train_labels:train_labels_}))
    print(sess.run(accuracy,feed_dict = {train_imgs:validation_imgs_,train_labels:validation_labels_}))












