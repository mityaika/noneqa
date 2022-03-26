import configargparse

parser = configargparse.get_argument_parser(name='default')

parser.add_argument('--default-config', is_config_file=True, default='config/default.config',
                    help='default config file. default: %(default)s')
parser.add_argument('--config-file', required=False, is_config_file=True,
                    help='environment config file', env_var='ENV_CONFIG_FILE')
parser.add_argument('-l', '--log-level', env_var='LOG_LEVEL', default='INFO', help='default: %(default)s')
