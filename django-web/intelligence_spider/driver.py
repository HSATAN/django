'''
def get_text(self, url):
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()

        browser.get(url)
        text = browser.page_source
        browser.quit()
        display.stop()
        return text
    except:
        try:
            browser = webdriver.Firefox()

            browser.get(url)
            text = browser.page_source
            browser.quit()
            return text
        except:
            return None


def get_text_selenium(self, url_list):
    url_list = [url_list[0]]
    try:
        browser = webdriver.Firefox()
        text_list = []
        for url in url_list:
            try:

                browser.get(url)
                text = browser.page_source
                text_list.append(text)
            except:
                pass
        browser.quit()
        return text_list
    except:
        browser.quit()
        return None


def get_page_selenium(cls, url, home_urls):
    try:
        browser = webdriver.Firefox()
        text_list = {}
        for region, url in home_urls.items():
            text_list.setdefault(region, '')
            try:
                browser.get(url)
                text_list[region] = browser.page_source
            except:
                pass
        browser.quit()
        return text_list
    except:
        browser.quit()
        return None
'''