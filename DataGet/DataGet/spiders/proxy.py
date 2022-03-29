import scrapy
from scrapy import Request,Spider
from pyquery import PyQuery
from DataGet.items import ProxyItem


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['proxy']
    start_urls = ['http://proxy/']
    page = 1
    kuaidaili_url = "https://www.kuaidaili.com/free/inha/{page}/"
    _66daili_url = "http://www.66ip.cn/areaindex_{page}/1.html"
    ip3366_url = "http://www.ip3366.net/?stype=1&page={page}"

    def start_requests(self):
        yield Request(url=self.kuaidaili_url.format(page=self.page), callback=self.kuaidaili_parse)
        yield Request(url=self._66daili_url.format(page=self.page), callback=self._66_daili_parse)
        yield Request(url=self.ip3366_url.format(page=self.page), callback=self.ip3366_parse)
        # yield Request(url=self.xicidail_url.format(page=1), callback=self.xicidaili_parse)

    def kuaidaili_parse(self, response):
        pq = PyQuery(response.text)
        item = ProxyItem()
        proxies = pq.find("#list .table-bordered tbody").find("tr")
        for proxy in proxies.items():
            ip = proxy.find("td").eq(0).text()
            port = proxy.find("td").eq(1).text()
            item["proxy"] = ip + ":" + port
            print("从%s成功获取代理：IP：%s PORT：%s" % ("www.kuaidaili.com", ip, port))
            yield item
        now_page = int(response.url.split("/")[-2])
        next_page = now_page + 1
        if next_page <= 10:
            yield Request(url=self.kuaidaili_url.format(page=str(next_page)), callback=self.kuaidaili_parse,
                          dont_filter=True)

    def _66_daili_parse(self, response):
        pq = PyQuery(response.text)
        item = ProxyItem()
        proxies = pq.find("#footer table tr:gt(0)")
        for proxy in proxies.items():
            ip = proxy.find("td").eq(0).text()
            port = proxy.find("td").eq(1).text()
            item["proxy"] = ip + ":" + port
            print("从%s成功获取代理：IP：%s PORT：%s" % ("http://www.66ip.cn", ip, port))
            yield item
        now_page = int(response.url.split("/")[-2].split("_")[1])
        next_page = now_page + 1
        if next_page <= 34:
            yield Request(url=self._66daili_url.format(page=str(next_page)), callback=self._66_daili_parse,
                          dont_filter=True)

    def ip3366_parse(self, response):
        pq = PyQuery(response.text)
        item = ProxyItem()
        proxyies = pq.find("#list table tbody tr:gt(0)")
        for proxy in proxyies.items():
            ip = proxy.find("td").eq(0).text()
            port = proxy.find("td").eq(1).text()
            item["proxy"] = ip + ":" + port
            print("从%s成功获取代理：IP：%s PORT：%s" % ("www.ip3366.net", ip, port))
            yield item
        now_page = int(response.url.split("=")[2])
        next_page = now_page + 1
        if next_page <= 10:
            yield Request(url=self.ip3366_url.format(page=str(next_page)), callback=self.ip3366_parse, dont_filter=True)
