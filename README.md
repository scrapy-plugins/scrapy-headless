# Scrapy Selenium

This is a plugin to make it easier to use scrapy with a selenium grid


## Questions

- py27,34,35,36
- scrapy 1.1, 1.2, 1.3, 1.4, 1.5
- pipenv or no pipenv?
- ci?

- How to setup selenium timeout?? how much? where? How?
- Should it be able to support normal selenium(non-grid)
    - Yes but not on first installment
- Should it support custom driver creation? How? Spider method?
    - Yes but ont on first installment
- How should the user control what the webdriver does? Overriding the Download Handler or a spider method?
    - Overriding for now
- SeleniumRequest or a meta flag? Does SeleniumRequest need anything else?
- What else should be tested?
    - Test coverage
