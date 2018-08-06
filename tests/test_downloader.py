import tempfile

from scrapy.settings import Settings
from scrapy import Request
from scrapy.spiders import Spider
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from twisted.protocols.policies import WrappingFactory
from twisted.web import server, static
from twisted.internet import reactor
from twisted.python.filepath import FilePath
from pytest_mock import mocker

from scrapy_selenium.selenium_downloader import SeleniumDownloadHandler
from scrapy_selenium.selenium_request import SeleniumRequest


def get_downloader(proxy=False, settings_dict=None):
    settings_dict = settings_dict or {
        "SELENIUM_GRID_URL": "https://selenium.grid",
        "SELENIUM_NODES": 3,
        "SELENIUM_CAPABILITIES": DesiredCapabilities.FIREFOX,
    }
    if proxy:
        settings_dict["SELENIUM_PROXY"] = "172.12.2.1:2122"
    settings = Settings(settings_dict)
    return SeleniumDownloadHandler(settings)


def test_settings():
    downloader = get_downloader()
    assert downloader.grid_url == "https://selenium.grid"
    assert downloader.selenium_nodes == 3
    assert downloader._threadpool.max == 3
    assert downloader._threadpool.min == 3
    assert downloader.capabilities == DesiredCapabilities.FIREFOX


def test_selenium_proxy():
    downloader = get_downloader(True)
    assert downloader.capabilities == {
        "browserName": "firefox",
        "marionette": True,
        "acceptInsecureCerts": True,
        "proxy": {
            "proxyType": "MANUAL",
            "ftpProxy": "172.12.2.1:2122",
            "httpProxy": "172.12.2.1:2122",
            "sslProxy": "172.12.2.1:2122",
        },
        "acceptSslCerts": True,
    }


def test_download_with_proxy_https_noconnect():
    def _test(response):
        assert response.status == 200
        assert response.url == request.url
        assert response.body == b"0123456789"

    tmpname = tempfile.mkdtemp(dir="/tmp/")
    FilePath(tmpname).child("file").setContent(b"0123456789")
    r = static.File(tmpname)
    site = server.Site(r, timeout=None)
    wrapper = WrappingFactory(site)
    port = reactor.listenTCP(0, wrapper, interface="localhost")
    portno = port.getHost().port

    http_proxy = "http://localhost:%d/file" % (portno,)
    request = Request(http_proxy)
    downloader = get_downloader()
    return downloader.download_request(request, Spider("foo")).addCallback(_test)


def test_selenium_stuff(mocker):
    def _test(response):
        assert response.status == 200
        assert response.url == request.url
        assert response.body == b"selenium page"
        downloader.close()

    driver = mocker.patch("scrapy_selenium.selenium_downloader.Remote").return_value

    driver.page_source = "selenium page"
    driver.current_url = "http://selenium.request.com/"

    url = "http://selenium.request.com/"
    request = SeleniumRequest(url)
    downloader = get_downloader()
    return downloader.download_request(request, Spider("foo")).addCallback(_test)
