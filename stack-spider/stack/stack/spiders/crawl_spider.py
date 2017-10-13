from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from stack.items import StackItem
from stack.question_links import QLinkItem


class StackSpider(CrawlSpider):
    name = "stackcrawl"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        # "http://stackoverflow.com/questions?sort=newest",
    ]
    for i in range(1, 36):
        url = 'http://stackoverflow.com/questions/tagged/openstack?page=%s&sort=votes&pagesize=50' % str(i)
        start_urls.append(url)
    rules = (
        Rule(
            SgmlLinkExtractor(allow=('&page=\d&pagesize=\d')),
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        questions = hxs.xpath('//div[@class="summary"]/h3')
        for question in questions:
            item = QLinkItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
