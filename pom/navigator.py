import selenium.common.exceptions


import pom.locators as locators
from pom import WebDriverSetup
import logger

log = logger.get_logger(__name__, 'INFO')


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
        """
        Returns .list-devices element.
        :return:
        """
        return self.driver.find_element(**locators.MainPage.devices)

    @staticmethod
    def get_device_details(device_element):
        def safe_find(f):
            """
            Return None if NoSuchElementException occurs.
            :param f:
            :return:
            """
            try:
                return f
            except selenium.common.exceptions.NoSuchElementException:
                return None

        _system_name = safe_find(device_element.find_element(**locators.MainPage.device_name))
        _type = safe_find(device_element.find_element(**locators.MainPage.device_type))
        _hdd_capacity = safe_find(device_element.find_element(**locators.MainPage.device_capacity))
        _remove = safe_find(device_element.find_element(**locators.MainPage.device_remove))
        _edit = safe_find(device_element.find_element(**locators.MainPage.device_edit))
        details = {
            'system_name': _system_name.text if _system_name else None,
            'type': _type.text if _type else None,
            'hdd_capacity': _hdd_capacity.text.replace(' GB', '') if _hdd_capacity else None,
            'edit': _edit.is_displayed() if _edit else None,
            'remove': _remove.is_displayed() if _remove else None,
            'id': _edit.get_attribute('href').split('/')[-1] if _edit else None,
            'displayed': device_element.is_displayed()
        }

        log.info(f'Details: {details}')

        return details

    def get_devices_list(self) -> list:
        """
        Returns list of device dictionaries
        :return: python list of dictionaries with eacf device details resolved from UI
        """
        device_elements = self.driver.find_elements(**locators.MainPage.device)  # find all tags with device
        devices = list()
        for device_elements in device_elements:
            device = self.get_device_details(device_elements)  # convert element to dictionary
            devices.append(device)

        return devices

    def get_device_by_name(self, name:str):
        """
        Returns UI element by name found by XPath.
        :param name:
        :return:
        """
        return self.driver.find_element(**locators.MainPage.find_device_by_name(name))

    def get_device_by_id(self, device_id:str):
        """
        Returns UI element by id found by XPath.
        :param device_id:
        :return:
        """
        return self.driver.find_element(**locators.MainPage.find_device_by_id(device_id))
