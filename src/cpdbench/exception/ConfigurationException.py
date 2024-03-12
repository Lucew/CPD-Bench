class ConfigurationException(Exception):
    """General error for inconsistencies and errors in the given config file."""
    exc_message = "Error in configuration file: Invalid value for {0}, using default value."

    def __init__(self, config_variable):
        super().__init__(self.exc_message.format(config_variable))


class ConfigurationFileNotFoundException(Exception):
    """Error if a given config file path does not exist"""
    exc_message = "Given config file path [{0}] does not exist. Using default config values."

    def __init__(self, config_variable):
        super().__init__(self.exc_message.format(config_variable))
