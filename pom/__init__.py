from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverSetup:
    def __init__(self, browser: str = 'Chrome', implicit_wait: int = 10):
        if browser.lower() == 'chrome':
            options = Options()
            options.add_argument('start-maximized')
            # options.add_experimental_option('detach', True)
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.implicitly_wait(implicit_wait)
        else:
            raise AttributeError(f'Browser {browser} not implemented.')

    def __del__(self):
        # pass
        if self.driver:
            self.driver.close()
            # self.driver.quit()

