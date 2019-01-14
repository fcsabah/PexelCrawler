import scrapy
import os
import requests
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class PexelSpider(CrawlSpider):
    name = "PexelSpider"
    allowed_domains = ['www.pexels.com']
    start_urls = ["https://www.pexels.com/"]
    rules = [Rule(LinkExtractor(allow_domains="www.pexels.com"), follow=True, callback='parse_link')]

    def parse_link(self, response):
        image_links = response.xpath('//*[@download="true"]/../a/@href').extract()
        path_to_store_image = '/home/fahad/Spyder_Projects/PexelCrawler/images/'
        request_url = response.request.url
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}

        if not os.path.exists(path_to_store_image):
            os.makedirs(path_to_store_image)

        for image_link in image_links:
            if "images.pexels.com" not in image_link:
                continue
            image_id = image_link.split('/')[4]
            image_name = path_to_store_image + image_id +'.jpeg'
            if os.path.exists(image_name):
                continue

            picture_request = requests.get(image_link, headers=headers)
            if picture_request.status_code == 200:
                with open(image_name, 'wb') as f:
                    f.write(picture_request.content)
            else:
                print("response code %d for image id %s" % picture_request.status_code, image_id)

        if '/photo/' not in request_url and '/photos/' not in request_url:
            for page_no in range(0,41):
                Ajax_Request_URL = 'https://www.pexels.com/?dark=true&format=js&page=%d' % page_no
                yield scrapy.Request(url=Ajax_Request_URL, headers=headers, callback=self.Ajax_Parse)
                time.sleep(1)

    def Ajax_Parse(self, response):
        path_to_store_image = '/home/fahad/Spyder_Projects/PexelCrawler/images/'
        if not os.path.exists(path_to_store_image):
            os.makedirs(path_to_store_image)

        image_links = response.xpath('//*[@download="true"]/../a/@href').extract()
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}

        for image_link in image_links:
            if "images.pexels.com" not in image_link:
                continue
            image_id = image_link.split('/')[4]
            image_name = path_to_store_image + image_id +'.jpeg'
            if os.path.exists(image_name):
                continue

            picture_request = requests.get(image_link, headers=headers)
            if picture_request.status_code == 200:
                with open(image_name, 'wb') as f:
                    f.write(picture_request.content)
            else:
                print("response code %d for image id %s" % picture_request.status_code, image_id)