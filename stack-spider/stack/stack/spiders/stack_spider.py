from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem
from stack.question_links import QLinkItem
from stack.QuestionItem import QuestionItem
from stack.AnswerItem import AnswerItem
from stack.users import UserItem
from scrapy.conf import settings
import pymongo
import time


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    db = connection[settings['MONGODB_DB']]
    collection = db[settings['MONGODB_COLLECTION']]
    links = []
    print "!!!test"
    for link_item in\
            connection['stackoverflow'].questions.find():
        print 'http://stackoverflow.com' + link_item['url']
        links.append('http://stackoverflow.com' + link_item['url'])
        # break
    # for link_item in connection['stackoverflow'].answers.find():
    #     links.append('http://stackoverflow.com' + link_item['user_id'])
    start_urls = links
    # start_urls = [
    #     "http://stackoverflow.com/questions?sort=newest",
    # ]
    # for i in range(1, 36):
    #     url = 'http://stackoverflow.com/questions/tagged/openstack?page=%s&sort=votes&pagesize=50' % str(i)
    #     start_urls.append(url)
    # rules = (
    #     Rule(
    #         SgmlLinkExtractor(allow=('&page=\d&pagesize=\d')),
    #         callback='parse',
    #         follow=True
    #     ),
    # )

    def parse(self, response):
        # GET URL
        # questions = Selector(response).xpath('//div[@class="summary"]/h3')
        #
        # for question in questions:
        #     item = QLinkItem()
        #     item['title'] = question.xpath(
        #         'a[@class="question-hyperlink"]/text()').extract()[0]
        #     item['url'] = question.xpath(
        #         'a[@class="question-hyperlink"]/@href').extract()[0]
        #     yield item
        # questions = Selector(response).xpath('//div[@class="summary"]/h3')

        ###### get q info
        # item = QuestionItem()
        # title = Selector(response).xpath('//div[@id="question-header"]/h1/a/text()').extract()[0]
        # url = Selector(response).xpath('//div[@id="question-header"]/h1/a/@href').extract()[0]
        # mainbar = Selector(response).xpath('//div[@id="question"]')
        # # print mainbar
        # votes = Selector(response).xpath('//div[@id="question"]/table/tr/td/div/span/text()').extract()[0]
        # desc = str(Selector(response).xpath('//td[@class="postcell"]/div/div[@class="post-text"]').extract()[0]).strip()
        # tags = Selector(response).xpath('//td[@class="postcell"]/div/div[@class="post-taglist"]/a/text()').extract()
        # start_time = Selector(response).xpath('//td[@class="post-signature owner"]/div/div/span[@class="relativetime"]/@title').extract()[0]
        # update_time = Selector(response).xpath('//div[@class="user-action-time"]/span[@class="relativetime"]/@title').extract()[0]
        # user_id = Selector(response).xpath(
        #     '//td[@class="post-signature owner"]/div/div[@class="user-details"]/a/@href').extract()
        # item['source'] = 'stackoverflow'
        # item['title'] = title
        # item['url'] = url
        # item['votes'] = votes
        # item['desc'] = desc
        # item['tag'] = tags
        # item['user_id'] = user_id
        # item['start_time'] = start_time
        # item['update_time'] = update_time
        # yield item

        ##### get answer info
        answers = Selector(response).xpath('//div[@class="answer"]')
        ac_answer = Selector(response).xpath('//div[@class="answer accepted-answer"]')
        answers.extend(ac_answer)
        url = Selector(response).xpath('//div[@id="question-header"]/h1/a/@href').extract()[0]
        print "!!!!!!!!!!!"
        print len(answers)
        for answer in answers:
            item = AnswerItem()
            votes = answer.xpath('table/tr/td/div/span/text()').extract()[0]
            desc = answer.xpath('table/tr/td[@class="answercell"]/div[@class="post-text"]').extract()[0]
            user_ids = answer.xpath('table/tr/td[@class="answercell"]/table/tr/td[@class="post-signature"]/div/div[@class="user-details"]/a/@href').extract()
            action_time = answer.xpath('table/tr/td[@class="answercell"]/table/tr/td[@class="post-signature"]/div/div[@class="user-action-time"]/span/@title').extract()
            print action_time
            if len(action_time) == 1:
                start_time = action_time[0]
                update_time = action_time[0]
            elif len(action_time) == 2:
                start_time = action_time[1]
                update_time = action_time[0]
            if len(user_ids) == 1:
                user_id = user_ids[0]
            elif len(user_ids) == 2:
                user_id = user_ids[1]
            else:
                user_id = ''
            item['votes'] = votes
            item['desc'] = desc
            item['user_id'] = user_id
            item['start_time'] = start_time
            item['update_time'] = update_time
            item['url'] = url
            yield item

        ##### get user profile
        # item = UserItem()
        # print "!!!!!!"
        # item['name'] = Selector(response).xpath('//h2[@class="user-card-name"]/text()').extract()[0]
        # item['url'] = Selector(response).xpath('//div[@class="avatar"]/a/@href').extract()[0]
        # item['source'] = 'sf'
        # item['answer_num'] = Selector(response).xpath('//div[@class="stat answers col-3"]/span/text()').extract()[0]
        # item['votes'] = Selector(response).xpath('//div[@class="stat people-helped col-5"]/span/text()').extract()[0]
        # item['tags'] = Selector(response).xpath('//a[@class="post-tag"]/text()').extract()
        # item['ranking'] = Selector(response).xpath('//span[@class="top-badge"]/a/b/text()').extract()
        # if item['ranking']:
        #     item['ranking'] = item['ranking'][0]
        #
        # item['name'] = item['name'].replace(' ', '').replace('\n', '')
        # item['votes'] = item['votes'].replace('~', '')
        # print item
        # yield item

    def get_links(cls):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        collection = db[settings['MONGODB_COLLECTION']]
        # print collection
        links = []
        for link_item in connection['stackoverflow'].questions.find():
            print 'http://stackoverflow.com' + link_item['url']
            links.append('http://stackoverflow.com' + link_item['url'])
        return links[0]

    def second_step(cls):
        links = cls.get_links()


