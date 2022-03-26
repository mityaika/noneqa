from selenium.webdriver.common.by import By


class MainPage:
    devices = {'by': By.CSS_SELECTOR, 'value': '.list-devices'}
    device = {'by': By.CSS_SELECTOR, 'value': '.device-main-box'}
    device_name = {'by': By.CSS_SELECTOR, 'value': '.device-name'}
    device_type = {'by': By.CSS_SELECTOR, 'value': '.device-type'}
    device_capacity = {'by': By.CSS_SELECTOR, 'value': '.device-capacity'}
    device_edit = {'by': By.CSS_SELECTOR, 'value': '.device-edit'}
    device_remove = {'by': By.CSS_SELECTOR, 'value': '.device-remove'}

    @staticmethod
    def find_device_by_name(name):
        value = f'//span[contains(@class, "device-name") and .//text()="{name}"]'
        return {'by': By.XPATH, 'value': value}

