# -*- coding: utf-8 -*-
"""Perceptron.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y_rbUTKfVA7cTEikGkUxK3lWw2lBrj4H
"""

import random
import numpy as np
import copy
import matplotlib.pyplot as plt

global weights
global w
global y_pred_lst
weights = []
y_pred_lst = []

def getting_y_dataset(dataset):
  y_label = []
  dataset_tmp = copy.deepcopy(dataset)
  for row in dataset_tmp:
    if row[-1] == 0:
      y_label.append(-1)
    else:
      y_label.append(1)
  return y_label

def putting_bias_in_dataset(dataset):
      # making datasets with no label
      # dataset_train_no_label = np.stack(row[:5] for row in dataset_train)
      # y_label = np.stack(row[-1] for row in dataset_train)
      # dataset_test_no_label = np.stack(row[:4] for row in dataset_test)
    
    dataset_with_bias = []
    for row in dataset:
      row[-1] = 1
      dataset_with_bias.append(row)

    return dataset_with_bias

def standard_perceptron(dataset_train_with_bias, y_train_label, epoch, r):

  # initialising weight and average
  w = np.zeros(len(dataset_train_with_bias[0]))

  for i in range(epoch):

    # shuffle the data
    np.random.shuffle(dataset_with_bias)

    for i in range(len(dataset_train_with_bias)):

      # update weight for each examples x_i
      if y_train_label[i]*np.dot(w.transpose(),dataset_train_with_bias[i]) <= 0:
        w += r*y_train_label[i]*dataset_train_with_bias[i] 
        weights.append(w)

  return w

def voted_perceptron(dataset_train_with_bias, y_train_label, epoch, r):

  # initialising weight and average
  w = np.zeros(len(dataset_train_with_bias[0]))
  weights.append(w)

  # initialising c and m
  m = 0
  c = 0
  c_lst = []
  c_lst.insert(0,c)

  for i in range(epoch):

    # shuffle the data
    np.random.shuffle(dataset_train_no_label)

    for i in range(len(dataset_train_with_bias)):

      # update weight for each examples x_i
      if y_train_label[i]*np.dot(w.transpose(),dataset_train_with_bias[i]) <= 0:
        w += r*y_train_label[i]*dataset_train_with_bias[i]
        weights.append(w)
        m += 1
        c_lst.insert(m,1)
      else:
        c_lst[m] += 1

  return weights,c_lst

def average_perceptron(dataset_train_with_bias, y_train_label, epoch, r):
 
  # initialising weight and average
  w = np.zeros(len(dataset_train_with_bias[0]))
  av_w = np.zeros(len(dataset_train_with_bias[0]))
  weights.append(w)

  # counter for incorrect matches
  count = 0

  for i in range(epoch):

    # shuffle the data
    np.random.shuffle(dataset_train_no_label)

    for i in range(len(dataset_train_with_bias)):

      # update weight for each examples x_i
      if y_train_label[i]*np.dot(w.transpose(),dataset_train_with_bias[i]) <= 0:
        w = w + r*y_train_label[i]*dataset_train_with_bias[i]
    
      # average weight
      av_w += w
  return av_w

def std_predictions(dataset, w):
  y_pred = np.dot(dataset, w)
  for y in y_pred:
    if y <= 0:
      y = -1
    else:
      y = 1
  return y_pred

def av_predictions(dataset, a):
  y_pred = np.dot(dataset, a)
  for y in y_pred:
    if y <= 0:
      y = -1
    else:
      y = 1
  return y_pred

def v_predictions(c_lst, w_lst, dataset):
  y_pred = []
  for i,c in enumerate(c_lst):
    inner_product = np.dot(dataset, w_lst[i])
    for i in inner_product:
      if i <= 0:
        i = -1
      else:
        i = 1
    y_pred.append(c * inner_product) 
  
  y_pred_sum = np.zeros(len(y_pred[0]))
  for i in range(1,len(y_pred)):
    y_pred_sum += np.add(y_pred[i-1], y_pred[i])
  
  for y in y_pred_sum:
    if y <= 0:
      y = -1
    else:
      y = 1
  return y_pred_sum

def main():
  # empty arrays for train and test datasets
  dataset_train_raw = []
  dataset_test_raw = []
  # import train dataset
  with open('drive/MyDrive/ML_data/bank-note/train.csv', 'r') as train_file:
      for line in train_file:
          terms = line.strip().split(',')
          dataset_train_raw.append(terms)

  # import test dataset
  with open('drive/MyDrive/ML_data/bank-note/test.csv', 'r') as test_file:
      for line in test_file:
          terms = line.strip().split(',')
          dataset_test_raw.append(terms)

  dataset_train = [] 
  dataset_test = [] 
  # converting the datatype of each entry into float      
  for row in dataset_train_raw:
      row = np.asarray(row,dtype=float)
      dataset_train.append(row)
  for row in dataset_test_raw:
      row = np.asarray(row,dtype=float)
      dataset_test.append(row)
  
  # creating dataset with bias and seperate the labels for training
  y_train_label = getting_y_dataset(dataset_train)
  dataset_train_with_bias = putting_bias_in_dataset(dataset_train)

  #epoch and r
  epoch = 10
  r = 0.1

  # getting actual label
  y_actual = []
  for row in dataset_test:
    y_actual.append(row[-1])

  # Question 2.A
  # standard perceptron model ( = final weight)
  count_std = 0
  w = standard_perceptron(dataset_train_with_bias,y_train_label,epoch, r)
  print("weights for standard = ", w)

  # prediction
  y_pred = std_predictions(dataset_test, w)

  # count incorrect predictions
  for i, y in enumerate(y_pred):
    if y != y_actual[i]:
      count_std += 1

  avg_pred_err_std = count_std / len(dataset_test)
  print("average prediction error for standard perceptron = ", avg_pred_err_std)

  # Question 2.B
  # voted perceptron model ( = final weight)
  count_v = 0
  weights, c_lst = voted_perceptron(dataset_train_with_bias,y_train_label,epoch, r)
  print("list weights for voted perceptron", weights[0:5])
  print("counts of correctly predicted training examples = ", c_lst)

  y_pred_lst_v = []
  # prediction
  for i,c in enumerate(c_lst):
    y_pred = v_predictions(c[i],weights[i],dataset_test)
    y_pred_lst_v.append(y_pred)
    
  # count incorrect predictions
  for i, y in enumerate(y_pred_lst_v):
    if y[i] != y_actual[i]:
      count_v += 1
  
  avg_pred_err_v = count_v / len(dataset_test)
  print("average prediction error for voted perceptron = ", avg_pred_err_v)

  # Question 2.C
  # average perceptron model ( = final weight)
  count_av = 0
  av_w = average_perceptron(dataset_train_with_bias,y_train_label,epoch, r)
  print("learned weight for average perceptron = ", av_w)

  # prediction
  y_pred = std_predictions(dataset_test, w)

  # count incorrect predictions
  for i, y in enumerate(y_pred):
    if y != y_actual[i]:
      count_av += 1

  avg_pred_err_av = count_av / len(dataset_test)
  print("average prediction error for average perceptron = ", avg_pred_err_av)

if __name__ == "__main__":
  main()
