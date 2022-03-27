from dataclasses import dataclass
from api import RESTAPI
import logger

log = logger.get_logger(__name__)


@dataclass
class Device:
    system_name: str
    type: str
    hdd_capacity: str
    id: str = None


class DevicesAPI(RESTAPI):

    def check_alive(self):
        return self.get(self.base_url)

    def get_devices(self) -> list:
        log.debug('Get all devices list')

        return self.get(self.base_url + 'devices').json()

    def get_device_by_name(self, name: str) -> list:
        """
        Get the list of devices and returns a list with the ones which match name.
        It is not clear if system_name is unique system-wide, good guess it is not unique.
        :param name:
        :return:
        """
        devices = self.get_devices()
        return [d for d in devices if d['system_name'] == name]

    def get_device_by_id(self, device_id: str) -> dict:
        log.debug(f'Get device by id: {device_id}')

        return self.get(self.base_url + 'devices' + f'/{device_id}').json()

    def add_device(self, device: Device):
        log.debug(f'Add device: {device}')

        return self.post(url=self.base_url + 'devices', payload=device.__dict__).json()

    def update_device(self, device: Device):
        log.debug(f'Update device: {device}')

        return self.put(url=self.base_url + 'devices' + '/' + device.id, payload=device.__dict__).json()

    def delete_device(self, device_id: str):
        log.debug(f'Delete device by id: {device_id}')

        return self.delete(self.base_url + 'devices' + f'/{device_id}').json()


if __name__ == '__main__':
    devices_api = DevicesAPI(base_url='http://localhost:3000/')
    log.info(devices_api.check_alive().json()['response'])

    # list devices
    for api_device in devices_api.get_devices():
        devices_api.get_device_by_id(api_device['id'])

    # add device
    new_device = Device(system_name='pySystem', type='pyType', hdd_capacity='import this')
    added_device = Device(**devices_api.add_device(new_device))
    log.info(f'added device: {added_device}')

    added_device.system_name = 'SUPPA PYTHON'
    devices_api.update_device(added_device)

    _device = devices_api.get_device_by_id(added_device.id)
    log.info(f'Device: {_device}')

    r = devices_api.delete_device(added_device.id)
    log.info(f'Delete result: {r}')

    for api_device in devices_api.get_devices():
        devices_api.get_device_by_id(api_device['id'])
