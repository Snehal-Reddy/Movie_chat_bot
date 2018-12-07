# -*- coding: utf-8 -*-
"""preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ouAKUkuJdgrRYwU9QeRrYysLZAiCOhgk
"""

import tensorflow as tf
import numpy as np
import re
import time
from google.colab import drive

##drive.mount('/content/drive')
!pwd
lines = open('drive/My Drive/Chat_bot/movie_lines.txt',encoding='utf-8',errors = 'ignore').read().split('\n')
conv = open('drive/My Drive/Chat_bot/movie_conversations.txt',encoding='utf-8',errors = 'ignore').read().split('\n')

id_line_dict = {}
for line in lines:
  
  words = line.split(' +++$+++ ')
  id_line_dict[words[0]] = words[-1]

conv_list = []
for line in conv:
  line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
  conv_list.append(line.split(','))
print(conv_list[0])

questions = []
answers = []
print(len(conv_list))
for convo in conv_list:
  for i in range(len(convo)-1):
    questions.append(id_line_dict[convo[i]])
    answers.append(id_line_dict[convo[i+1]])

def cleaner(lines):
  #print(lines)
  lines = lines.lower()
  lines = re.sub(r"'s"," is",lines)
  lines = re.sub(r"'ll"," will",lines)
  lines = re.sub(r"'ve"," have",lines)
  lines = re.sub(r"'re"," are",lines)
  lines = re.sub(r"'d"," would",lines)
  lines = re.sub(r"won't","will not",lines)
  lines = re.sub(r"can't","cannot",lines)
  lines = re.sub(r"-[}{#/@]","",lines)
  return lines

clean_answers = []
for answer in answers:
  clean_answers.append(cleaner(answer))

clean_questions = []
for question in questions:
  #print(type(question))
  clean_questions.append(cleaner(question))

word_count = {}
for answer in clean_answers:
  for word in answer:
    if word in word_count:
      word_count[word]+=1
    else:
      word_count[word] = 1

for question in clean_questions:
  for word in question:
    if word in word_count:
      word_count[word]+=1
    else:
      word_count[word] = 1

threshold = 20
question_word_id_dict = {}
number = 0
for word , count in word_count.items():
  if count >= threshold :
    question_word_id_dict[word] = count
  number+=1
answer_word_id_dict = {}
number = 0
for word , count in word_count.items():
  if count >= threshold :
    answer_word_id_dict[word] = count
  number+=1

tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']
for token in tokens:
  question_word_id_dict[token] = len(question_word_id_dict)+1
for token in tokens:
  answer_word_id_dict[token] = len(answer_word_id_dict)+1

id_answer_word_dict = {i : w for w , i in answer_word_id_dict.items()}

for i in range(len(clean_answers)):
  clean_answers[i]+='<EOS>'

questions_id_list = []
ints = []
for question in clean_questions:
  for word in question.split():
    if word not in question_word_id_dict:
      ints.append('<OUT>')
    else:
      ints.append(word)
  questions_id_list.append(ints)
answers_id_list = []
ints = []
for answer in clean_questions:
  for word in answer.split():
    if word not in answer_word_id_dict:
      ints.append('<OUT>')
    else:
      ints.append(word)
  answers_id_list.append(ints)

sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1,26):
  for i in enumerate(questions_id_list):
    if len(i[0])==length:
      sorted_clean_questions.append(questions_id_list[i[0]]) 
      sorted_clean_questions.append(questions_id_list[i[0]])