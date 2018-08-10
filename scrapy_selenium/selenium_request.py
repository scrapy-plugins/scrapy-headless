from scrapy import Request


class SeleniumRequest(Request):
    def __init__(
        self,
        url,
        callback=None,
        method="GET",
        headers=None,
        driver_callback=None,
        **kwargs
    ):
        self.driver_callback = driver_callback
        super(SeleniumRequest, self).__init__(url, callback, method, headers, **kwargs)
