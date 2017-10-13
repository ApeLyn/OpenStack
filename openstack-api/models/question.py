from mongoengine import *


class Questions(Document):
    url = StringField(required=True)
    title = StringField(required=True)
    topic = IntField(missing=0)

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(id=id).first()

    @classmethod
    def get_all_questions(cls):
        return cls.objects()

    @property
    def topic(self):
        return 0
        pass

    def to_json(self):
        return {
            'url': self.url,
            'title': self.title,
            'topic': self.topic,
            'id': str(self.id)
        }

    @classmethod
    def get_questions_by_page(cls, page):
        return cls.objects().skip(page * 10).limit(10)
