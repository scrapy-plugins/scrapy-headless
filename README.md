# Scrapy Headless

This is a plugin to make it easier to use scrapy with headless browsers, at the moment it only works with selenium grid as a driver.

## Installation

For now the project is in a private bit bucket repo, so install it from there:
```
pip install scrapy-headless
```

## Usage

You will first need to have a selenium grid server running, you may find some examples on:  https://github.com/SeleniumHQ/docker-selenium/wiki/Getting-Started-with-Docker-Compose

The easiest way is by using docker-compose, here is a example docker-compose.yml file:

```yml
selenium-hub:
  image: selenium/hub
  ports:
  - 4444:4444

chrome:
  image: selenium/node-chrome
  links:
  - selenium-hub:hub
  environment:
    - HUB_PORT_4444_TCP_ADDR=hub
    - GRID_TIMEOUT=180 # Default timeout is 30s might be low for Selenium
  volumes:
  - /dev/shm:/dev/shm
```

And just,
```
$ docker-compose up -d
```

And, if you want more browser instances
```
$ docker-compose up -d --scale chrome=3 # For 3 browsers
```

On scrapy you will need to update your settings, for example:
```py
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

SELENIUM_GRID_URL = 'http://localhost:4444/wb/hub'  # Example for local grid with docker-compose
SELENIUM_NODES = 1  # Number of nodes(browsers) you are running on your grid
SELENIUM_CAPABILITIES = DesiredCapabilities.CHROME  # Example for Chrome

# You need also to change the default download handlers, like so:
DOWNLOAD_HANDLERS = {
    "http": "scrapy_selenium.SeleniumDownloadHandler",
    "https": "scrapy_selenium.SeleniumDownloadHandler",
}
```

You may also set a proxy for your selenium requests:
```py
SELENIUM_PROXY = 'http://proxy.url:port'
```

Now all you need to do, is on your spider, for the requests you want handled by selenium use `HeadlessRequest` instead of scrapy's Request, for example:
```py
from scrapy import Spider
from scrapy_headless import HeadlessRequest


class SomeSpider(Spider):
    ...
    def some_parser(self, response):
        ...
        yield HeadlessRequest(some_url, callback=self.other_parser)
```

If you need to do something with the driver after getting the url you may also set a `driver_callback`:
```py
from scrapy import Spider
from scrapy_headless import HeadlessRequest


class SomeSpider(Spider):
    ...
    def some_parser(self, response):
        ...
        yield HeadlessRequest(some_url, callback=self.other_parser, driver_callback=self.process_webdriver)

    def process_webdriver(self, driver):
        ...
```

## Future
Ideally this download handler should be able to use any of the following:

- [x] Selenium Grid
- [ ] Selenium (without grid)
- [ ] Pyppeteer