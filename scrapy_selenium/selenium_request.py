from scrapy import Request


class SeleniumRequest(Request):
    def __init__(self, url, callback=None, method="GET", headers=None, **kwargs):
        super(SeleniumRequest, self).__init__(url, callback, method, headers, **kwargs)
