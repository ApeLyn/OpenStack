from flask import Flask, jsonify, request
app = Flask(__name__)

from mongoengine import connect
from datetime import datetime
from elasticsearch import Elasticsearch
from models.question import Questions
from models.answer import Answers
import string
# import libs
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    page -= 1
    data = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5],
        'page': int(page)
    }
    questions = Questions.get_questions_by_page(page)
    result = []
    for question in questions:
        result.append(question.to_json())
    return jsonify(result)


@app.route('/questions')
@crossdomain(origin='*')
def get_questions():
    page = int(request.args.get('page', 1))
    page -= 1
    data = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5],
        'page': int(page)
    }
    questions = Questions.get_questions_by_page(page)
    result = []
    for question in questions:
        result.append(question.to_json())
    return jsonify(result)


@app.route('/content/<id>')
def get_content(id):
    question = Questions.get_by_id(id)
    answers = Answers.get_by_question_url(question.url)
    result = []
    for answer in answers:
        result.append(answer.to_json())
    return jsonify(result)


def init():
    connect('stackoverflow', host='127.0.0.1', port=27017)


if __name__ == '__main__':
    init()
    Answers.save_template_data()
    app.run(debug=True)
