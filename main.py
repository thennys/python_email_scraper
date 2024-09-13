import re
from typing import Final

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException


# Regex used for finding e-mails in text
# EMAIL_REGEX: Final[str] = r"'(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])"

# Simplified email regex for most use cases
EMAIL_REGEX: Final[str] = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


class Browser:
    def __init__(self, driver: str):
        print('Starting up browser........')
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-gpu')
                                         
        try:
            self.Service = Service(driver)
            self.browser = webdriver.Chrome(service=self.Service, options=self.chrome_options)
        except WebDriverException as e:
            print(f"Error starting the browser: {e}")
            raise

    def scrape_emails(self, url: str) -> set:
        try:
            self.browser.get(url)
            print(f'Scraping: "{url}" for emails')
            page_source: str = self.browser.page_source
            # print(page_source)

            list_of_emails: set = set()

            for re_match in re.finditer(EMAIL_REGEX, page_source):
                list_of_emails.add(re_match.group())

            return list_of_emails
        except Exception as e:
            print(f"Error during scraping: {e}")
            return set()
    
    def close_browser(self):
        print('Closing browser')
        self.browser.close()

def main():
    driver:str = r"C:\Users\Administrator\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    # Option 2: Escape backslashes
    # driver: str = "C:\\Users\\Administrator\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

    browser = Browser(driver=driver)


    #emails:set = browser.scrape_emails('https://www.facebook.com')
    # emails:set= browser.scrape_emails('https://www.randomlists.com/email-addresses?qty=50')
    url: str = 'https://www.randomlists.com/email-addresses?qty=50'
    emails: set = browser.scrape_emails(url)
    
    if emails:
        for i, email in enumerate(emails, start=1):
            print(f"{i}  : {email}")
    else:
        print("No Emails found")
        browser.close_browser()

if __name__ == '__main__':
    main()