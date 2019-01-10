# -*- coding: utf-8 -*-
"""training_utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c6G8p33Kj3ytdp8GYsO5YNbL_Hshiz4R
"""

from google.colab import drive
#drive.mount('/content/drive')
import tensorflow as tf
import numpy as np
import re
import time

def input_ph():
  input = tf.placeholder(tf.int32,[None,None],name = 'input')
  output = tf.placeholder(tf.int32,[None,None],name = 'ouput')
  lr = tf.placeholder(tf.float32,name = 'learning_rate')
  keep_prob = tf.placeholder(tf.float32,name = 'droupout_rate')
  return input,output,lr,keep_prob

def batch_divide(taget,batchsize,word_int_dict):
  sos = tf.fill([batchsize,1],word_int_dict['<SOS>'])
  q_batch = tf.strided_slice(target,[0,0],[batchsize,-1],stride=[1,1])
  batch = tf.concat([sos,q_batch],1)
  return batch

def encoder_form(rnn_inputs,rnn_size,num_layers,keep_prob,sequence_list):
  lstm = tf.contrib.rnn.BasicLSTMCell(rnn_size)
  drop_shit = tf.contrib.rnn.DropoutWrapper(lstm,input_keep_prob = keep_prob)
  single_encoder = tf.contrib.rnn.MultiRNNCell([drop_shit]*num_layers)
  a,encoder_state = tf.nn.Bdirectional_dynamic_rnn(cell_fw = single_encoder,cell_bw = single_encoder,sequence_length = sequence_list,inputs = rnn_inputs,dtype = tf.float32)
  return encoder_state

def decoder_form_training_set(encoder_state, decoder_cell, decoder_embedded_input, sequence_length, decoding_scope, output_function, keep_prob, batch_size):
    attention_states = tf.zeros([batch_size, 1, decoder_cell.output_size])
    attention_keys, attention_values, attention_score_function, attention_construct_function = tf.contrib.seq2seq.prepare_attention(attention_states, attention_option = "bahdanau", num_units = decoder_cell.output_size)
    training_decoder_function = tf.contrib.seq2seq.attention_decoder_fn_train(encoder_state[0],attention_keys,attention_values,attention_score_function,attention_construct_function,name = "attn_dec_train")
    decoder_output, decoder_final_state, decoder_final_context_state = tf.contrib.seq2seq.dynamic_rnn_decoder(decoder_cell,training_decoder_function,decoder_embedded_input,sequence_length,scope = decoding_scope)
    decoder_output_dropout = tf.nn.dropout(decoder_output, keep_prob)
    return output_function(decoder_output_dropout)

