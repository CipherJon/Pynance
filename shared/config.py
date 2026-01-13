# shared/config.py

"""
Configuration module for shared settings.
"""


class SharedConfig:
    """
    A class to manage shared configuration settings.
    """

    def __init__(self):
        """
        Initialize the SharedConfig instance.
        """
        self.settings = {}

    def set_setting(self, key: str, value):
        """
        Set a configuration setting.

        Args:
            key (str): The key for the setting.
            value: The value to store for the setting.
        """
        self.settings[key] = value

    def get_setting(self, key: str):
        """
        Retrieve a configuration setting.

        Args:
            key (str): The key for the setting.

        Returns:
            The value associated with the key, or None if the key does not exist.
        """
        return self.settings.get(key)
