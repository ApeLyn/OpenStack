# coding=utf8
from mongoengine import connect
from datetime import datetime
from elasticsearch import Elasticsearch
from models.question import Questions
from models.answer import Answers
import string
import libs
from gensim.models import word2vec


def init():
    connect('stackoverflow', host='127.0.0.1', port=27017)


def get_es():
    es = Elasticsearch()
    return es


def get_models():
    model = word2vec.Word2Vec.load("openstack_with_q.model")
    return model


def get_answers_by_word(sentence):
    init()
    es = get_es()

    # 获取model
    model = get_models()

    # save_all_questions()
    input_str = "Failed to add image. Got error: The request returned 500 Internal Server Error"
    words = libs.get_word_line(input_str)
    words = words.split(' ')
    words.remove('')
    ava_words = []
    for word in words:
        if word in model.wv.vocab:
            ava_words.append(word)

    # 过滤输入的字符串
    exclude = set(string.punctuation)
    should = []
    for word in ava_words:
        if not word:
            continue
        pure_word = ''.join(ch for ch in word if ch not in exclude)
        y2 = model.most_similar(pure_word.lower(), topn=5)
        # libs.get_word_line(pure_word)
        should.append({
            "match": {
                "title": {
                    "query": pure_word.lower(),
                    "boost": 1
                }
            }
        })
        for y in y2:
            should.append({
                "match": {
                    "title": {
                        "query": y[0],
                        "boost": y[1]
                    }
                }
            })
            # print y[0]
            # print y[1]
        print "done!!"

    query = {
      "query": {
        "bool": {
          "should": should
        }
      }
    }
    params = {
        'size': 10
    }
    print query
    pass
    result = es.search(index="openstack", doc_type="question", body=query, params=params)
    data = result['hits']['hits']
    print len(data)
    for result in data:
        # print result['_source']['title']
        title = libs.get_word_line(result['_source']['title'])
        title_words = title.split(' ')
        title_words.remove('')
        real_words = []
        for word in title_words:
            if word in model.wv.vocab:
                real_words.append(word)
        # print real_words
        print model.n_similarity(real_words, ava_words)
        # get_answers_by_url(result['_source']['url'])
        # print result['_source']['title']
    # print "hello world"

