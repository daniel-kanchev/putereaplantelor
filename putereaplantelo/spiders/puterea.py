import scrapy
from datetime import datetime
from itemloaders.processors import TakeFirst
from putereaplantelo.items import Article
from scrapy.loader import ItemLoader


class PutereaSpider(scrapy.Spider):
    name = 'puterea'
    allowed_domains = ['putereaplantelor.ro']
    start_urls = ['https://putereaplantelor.ro/blog']

    def parse(self, response):
        links = response.xpath("//a[@class='more-link']/@href").getall()
        yield from response.follow_all(links, self.parse_article)

        next_page = response.xpath("//div[@class='pagination-next alignright']/a/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article(), response)
        item.default_output_processor = TakeFirst()

        title = response.xpath("(//h1)[1]//text()").get()
        date = response.xpath("//time/text()").get()
        date = format_date(date)
        author = response.xpath("//span[@class='entry-author-name']/text()").get()

        categories = response.xpath("(//span[@class='entry-terms'])[1]//text()").getall()
        categories.pop(0)
        categories = [cat for cat in categories if cat.strip()]
        categories = "".join(categories)

        tags = response.xpath("(//span[@class='entry-terms'])[2]//text()").getall()
        if tags:
            tags.pop(0)
            tags = [tag for tag in tags if tag.strip()]
            tags = "".join(tags)

        content = response.xpath("//div[@class='entry-content']//text()").getall()
        content = " ".join(content)

        item.add_value("title", title)
        item.add_value("date", date)
        item.add_value("author", author)
        item.add_value("categories", categories)
        item.add_value("tags", tags)
        item.add_value("link", response.url)
        item.add_value("content", content)

        return item.load_item()


def format_date(date):
    date_dict = {
        "ianuarie": "January",
        "februarie": "February",
        "martie": "March",
        "aprilie": "April",
        "mai": "May",
        "iunie": "June",
        "iulie": "July",
        "august": "August",
        "septembrie": "September",
        "octombrie": "October",
        "noiembrie": "November",
        "decembrie": "December",
    }

    date = date.split(" ")
    for key in date_dict.keys():
        if date[1] == key:
            date[1] = date_dict[key]
    date = " ".join(date)
    date_time_obj = datetime.strptime(date, '%d %B %Y')
    date = date_time_obj.strftime("%Y/%m/%d")
    return date
