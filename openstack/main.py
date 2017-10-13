# coding=utf8
from mongoengine import connect
from datetime import datetime
from elasticsearch import Elasticsearch
from models.question import Questions_content
from models.answer import Answers
import string
from gensim.models import word2vec
import libs
from models.question_base import Questions

def init():
    connect('stackoverflow', host='127.0.0.1', port=27017)


def get_es():
    es = Elasticsearch()
    return es


def get_all_questions():
    questions = Questions_content.get_all_questions()
    for question in questions:
        print question.title
    return questions


def get_answers_by_url(url):
    answers = Answers.get_by_question_url(url)
    for answer in answers:
        print answer.desc


def save_all_questions():
    es = Elasticsearch()
    questions = get_all_questions()
    for question in questions:
        es.index(index="openstack", doc_type="question", body=question.to_json())


def get_models():
    model = word2vec.Word2Vec.load("openstack_with_q.model")
    return model


def get_questions_by_keyword(keyword):
    init()
    es = get_es()

    # 获取model
    model = get_models()

    # save_all_questions()
    input_str = keyword
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
    questions = []
    for result in data:
        # print result['_source']['title']
        title = libs.get_word_line(result['_source']['title'])
        url = result['_source']['url']
        print url

        title_words = title.split(' ')
        title_words.remove('')
        real_words = []
        for word in title_words:
            if word in model.wv.vocab:
                real_words.append(word)
        print model.n_similarity(real_words, ava_words)

        question = Questions_content.get_question_by_url(url)
        if question:
            question_content = question.to_json()
            question_content['sim'] = model.n_similarity(real_words, ava_words)
            questions.append(question_content)
            # print question.to_json()
        else:
            print "NONE!"
        # get_answers_by_url(result['_source']['url'])
        # print result['_source']['title']
    # print "hello world"
    questions = sorted(questions, key=lambda x:x['sim'], reverse=True)
    print questions
    return questions


def splitStr(str1, seperateStr):
    res = [str1]
    for splitFlag in seperateStr:
        t = []
        map(lambda x: t.extend(x.split(splitFlag)),res)
        print "res is ",res
        res = t
    return res


def get_words():
    init()
    count = 0
    questions = Questions.objects()
    for question in questions:
        title_words = question.title
        title_words = splitStr(title_words, '?!.')
        print str(title_words)
        count += len(title_words)
    print count


if __name__ == "__main__":
    # get_questions_by_keyword("openstack compute nova error")
    get_words()