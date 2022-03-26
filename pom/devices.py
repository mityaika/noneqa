import locators


class Devices:
    def __init__(self, driver):
        self.driver = driver

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

