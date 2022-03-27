from selenium.webdriver.common.by import By


class MainPage:
    devices = {'by': By.CSS_SELECTOR, 'value': '.list-devices'}
    device = {'by': By.CSS_SELECTOR, 'value': '.device-main-box'}
    device_name = {'by': By.CSS_SELECTOR, 'value': '.device-name'}
    device_type = {'by': By.CSS_SELECTOR, 'value': '.device-type'}
    device_capacity = {'by': By.CSS_SELECTOR, 'value': '.device-capacity'}
    device_edit = {'by': By.CSS_SELECTOR, 'value': '.device-edit'}
    device_remove = {'by': By.CSS_SELECTOR, 'value': '.device-remove'}
    add_device_btn = {'by': By.CSS_SELECTOR, 'value': '.submitButton'}

    @staticmethod
    def find_device_by_name(name):
        # find .device-name class with text in span and go 2 levels up for the main object
        value = f'.//span[@class="device-name" and contains(text(), "{name}")]/../..'
        return {'by': By.XPATH, 'value': value}

    @staticmethod
    def find_device_by_id(device_id):
        value = f'//a[contains(@class, "device-edit") and contains(@href, "{device_id}")]/../..'
        return {'by': By.XPATH, 'value': value}


class DevicePage:
    system_name = {'by': By.ID, 'value': 'system_name'}
    type = {'by': By.ID, 'value': 'type'}
    hdd_capacity = {'by': By.ID, 'value': 'hdd_capacity'}
    submit_btn = {'by': By.CSS_SELECTOR, 'value': '.submitButton'}
