import pytest

from api.devices import DevicesAPI
from pom.devices import DevicesUI
import config
import logger

parser = config.parser
parser.add_argument('--ui-url', help='URL to client app', env_var='UI_URL')
parser.add_argument('--api-url', help='URL to server app', env_var='API_URL')

cfg, _ = parser.parse_known_args()

log = logger.get_logger(__name__, cfg.log_level)
log.info(cfg)


class TestMainPage(object):
    api = DevicesAPI(base_url=cfg.api_url)
    expected_devices = api.get_devices()
    log.debug(f'{len(expected_devices)} devices from API')

    ui = DevicesUI(browser='Chrome', url=cfg.ui_url)

    @pytest.mark.parametrize('name', [d['system_name'] for d in expected_devices],
                             ids=['test_device_displayed_' + d['system_name'] for d in expected_devices])
    def test_each_device_displayed(self, name):
        device = self.ui.get_device_by_name(name)
        assert device.is_displayed()
