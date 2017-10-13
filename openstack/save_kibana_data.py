# coding=utf8
from mongoengine import connect
from datetime import datetime
from elasticsearch import Elasticsearch
from models.question import Questions_content
from models.answer import Answers
import string
from gensim.models import word2vec
import libs


import random
# st = "07:30:00"
# et = "09:30:00"
st = "09:30:00"
et = "11:30:00"

def time2seconds(t):
    h,m,s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def seconds2time(sec):
    m,s = divmod(sec,60)
    h,m = divmod(m,60)
    return "%02d:%02d:%02d" % (h, m, s)

sts = time2seconds(st) #sts==27000
ets = time2seconds(et) #ets==34233



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
    from datetime import datetime
    es = Elasticsearch()
    questions = get_all_questions()
    for question in questions:
        es.index(index="kibana-1", doc_type="kibana-1", body=question.to_json())


if __name__ == "__main__":
    init()
    es = get_es()
    rt = random.sample(range(sts, ets), 2210)
    # rt == [28931, 29977, 33207, 33082, 31174, 30200, 27458, 27434, 33367, 30450]

    rt.sort()  # 对时间从小到大排序

    ips = ['192.168.0.2', '192.168.0.3', '192.168.0.4', '192.168.0.5']

    for r in rt:
        dtstr = '2017-04-20 ' + seconds2time(r)
        datetime = datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
        ip = ips[random.randint(0, 3)]
        data = {
            'timestamp': datetime,
            'level': 'INFO',
            'status': 200,
            'module': 'nova.metadata.wsgi.server',
            'time': float(random.randint(100, 1000)) / 100000,
            'ip': ip
        }
        es.index(index="kibana1-test", doc_type="data-1", body=data)
        print data
    # save_all_questions()
