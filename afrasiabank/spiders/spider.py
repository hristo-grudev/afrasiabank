import scrapy

from scrapy.loader import ItemLoader

from ..items import AfrasiabankItem
from itemloaders.processors import TakeFirst


class AfrasiabankSpider(scrapy.Spider):
	name = 'afrasiabank'
	start_urls = ['https://www.afrasiabank.com/en/about/newsroom']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="newsmore-intro-block"]//h1/text()|//div[@class="title"]/h1/text()').get()
		description = response.xpath('//div[@class="text-only-block"]//text()[normalize-space() and not(ancestor::div[@class="news-nav"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date"]/text()|//div[@class="date-published"]/div[@class="txt2"]/text()').get()

		item = ItemLoader(item=AfrasiabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
