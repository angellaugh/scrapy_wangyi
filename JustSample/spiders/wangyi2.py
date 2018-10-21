'''
1. 翻页；
2. 存储
'''

import scrapy
import pandas



class QuotesSpider(scrapy.Spider):
    name = "wangyi1802"
    dftotal = pandas.DataFrame(columns=('title', 'author', 'createTime', 'favorite', 'share', 'comment'))
    dftotal.to_excel('wangyi05.xls')

    def start_requests(self):
        urls = [
            'http://music.163.com/discover/playlist'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        s = response.css('div.u-page')

        pageurl = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'
        for page1 in range(0, 2):
            # 取前五页，将数据传入
            page = page1*35
            next_page = pageurl.format(page)
            # print(next_page)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield  scrapy.Request(next_page,callback=self.parse_list,meta={'url': next_page},encoding='utf-8')

    def parse_list(self, response):
        s = response.css('ul.m-cvrlst')
        for total in s:
            title = total.css('p.dec a::text').extract();
            author = total.css('a.nm-icn::text').extract();
            count = total.css('span.nb::text').extract();
            url = total.css('p.dec a[href*=play]::attr(href)').extract();
            # print('第一页的35个歌单-%s,作者%s,播放次数%s,歌单链接%s' %title %autor %count %url)
            mycontent = dict(title=title, autor=author, count=count, url=url)
            # print(dict(title=title,autor=autor,count=count,url=url))
            print(mycontent)
            df = pandas.DataFrame(mycontent)
            df.to_excel('aa.xls')

        for next_page in url:
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield  scrapy.Request(next_page,callback=self.parse_inside,meta={'url': next_page},encoding='utf-8')

    def parse_inside(self,response):
        s = response.css('div.g-wrap6')
        url = response.meta['url']

        for s1 in s:
            createTime = s1.css('span.time::text').extract_first()
            createTimeUpdate = createTime.split('\xa0')[0]
            fav = s1.css('a.u-btni-fav i::text').extract_first()
            favUpdate = fav.split('(')[1].split(')')[0]
            share1 = s1.css('a.u-btni-share::attr(data-count)').extract_first()
            shareUpdate = int(share1)
            comment = s1.css('a.u-btni-cmmt span[id=cnt_comment_count]::text').extract_first()
            author = s1.css('a.s-fc7::text').extract_first()
            title=s1.css('div.tit h2::text').extract_first()
            # ddataInside = dict(title = [title],author=[author],creatTime= [createTimeUpdate], favorite= [favUpdate], share = [shareUpdate], comment= [comment])

            ddataInside = dict(title = title,author = author,createTime = createTimeUpdate,
                              favorite = favUpdate,share = shareUpdate,comment = comment)



            df = pandas.DataFrame(ddataInside,index=[0])
            print(1)
            print(df)
            hadInfo = pandas.read_excel('wangyi05.xls')
            print(2)
            print(hadInfo)
            Totalinfor= pandas.concat([hadInfo,df])
            print(3)
            print(Totalinfor)

            Totalinfor.to_excel('wangyi05.xls')