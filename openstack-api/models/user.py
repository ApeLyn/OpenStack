from mongoengine import *


class Users(Document):
    user_id = StringField(required=True)
    url = StringField(required=True)
    start_time = StringField(required=True)
    update_time = StringField(required=True)
    votes = StringField(required=True)
    desc = StringField(required=True)
    question_id = ObjectIdField()

    @classmethod
    def get_all_answers(cls):
        return cls.objects()

    @classmethod
    def get_by_question_url(cls, url):
        return cls.objects(url=url)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'url': self.url,
            'start_time': self.start_time,
            'votes': int(self.votes),
            'content': self.desc
        }
