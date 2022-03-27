import random

import pytest
import pandas as pd

from testdata import device_props
from api.devices import DevicesAPI
from pom.navigator import DevicesUI
import config
import logger

parser = config.parser
parser.add_argument('--ui-url', help='URL to client app', env_var='UI_URL')
parser.add_argument('--api-url', help='URL to server app', env_var='API_URL')
parser.add_argument('--implicit-wait', type=str, default=10,
                    help='The web driver to wait for a certain amount of time '
                         'before it throws a "No Such Element Exception". Default: %(default)s',
                    env_var='IMP_WAIT')

cfg, _ = parser.parse_known_args()

log = logger.get_logger(__name__, cfg.log_level)
log.info(cfg)


def dataframe_difference(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Find rows which are different between two DataFrames.

    :param df1: first dataframe.
    :param df2: second dataframe.
    :return:    if there is different between both dataframes.
    """
    comparison_df = df1.merge(df2, indicator=True, how='outer')
    diff_df = comparison_df[comparison_df['_merge'] != 'both']
    return diff_df


class TestDevices(object):
    """
    Make an API call to retrieve the list of devices.
    Use the list of devices to check the elements are visible in the DOM.
    Check the
        name,
        type
        and capacity
        of each element of the list using the class names and
        make sure they are correctly displayed. - not clear criteria what is "correctly displayed".
    Verify that all devices contain the edit and delete buttons.
    """

    @classmethod
    def teardown_class(cls):
        # here you should report test results to test case management system for reporting historical purposes.
        pass

    api = DevicesAPI(base_url=cfg.api_url)
    expected_devices = api.get_devices()  # get the list of devices returned from API
    log.debug(f'{len(expected_devices)} devices from API')

    ui = DevicesUI(browser='Chrome', url=cfg.ui_url, implicit_wait=cfg.implicit_wait)
    actual_devices = ui.get_devices_list()  # get the list of devices from UI to compare further

    @pytest.mark.parametrize('name', [d['system_name'] for d in expected_devices],
                             ids=[d['system_name'] for d in expected_devices])
    def test_each_device_displayed_alpha(self, name: str):
        """
        This test literally searches for an element in UI for each device by name.
        :param name:
        :return:
        """
        device = self.ui.get_device_by_name(name)
        assert device.is_displayed()

    @pytest.mark.parametrize('device', actual_devices,
                             ids=[d['system_name'] for d in actual_devices])
    def test_each_device_displayed_beta(self, device: dict):
        """
        The test iterates over the list of devices read from UI and check displayed value.
        :param device
        :return:
        """
        assert device['displayed']

    @pytest.mark.parametrize('device', actual_devices,
                             ids=[d['system_name'] for d in actual_devices])
    def test_each_device_has_edit(self, device: dict):
        assert device['edit']

    @pytest.mark.parametrize('device', actual_devices,
                             ids=[d['system_name'] for d in actual_devices])
    def test_each_device_has_remove(self, device: dict):
        assert device['remove']

    def test_devices(self):
        """
        The test expected the lists of devices from API and from UI are to be identical.
        :return:
        """
        expected = pd.DataFrame(self.expected_devices)  # convert list of dict to pandas dataframe
        actual = pd.DataFrame(self.actual_devices)
        actual.drop(labels=['edit', 'remove', 'displayed'], axis=1, inplace=True)  # remove excessive columns

        diff = dataframe_difference(expected, actual)  # do outer merge with mark what is one side only
        result = len(diff) == 0
        assert result, diff

    def test_devices_fail_on_purpose(self):
        """
        This test purposely fails with one extra element in "expected devices".
        This would happen if UI did not display one or more devices.
        :return:
        """
        self.expected_devices.append({'id': 'abc', 'system_name': 'olalala', 'type': 'oy', 'hdd_capacity': '123'})
        expected = pd.DataFrame(self.expected_devices)
        actual = pd.DataFrame(self.actual_devices)
        actual.drop(labels=['edit', 'remove', 'displayed'], axis=1, inplace=True)

        diff = dataframe_difference(expected, actual)
        result = len(diff) == 0
        assert result, diff


class TestAddDevice(object):
    """
    Verify that devices can be created properly using the UI.
    Verify the new device is now visible. Check name, type and capacity are visible and correctly displayed to the user.

    Since system_name is not unique system-wide we may have more than one element with the same name in UI.
    When a new device created, UI does not return its unique id. One of the ways to intercept http response and get the
    exact id of the new added device is to run MITM proxy. This can be done with python and Selenium,
    but will take longer time to implement.

    """

    api = DevicesAPI(base_url=cfg.api_url)
    ui = DevicesUI(browser='Chrome', url=cfg.ui_url, implicit_wait=1)

    @pytest.fixture(scope='class')
    def add_device_via_ui(self) -> dict:
        new_device = {'system_name': random.choice(device_props.first_names).upper() + '-' +
                                     random.choice(device_props.size_matters).upper() + '-' +
                                     random.choice(device_props.platforms).upper(),
                      'device_type': random.choice(device_props.device_types),
                      'hdd_capacity': str(2 ** random.randint(7, 12))
                      }

        try:
            self.ui.add_device(**new_device)
            log.info(f'Added new device: {new_device}')
            return new_device

        except Exception as e:
            log.error(f'Could not add a device via UI: {new_device}')
            log.exception(e)
            raise

    @classmethod
    def teardown_class(cls):
        """
        Here I should delete the added device via API to return the system to the previous state.
        :return:
        """
        # device_id = %placeholder%
        # cls.api.delete_device(device_id)
        pass

    def test_new_device_api(self, add_device_via_ui):
        """
        Read the created device from API
        :param add_device_via_ui:
        :return:
        """
        expected_device = add_device_via_ui
        log.info(f'Looking for the device in API: {expected_device}')

        # this place is not correct intentionally
        # take only the first device from UI with matching name.
        # all others will be ignored.
        # to do it right way, have to intercept id of the created device in HTTP response
        actual_devices = self.api.get_device_by_name(expected_device['system_name'])
        log.info('Devices found with system name \'{}\':\n {}'.format(expected_device['system_name'], actual_devices))
        actual_device = actual_devices[0]
        actual_device.pop('id')
        actual_device['device_type'] = actual_device.pop('type')

        assert actual_device == expected_device

    def test_new_device_ui(self, add_device_via_ui):
        """
        Read the created device from UI. The device is searched by name which may cause ambiguous recognition.
        :param add_device_via_ui:
        :return:
        """
        expected_device = add_device_via_ui
        log.info(f'Looking for the device in UI: {expected_device}')

        # # reread the list of devices from UI
        # actual_devices = self.ui.get_devices_list()
        # # since we go by name, let's take just the first one. later it is bette to switch to id.
        # actual_device = [d for d in actual_devices if d['system_name'] == expected_device['system_name']][0]

        actual_device = self.ui.get_device_details(self.ui.get_device_by_name(expected_device['system_name']))

        # drop and rename the keys to match dict structure
        drop_keys = ['displayed', 'id', 'remove', 'edit']
        for key in drop_keys:
            actual_device.pop(key)
        actual_device['device_type'] = actual_device.pop('type')

        assert actual_device == expected_device

    def test_new_device_visible(self, add_device_via_ui):
        assert self.ui.get_device_details(self.ui.get_device_by_name(add_device_via_ui['system_name']))['displayed']

