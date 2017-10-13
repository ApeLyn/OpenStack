from mongoengine import *


class Answers(Document):
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

    @classmethod
    def save_template_data(cls):
        answer = Answers()
        answer.user_id = '/users/4665710/bharath-shetty'
        answer.url = '/questions/20235276/openstack-compute-nova-error'
        answer.start_time = '2017-05-23 10:27:16Z'
        answer.votes = '14'
        answer.desc = '<div class="post-text" itemprop="text"><p>If you used devstack (<a href="http://devstack.org/" rel="nofollow noreferrer">http://devstack.org/</a>) to deploy OpenStack you can use openrc trick:</p><pre><code>$cd devstack/$source openrc admin admin # for admin rights</code></pre><p>or</p><pre><code>$source openrc demo demo # for demo user</code></pre><p>Otherwise you need to export OS variables manually:</p><pre><code>$export OS_USERNAME = admin$export OS_TENANT_NAME = &lt;yourtenant&gt;$export OS_PASSWORD = &lt;yourpasswd&gt; # password which you used during deployment etc</code></pre><p>Related question <a href="https://stackoverflow.com/questions/20005279/how-to-manage-users-passwords-in-devstack">How to manage users/passwords in devstack?</a></p><p>If you want manually install all the services heres handy manual <a href="https://github.com/mseknibilel/OpenStack-Grizzly-Install-Guide/blob/OVS_MultiNode/OpenStack_Grizzly_Install_Guide.rst" rel="nofollow noreferrer">https://github.com/mseknibilel/OpenStack-Grizzly-Install-Guide/blob/OVS_MultiNode/OpenStack_Grizzly_Install_Guide.rst</a></p><p>I d recommend to install it once by this manual to learn how it works, and then use latest stable devstack each time when you need to set up a new environment just to save your time.</p><p>Regards</p></div>'
        answer.save()