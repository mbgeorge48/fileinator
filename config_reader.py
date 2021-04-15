import yaml


class ConfigReader:

    def __init__(self):
        config_path = 'config.yml'
        self.config = self.read_yml_config(config_path)
        self.x = self.config.get('x')

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