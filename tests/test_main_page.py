from operator import itemgetter
import pytest
import pandas as pd

from api.devices import DevicesAPI
from pom.navigator import DevicesUI
import config
import logger

parser = config.parser
parser.add_argument('--ui-url', help='URL to client app', env_var='UI_URL')
parser.add_argument('--api-url', help='URL to server app', env_var='API_URL')

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
    api = DevicesAPI(base_url=cfg.api_url)
    expected_devices = api.get_devices()  # get the list of devices returned from API
    log.debug(f'{len(expected_devices)} devices from API')

    ui = DevicesUI(browser='Chrome', url=cfg.ui_url)
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




