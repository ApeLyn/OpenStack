# -*- coding:utf8 -*-
import nltk
import libs
import sys
sys.path.append('../')
from models.question import Questions
import os
from mongoengine import connect
import codecs


wordEngStop = nltk.corpus.stopwords.words('english')
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*','=','abstract=', '{', '}']
porterStem = nltk.stem.PorterStemmer()
lancasterStem = nltk.stem.lancaster.LancasterStemmer()

fout = open('text.txt', 'a')


connect('stackoverflow', host='127.0.0.1', port=27017)

# 读取数据库中的问题 写入语料库
questions = Questions.get_all_questions()
for q in questions:
    line = q.title
    line = line.encode('utf-8')
    wordLine = libs.get_word_line(line)
    fout.write(wordLine.encode('utf-8') + '\n')


# fin = open('text.txt', 'r')
# for eachLine in fin:
#     wordLine = libs.get_word_line(eachLine)
#     fout.write(wordLine.encode('utf-8')+'\n')
# fin.close()
fout.close()
