# -*- coding:utf8 -*-
import nltk
import os

porterStem = nltk.stem.PorterStemmer()
lancasterStem = nltk.stem.lancaster.LancasterStemmer()
wordEngStop = nltk.corpus.stopwords.words('english')
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*', '=', 'abstract=',
                        '{', '}']


def get_word_line(line):

    eachLine = line.encode('utf-8').lower().decode('utf-8', 'ignore')  # 小写
    tokens = nltk.word_tokenize(eachLine)  # 分词（与标点分开）
    wordLine = ''
    for word in tokens:
        if not word in english_punctuations:  # 去标点
            if not word in wordEngStop:  # 去停用词
                # word = porterStem.stem(word)
                # word = lancasterStem.stem(word)
                wordLine += word + ' '
    print wordLine
    return wordLine
