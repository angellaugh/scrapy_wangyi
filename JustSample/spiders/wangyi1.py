'''
1. 访问 网易云音乐热歌；
2. 提取第一页的内容；
3. 保存到excel；

'''


import scrapy
import pandas

class QuotesSpider(scrapy.Spider):
    name = "wangyi1801"

    def start_requests(self):
        urls = [
            'http://music.163.com/discover/playlist'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for total in response.css('ul.m-cvrlst'):
            title = total.css('p.dec a::text').extract()
            autor = total.css('a.nm-icn::text').extract()
            count = total.css('span.nb::text').extract()
            url = total.css('p.dec a[href*=play]::attr(href)').extract()
            # print('第一页的35个歌单-%s,作者%s,播放次数%s,歌单链接%s' %title %autor %count %url)
            total_infor = dict(title=title,autor=autor,count=count,url=url)

            df = pandas.DataFrame(total_infor)
            df.to_excel('wangyi0530.xls')
