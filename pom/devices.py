import pom.locators as locators
from pom import WebDriverSetup


class DevicesUI(WebDriverSetup):
    def __init__(self, browser, url):
        super().__init__(browser)
        # self.driver = driver
        self.url = url
        self.open_ui()

    def open_ui(self):
        self.driver.get(self.url)

    def close_ui(self):
        self.driver.close()

    def get_devices_element(self):
        return self.driver.find_element(**locators.MainPage.devices)

    def get_devices_list(self):
        return self.driver.find_elements(**locators.MainPage.device)

    @staticmethod
    def get_device_details(device_element):
        details = {
            'name': device_element.find_element(**locators.MainPage.device_name).text,
            'type': device_element.find_element(**locators.MainPage.device_type).text,
            'capacity': device_element.find_element(**locators.MainPage.device_capacity).text,
            'edit': device_element.find_element(**locators.MainPage.device_edit),
            'remove': device_element.find_element(**locators.MainPage.device_remove),
            'id': device_element.find_element(**locators.MainPage.device_edit).get_attribute('href').split('/')[-1],
            'displayed': device_element.is_displayed()
        }

        return details

    def get_device_by_name(self, name):
        return self.driver.find_element(**locators.MainPage.find_device_by_name(name))

