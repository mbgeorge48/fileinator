import yaml


class ConfigReader:

    def __init__(self):
        config_path = 'config.yml'
        self.config = self.read_yml_config(config_path)
        self.windows_hostname = self.config.get('windows_hostname')
        self.mac_hostname = self.config.get('mac_hostname')

        self.local_path = self.config.get('local_path')
        self.remote_path = self.config.get('remote_path')

    def read_yml_config(self, filename):
        """
        Takes in config yaml file and returns the config from it
        """
        with open(filename, 'r') as stream:
            try:
                config = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

        return config