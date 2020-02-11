from setuptools import setup


with open("README.md") as f:
    readme = f.read()


setup(
    name="scrapy-headless",
    version="0.0.1",
    license="BSD",
    description="Download Handler for using Scrapy with headless browsers",
    maintainer="Henrique Coura",
    maintainer_email="coura.henrique@gmail.com",
    author="Scrapinghub",
    author_email="opensource@scrapinghub.com",
    url="https://github.com/scrapy-plugins/scrapy-headless",
    packages=["scrapy_headless"],
    platforms=["Any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Scrapy",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["scrapy>=1.6.0"],
)
